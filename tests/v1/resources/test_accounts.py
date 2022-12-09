from unittest import TestCase

import pytest as pt

from api.v1.models import db, Account
from tests.fixtures import api_test_client


@pt.mark.usefixtures("api_test_client")
class AccountsTestCase(TestCase):

    def test_get_return_200(self):
        jsonData = dict(
            username="buglib",
            password="123456",
            email="buglib@foxmail.com",
            telephone="12345678912"
        )
        resp = self.client.post("/v1/accounts", json=jsonData)
        assert resp.status_code == 200
        assert resp.json["code"] == 0 and resp.json["message"] == "操作成功"

    def test_get_return_400(self):
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
        resp = self.client.post("/v1/accounts", json=jsonData)
        assert resp.status_code == 400
        assert resp.json["code"] == -1 and resp.json["message"] == "操作失败，用户已存在"

    def test_put_return_200(self):
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
        resp = self.client.put("/v1/accounts", json=jsonData)
        assert resp.status_code == 200