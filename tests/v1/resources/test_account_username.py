from unittest import TestCase

import pytest as pt

from api.v1.models import db, Account
from tests.fixtures import api_test_client


@pt.mark.usefixtures("api_test_client")
class AccountUsernameTestCase(TestCase):

    def test_return_200(self):
        user = Account(
            username="Messi",
            password="123",
            email="leomessi@gmail.com",
            telephone="10101010101"
        )
        db.session.add(user)
        db.session.commit()

        resp = self.client.get("/v1/account/Messi")
        assert resp.status_code == 200
        assert resp.json["username"] == "Messi"
        assert resp.json["name"] is None
        assert resp.json["email"] == "leomessi@gmail.com"
        assert resp.json["telephone"] == "10101010101"
        assert resp.json["location"] is None
        assert resp.json["avatar"] is None

    def test_return_404(self):
        resp = self.client.get("/v1/account/messi")
        assert resp.status_code == 404
        assert resp.json["code"] == -1
        assert resp.json["message"] == "按用户名查找用户失败，即用户不存在"
