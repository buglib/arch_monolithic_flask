# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
import time
import uuid

from flask import current_app, request
import jwt

from . import Resource
from ..models import db, Account, Oauth2Token


class OauthToken(Resource):

    def get(self):
        username = request.args.get("username", None)
        password = request.args.get("password", None)
        grant_type = request.args.get("grant_type", None)
        client_id = request.args.get("client_id", None)
        client_secret = request.args.get("client_secret", None)
    
        user = Account.query.filter_by(username=username).first()
        if not user:
            resp_body = dict(
                status="Fail to get access token",
                message="User '%s' not found" % username
            )
            status_code = 404
        elif not user.check_password(password=password):
            resp_body = dict(
                status="Fail to get access token",
                message="Invalid password for user '%s'" % username
            )
        elif grant_type != "password":
            resp_body = dict(
                status="Fail to get access token",
                message="Grant type must be password"
            )
            status_code = 400
        elif client_id != current_app.config["OAUTH2_CLIENT_ID"]:
            resp_body = dict(
                status="Fail to get access token",
                message="Invalid client id for user '%s'" % username
            )
            status_code = 400
        elif client_secret != current_app.config["OAUTH2_CLIENT_SECRET"]:
            resp_body = dict(
                status="Fail to get access token",
                message="Invalid client secret for user '%s'" % username
            )
            status_code = 400
        else:
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
            refresh_token_id = str(uuid.uuid1())
            refresh_token_expires_in = round(time.time()) + current_app.config["OAUTH2_REFRESH_TOKEN_EXPIRED_TIME"]
            refresh_token_payload = dict(
                username=username,
                user_name=username,
                scope=["ALL"],
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
            resp_body = dict(
                jti=access_token_id,
                username=username,
                token_type=token_type,
                access_token=access_token,
                refresh_token=refresh_token,
                scope="ALL",
                authorities=authorities,
                expires_in=access_token_expires_in
            )
            # 将上面两个令牌保存到数据库
            token_record = Oauth2Token(
                client_id=client_id,
                token_type=token_type,
                access_token=access_token,
                refresh_token=refresh_token,
                scope="ALL",
                issued_at=time.time(),
                access_token_revoked_at=access_token_expires_in,
                refresh_token_revoked_at=refresh_token_expires_in,
                expires_in=access_token_expires_in,
                user_id=user.id
            )
            db.session.add(token_record)
            try:
                db.session.commit()
            except Exception as e:
                print(e)
                SystemExit()
            status_code = 200
        return resp_body, status_code

