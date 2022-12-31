import time
import uuid

from authlib.integrations.flask_oauth2 import (
    AuthorizationServer as BaseAuthorizationServer,
    ResourceProtector
)
from authlib.integrations.sqla_oauth2 import (
    create_query_client_func,
    create_save_token_func,
    create_bearer_token_validator
)
from authlib.oauth2.rfc6749 import grants
from authlib.oauth2.rfc6749.authenticate_client import (
    _validate_client,
    ClientAuthentication as BaseClientAuthentication
)
from authlib.oauth2.rfc6749.errors import (
    OAuth2Error,
    UnsupportedGrantTypeError,
    UnauthorizedClientError,
    InvalidRequestError,
    InvalidGrantError,
)
from authlib.oauth2.rfc6750 import BearerTokenValidator as BaseBearerTokenValidator
from flask import Flask, current_app
import jwt

from ..models import (
    db,
    Account,
    OAuth2Client,
    OAuth2Token
)


class PasswordGrant(grants.ResourceOwnerPasswordCredentialsGrant):

    TOKEN_ENDPOINT_AUTH_METHODS = ["none"]

    def authenticate_user(self, username: str, password: str):
        user = Account.query.filter_by(username=username).first()
        if user is not None and user.check_password(password=password):
            return user

    def validate_token_request(self):
        """The client makes a request to the token endpoint by adding the
        following parameters using the "application/x-www-form-urlencoded"
        format per Appendix B with a character encoding of UTF-8 in the HTTP
        request entity-body:

        grant_type
             REQUIRED.  Value MUST be set to "password".

        username
             REQUIRED.  The resource owner username.

        password
             REQUIRED.  The resource owner password.

        scope
             OPTIONAL.  The scope of the access request as described by
             Section 3.3.

        If the client type is confidential or the client was issued client
        credentials (or assigned other authentication requirements), the
        client MUST authenticate with the authorization server as described
        in Section 3.2.1.

        For example, the client makes the following HTTP request using
        transport-layer security (with extra line breaks for display purposes
        only):

        .. code-block:: http

            POST /token HTTP/1.1
            Host: server.example.com
            Authorization: Basic czZCaGRSa3F0MzpnWDFmQmF0M2JW
            Content-Type: application/x-www-form-urlencoded

            grant_type=password&username=johndoe&password=A3ddj3w
        """
        # ignore validate for grant_type, since it is validated by
        # check_token_endpoint
        client = self.authenticate_token_endpoint_client()
        # log.debug('Validate token request of %r', client)

        if not client.check_grant_type(self.GRANT_TYPE):
            raise UnauthorizedClientError()

        # params = self.request.form
        params = self.request.args
        if 'username' not in params:
            raise InvalidRequestError('Missing "username" in request.')
        if 'password' not in params:
            raise InvalidRequestError('Missing "password" in request.')

        # log.debug('Authenticate user of %r', params['username'])
        user = self.authenticate_user(
            params['username'],
            params['password']
        )
        if not user:
            raise InvalidRequestError(
                'Invalid "username" or "password" in request.',
            )
        self.request.client = client
        self.request.user = user
        self.validate_requested_scope()


class RefreshTokenGrant(grants.RefreshTokenGrant):

    TOKEN_ENDPOINT_AUTH_METHODS = ["none"]
    INCLUDE_NEW_REFRESH_TOKEN = True

    def authenticate_refresh_token(self, refresh_token: str):
        # return super().authenticate_refresh_token(refresh_token)
        token = OAuth2Token.query.filter_by(refresh_token=refresh_token).first()
        if token is not None and token.is_refresh_token_active():
            return token

    def authenticate_user(self, credential: OAuth2Token):
        # return super().authenticate_user(credential)
        return Account.query.get(credential.user_id)

    def _validate_request_token(self, client):
        refresh_token = self.request.args.get('refresh_token')
        if refresh_token is None:
            raise InvalidRequestError('Missing "refresh_token" in request.')

        token = self.authenticate_refresh_token(refresh_token)
        if not token or not token.check_client(client):
            raise InvalidGrantError()
        return token

    def revoke_old_credential(self, credential):
        """The authorization server MAY revoke the old refresh token after
        issuing a new refresh token to the client. Developers MUST implement
        this method in subclass::

            def revoke_old_credential(self, credential):
                credential.revoked = True
                credential.save()

        :param credential: Token object
        """
        # credential.revoked = True
        # credential.save()
        # try:
        credential.refresh_token_revoked_at = round(time.time())
        db.session.add(credential)
        db.session.commit()
        # except Exception as e:
        #     print("&" * 50)
        #     print(e)
        # print("&" * 50)
        # print(credential.is_revoked())


def authenticate_none(query_client, request):
    """Authenticate public client by ``none`` method, it means
       client id and client secret are in url's query parameters.
    """
    client_id = request.args.get("client_id", None)
    client_secret = request.args.get("client_secret", None)
    if client_id and client_secret:
        client = _validate_client(query_client, client_id, request.state)
        if client.check_client_secret(client_secret):
            # log.debug(f'Authenticate {client_id} via "none" success')
            return client
    # log.debug(f'Authenticate {client_id} via "none" failed')


