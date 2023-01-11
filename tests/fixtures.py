import os
import time

import pytest as pt

from api import create_app
from api.v1.models import db


# @pt.fixture(scope="class")
# def api_test_client(request):
#     class TestCaseHook:
#         pass

#     request.cls.app = create_app(configName="test")
#     request.cls.context = request.cls.app.app_context()
#     request.cls.context.push()
#     db.create_all()
#     request.cls.client = request.cls.app.test_client()
#     yield
#     db.session.remove()
#     db.drop_all()
#     request.cls.context.pop()


@pt.fixture(scope="class")
def testing_app_and_client():
    app = create_app(configName="test")
    ctx = app.app_context()
    ctx.push()
    client = app.test_client()
    db.create_all()
    sql_file_path = os.path.join(
        os.path.dirname(app.root_path),
        "db",
        "mysql",
        "data.sql"
    )
    cmd = "mysql -h 127.0.0.1 -P 3306 -u bookstore -pbookstore --default-character-set=utf8 test_bookstore <'%s'" % sql_file_path
    os.system(cmd)
    yield app, client
    time.sleep(3)
    db.session.remove()
    db.drop_all()
    ctx.pop()


@pt.fixture(scope="class")
def testing_user_and_tokens(testing_app_and_client):
    app, client = testing_app_and_client
    user_data = dict(
        username="bookstore",
        password="123456",
        email="bookstore@gmail.com",
        telephone="12345678912"
    )
    resp = client.post("/v1/accounts", json=user_data)
    assert resp.status_code == 200
    # from pprint import pprint
    # pprint(resp.json)

    request_params = dict(
        username=user_data["username"],
        password=user_data["password"],
        grant_type="password",
        client_id=app.config["OAUTH2_CLIENT_ID"],
        client_secret=app.config["OAUTH2_CLIENT_SECRET"]
    )
    url = "/v1/oauth/token?username={username}&password={password}&grant_type={grant_type}&client_id={client_id}&client_secret={client_secret}".format(**request_params)
    resp = client.get(url)
    assert resp.status_code == 200
    # from pprint import pprint
    # pprint(resp.json)
    access_token = resp.json["access_token"]
    refresh_token = resp.json["refresh_token"]
    request_headers = {"Authorization": "bearer %s" % access_token}
    yield request_headers, user_data, access_token, refresh_token


@pt.fixture(scope="class")
def settlement_request_data():
    data = {
        "items": [
            {
                "amount": 1,
                "id": 1
            },
            {
                "amount": 1,
                "id": 6
            }
        ],
        "purchase": {
            "name": "周志明",
            "telephone": "18888888888",
            "delivery": True,
            "address": {
                "province": "广东省",
                "city": "广州市",
                "area": "海珠区"
            },
            "location": "广东省  广州市 海珠区 唐家湾港湾大道科技一路3号远光软件股份有限公司",
            "pay": "wechat",
            "id": 1,
            "username": "icyfenix",
            "avatar": "https://www.gravatar.com/avatar/1563e833e42fb64b41eed34c9b66d723?d=mp",
            "email": "icyfenix@gmail.com"
        }
    }
    yield data