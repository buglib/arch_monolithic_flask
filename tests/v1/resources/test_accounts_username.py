import pytest as pt

from api.v1.models import db, Account
from tests.fixtures import testing_app_and_client


@pt.mark.usefixtures("testing_app_and_client")
class TestAccountsUsernameResource:

    def test_return_200(self, testing_app_and_client):
        _, client = testing_app_and_client
        user = Account(
            username="Messi",
            password="123",
            email="leomessi@gmail.com",
            telephone="10101010101"
        )
        db.session.add(user)
        db.session.commit()

        resp = client.get("/v1/accounts/Messi")
        assert resp.status_code == 200
        assert resp.json["username"] == "Messi"
        assert resp.json["name"] is None
        assert resp.json["email"] == "leomessi@gmail.com"
        assert resp.json["telephone"] == "10101010101"
        assert resp.json["location"] is None
        assert resp.json["avatar"] is None

    def test_return_404(self, testing_app_and_client):
        _, client = testing_app_and_client
        resp = client.get("/v1/accounts/Luccy")
        assert resp.status_code == 404
        assert resp.json["code"] == -1
        assert resp.json["message"] == "按用户名查找用户失败，即用户不存在"
