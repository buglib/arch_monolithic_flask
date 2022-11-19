from unittest import TestCase

from api import create_app, db
from api.v1.models import db, Account


class AccountsTestCase(TestCase):

    def setUp(self) -> None:
        self.app = create_app(configName="test")
        self.context = self.app.app_context()
        self.context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
        self.context.pop()

    def testReturn200(self):
        jsonData = dict(
            username="buglib",
            password="123456",
            email="buglib@foxmail.com",
            telephone="12345678912"
        )
        resp = self.client.post("/v1/accounts", json=jsonData)
        assert resp.status_code == 200
        assert resp.json["code"] == 0 and resp.json["message"] == "操作成功"

    def testReturn400(self):
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

