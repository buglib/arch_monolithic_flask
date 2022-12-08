from pprint import pprint
from unittest import TestCase

import pytest as pt

from api.v1.models import db, Account, Oauth2Token
from tests.fixtures import api_test_client


@pt.mark.usefixtures("api_test_client")
class OauthTokenTestCase(TestCase):

    def test_with_username_and_password(self):
        # 先新建一个用户
        user = Account(
            username="Messi",
            password="123",
            email="leomessi@gmail.com",
            telephone="10101010101"
        )
        db.session.add(user)
        db.session.commit()

        request_params = dict(
            username=user.username,
            password=user.password,
            grant_type="password",
            client_id=self.app.config["OAUTH2_CLIENT_ID"],
            client_secret=self.app.config["OAUTH2_CLIENT_SECRET"]
        )
        url = "/v1/oauth/token?username={username}&password={password}&grant_type={grant_type}&client_id={client_id}&client_secret={client_secret}".format(**request_params)
        resp = self.client.get(url)
        # print("-" * 50)
        # print(url)
        # pprint(resp.json)
        # print("-" * 50)
        assert resp.status_code == 200
        assert resp.json["username"] == "Messi"
        assert resp.json["token_type"] == "bearer"
        assert resp.json["authorities"] == ["ROLE_USER", "ROLE_ADMIN"]
        assert resp.json["scope"] == "ALL"

    def test_with_refresh_token(self):
        # 先创建一个新用户
        user = Account(
            username="James",
            password="123",
            email="james@gmail.com",
            telephone="10101010101"
        )
        db.session.add(user)
        db.session.commit()

        # 接着为该用户关联令牌
        request_params = dict(
            username=user.username,
            password=user.password,
            grant_type="password",
            client_id=self.app.config["OAUTH2_CLIENT_ID"],
            client_secret=self.app.config["OAUTH2_CLIENT_SECRET"]
        )
        url = "/v1/oauth/token?username={username}&password={password}&grant_type={grant_type}&client_id={client_id}&client_secret={client_secret}".format(**request_params)
        resp = self.client.get(url)
        assert resp.status_code == 200
        refresh_token = resp.json["refresh_token"]

        # 然后使用刷新令牌获取访问令牌
        request_params.pop("username")
        request_params.pop("password")
        request_params["refresh_token"] = refresh_token
        url = "/v1/oauth/token?refresh_token={refresh_token}&grant_type={grant_type}&client_id={client_id}&client_secret={client_secret}".format(**request_params)
        resp = self.client.get(url)
        assert resp.status_code == 200

    def test_user_not_found(self):
        request_params = dict(
            username="Neymar",
            password="123",
            grant_type="password",
            client_id=self.app.config["OAUTH2_CLIENT_ID"],
            client_secret=self.app.config["OAUTH2_CLIENT_SECRET"]
        )
        url = "/v1/oauth/token?username={username}&password={password}&grant_type={grant_type}&client_id={client_id}&client_secret={client_secret}".format(**request_params)
        resp = self.client.get(url)
        expected = dict(
            status="Fail to get access token",
            message="User '%s' not found" % "Neymar"
        )
        assert resp.status_code == 404
        assert resp.json == expected
        # pprint(resp.json)

    def test_invalid_client_id(self):
        user = Account(
            username="CR7",
            password="123",
            email="cr7@gmail.com",
            telephone="10101010101"
        )
        db.session.add(user)
        db.session.commit()

        request_params = dict(
            username="CR7",
            password="123",
            grant_type="password",
            client_id="CR7",
            client_secret=self.app.config["OAUTH2_CLIENT_SECRET"]
        )
        url = "/v1/oauth/token?username={username}&password={password}&grant_type={grant_type}&client_id={client_id}&client_secret={client_secret}".format(**request_params)
        resp = self.client.get(url)
        expected = dict(
                status="Fail to get access token",
                message="Invalid client id for user '%s'" % "CR7"
            )
        # pprint(resp.json)
        assert resp.status_code == 400
        assert resp.json == expected

    def test_invalid_client_secret(self):
        user = Account(
            username="Kobe",
            password="123",
            email="Kobe@gmail.com",
            telephone="10101010101"
        )
        db.session.add(user)
        db.session.commit()

        request_params = dict(
            username="Kobe",
            password="123",
            grant_type="password",
            client_id=self.app.config["OAUTH2_CLIENT_ID"],
            client_secret="123"
        )
        url = "/v1/oauth/token?username={username}&password={password}&grant_type={grant_type}&client_id={client_id}&client_secret={client_secret}".format(**request_params)
        resp = self.client.get(url)
        expected = dict(
                status="Fail to get access token",
                message="Invalid client secret for user '%s'" % "Kobe"
            )
        # pprint(resp.json)
        assert resp.status_code == 400
        assert resp.json == expected

    def test_invalid_refresh_token(self):
        # 先创建一个新用户
        user = Account(
            username="Bob",
            password="123",
            email="bob@gmail.com",
            telephone="10101010101"
        )
        db.session.add(user)
        db.session.commit()

        # 接着为该用户关联令牌
        request_params = dict(
            username=user.username,
            password=user.password,
            grant_type="password",
            client_id=self.app.config["OAUTH2_CLIENT_ID"],
            client_secret=self.app.config["OAUTH2_CLIENT_SECRET"]
        )
        url = "/v1/oauth/token?username={username}&password={password}&grant_type={grant_type}&client_id={client_id}&client_secret={client_secret}".format(**request_params)
        resp = self.client.get(url)
        assert resp.status_code == 200
        refresh_token = "123"

        # 然后使用刷新令牌获取访问令牌
        request_params.pop("username")
        request_params.pop("password")
        request_params["refresh_token"] = refresh_token
        url = "/v1/oauth/token?refresh_token={refresh_token}&grant_type={grant_type}&client_id={client_id}&client_secret={client_secret}".format(**request_params)
        resp = self.client.get(url)
        assert resp.status_code == 400
        # pprint(resp.json)