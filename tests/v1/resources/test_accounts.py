from pprint import pprint
from unittest import TestCase

import pytest as pt

from api.v1.models import db, Account
from tests.fixtures import (
    testing_app_and_client,
    testing_user_and_tokens,
)


@pt.mark.usefixtures("testing_user_and_tokens")
@pt.mark.usefixtures("testing_app_and_client")
class TestAccountsResource:

    def test_post_return_200(self, testing_app_and_client):
        _, client = testing_app_and_client
        jsonData = dict(
            username="buglib",
            password="123456",
            email="buglib@foxmail.com",
            telephone="12345678912"
        )
        resp = client.post("/v1/accounts", json=jsonData)
        # pprint(resp.json)
        assert resp.status_code == 200
        assert resp.json["code"] == 0 and resp.json["message"] == "操作成功"

    def test_post_return_400(self, testing_app_and_client):
        _, client = testing_app_and_client
        user = Account(
            username="Messi",
            password="123",
            email="leomessi@gmail.com",
            telephone="10101010101"
        )
        db.session.add(user)
        db.session.commit()

        jsonData = dict(
            username="Messi",
            password="123456",
            email="buglib@foxmail.com",
            telephone="12345678912"
        )
        resp = client.post("/v1/accounts", json=jsonData)
        assert resp.status_code == 400
        assert resp.json["code"] == -1 and resp.json["message"] == "操作失败，用户已存在"

    def test_put_return_401(self, testing_app_and_client):
        _, client = testing_app_and_client
        user = Account(
            username="Alice",
            password="123",
            email="alice@gmail.com",
            telephone="10101010101"
        )
        db.session.add(user)
        db.session.commit()

        jsonData = dict(
            id=user.id,
            username="Alice",
            email="alice@foxmail.com",
            telephone="12345678912"
        )
        resp = client.put("/v1/accounts", json=jsonData)
        assert resp.status_code == 401

    def test_put_return_200(self, testing_app_and_client, testing_user_and_tokens):
        _, client = testing_app_and_client
        headers, data, access_token, _ = testing_user_and_tokens
        # headers = {"Authorization": "bearer %s" % access_token}
        resp = client.put(
            "/v1/accounts", 
            json=data,
            headers=headers
        )
        # print("")
        # print(headers["Authorization"])
        # pprint(resp)
        assert resp.status_code == 200