class ClientAuthentication(BaseClientAuthentication):

    def __init__(self, query_client):
        super().__init__(query_client)
        self._methods['none'] = authenticate_none


class AuthorizationServer(BaseAuthorizationServer):

    def authenticate_client(self, request, methods, endpoint='token'):
        """Authenticate client via HTTP request information with the given
        methods, such as ``client_secret_basic``, ``client_secret_post``.
        """
        if self._client_auth is None and self.query_client:
            self._client_auth = ClientAuthentication(self.query_client)
        client = self._client_auth(request, methods, endpoint)
        return client

    def create_token_response(self, request=None):
        """Validate token request and create token response.

        :param request: HTTP request instance
        """
        request = self.create_oauth2_request(request)
        try:
            grant = self.get_token_grant(request)
        except UnsupportedGrantTypeError as error:
            return self.handle_error_response(request, error)

        try:
            grant.validate_token_request()
            args = grant.create_token_response()
            return self.handle_response(*args)
        except OAuth2Error as error:
            return self.handle_error_response(request, error)


def generate_access_token(grant_type, client, user=None, scope=None,
                          expires_in=None, include_refresh_token=True):
    username = user.username
    token_type = "bearer"
    authorities = [
        "ROLE_USER",
        "ROLE_ADMIN"
    ]
    # 生成访问令牌
    access_token_id = str(uuid.uuid1())
    access_token_expires_in = round(time.time()) + current_app.config["OAUTH2_ACCESS_TOKEN_EXPIRED_TIME"]
    access_token_payload = dict(
        username=username,
        user_name=username,
        scope=["ALL"],
        exp=access_token_expires_in,
        authorities=authorities,
        client_id=current_app.config["OAUTH2_CLIENT_ID"],
        jti=access_token_id
    )
    access_token = jwt.encode(
        payload=access_token_payload,
        key=current_app.config["JWT_SIGNATURE_KEY"],  # JWT_SIGATURE_KEY
        algorithm="HS256"
    )
    if include_refresh_token:
        # 生成刷新令牌
        refresh_token_id = str(uuid.uuid1())
        refresh_token_expires_in = round(time.time()) + current_app.config["OAUTH2_REFRESH_TOKEN_EXPIRED_TIME"]
        refresh_token_payload = dict(
            username=username,
            user_name=username,
            scope=["ALL"],
            # scope=scope,
            ati=access_token_id,
            exp=current_app.config["OAUTH2_REFRESH_TOKEN_EXPIRED_TIME"],
            authorities=authorities,
            jti=refresh_token_id,
            client_id=current_app.config["OAUTH2_CLIENT_ID"],
        )
        refresh_token = jwt.encode(
            payload=refresh_token_payload,
            key=current_app.config["JWT_SIGNATURE_KEY"],
            algorithm="HS256"
        )
    else:
        refresh_token = None
    token = dict(
        jti=access_token_id,
        username=username,
        token_type=token_type,
        access_token=access_token,
        refresh_token=refresh_token,
        scope="ALL",
        authorities=authorities,
        expires_in=access_token_expires_in,
        refresh_token_expires_in=refresh_token_expires_in
    )
    return token


def save_token(token_data, request):
    if request.user:
        user_id = request.user.get_user_id()
    else:
        # client_credentials grant_type
        user_id = request.client.user_id
        # or, depending on how you treat client_credentials
        user_id = None
    token = OAuth2Token(
        client_id=request.client.client_id,
        user_id=user_id,
        # **token_data
        token_type=token_data.get("token_type", None),
        access_token=token_data.get("access_token", None),
        refresh_token=token_data.get("refresh_token", None),
        scope=token_data.get("scope", None),
        issued_at=round(time.time()),
        expires_in=token_data.get("expires_in", 0),
        # access_token_revoked_at=token_data.get("expires_in", 0),
        # refresh_token_revoked_at=token_data.get("refresh_token_expires_in", 0)
        access_token_revoked_at=0,
        refresh_token_revoked_at=0
    )
    db.session.add(token)
    db.session.commit()


query_client = create_query_client_func(db.session, OAuth2Client)
# save_token = create_save_token_func(db.session, OAuth2Token)
authorization_server = AuthorizationServer(
    query_client=query_client,
    save_token=save_token
)
require_oauth2 = ResourceProtector()


# class BearerTokenValidator(BaseBearerTokenValidator):

#     def authenticate_token(self, token_string):
#         # return super().authenticate_token(token_string)
#         token = OAuth2Token.query.filter_by(access_token=token_string).first()
#         return token


def register_oauth2(app: Flask):
    authorization_server.init_app(app=app)

    # support password grant and refresh token grant:
    authorization_server.register_grant(PasswordGrant)
    authorization_server.register_grant(RefreshTokenGrant)

    # support cumstomize token generator:
    authorization_server.register_token_generator("default", generate_access_token)

    # protect resource
    bearer_cls = create_bearer_token_validator(db.session, OAuth2Token)
    require_oauth2.register_token_validator(bearer_cls())
    # require_oauth2.register_token_validator(BearerTokenValidator)