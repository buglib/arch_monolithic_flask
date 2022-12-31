# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
import json
import time

from authlib.integrations.flask_oauth2 import current_token
from flask import current_app, g, request

from . import Resource
from ..extensions.oauth2 import require_oauth2
from ..models import (
    db,
    Account,
    OAuth2Client
)


class Accounts(Resource):

    method_decorators = {
        "put": [require_oauth2(scopes="ALL")]
    }

    def post(self):
        # print(g.json)
        # username = g.json["username"]
        username = request.json["username"]
        user = Account.query.filter_by(username=username).first()
        if user:
            resp_body = dict(
                code=-1,
                message="操作失败，用户已存在"
            )
            # status_code = 400
            return resp_body, 400
        else:
            # 新建用户
            user = Account(
                username=username,
                password=request.json["password"],
                email=request.json["email"],
                telephone=request.json["telephone"]
            )
            db.session.add(user)
            db.session.commit()
            # 关联认证用到的客户端信息
            client_metadata = json.dumps(
                obj={
                    "token_endpoint_auth_method": "none",
                    "grant_types": ["password", "refresh_token"],
                    "scope": "ALL"
                },
                ensure_ascii=False
            )
            client = OAuth2Client(
                client_id=current_app.config["OAUTH2_CLIENT_ID"],
                client_secret=current_app.config["OAUTH2_CLIENT_SECRET"],
                client_id_issued_at=time.time(),
                client_secret_expires_at=0,
                user_id=user.id,
                _client_metadata=client_metadata
            )
            db.session.add(client)
            db.session.commit()
            resp_body = dict(
                code=0,
                message="操作成功"
            )
            # status_code = 200
        return resp_body, 200

    def put(self):
        user_id = request.json.get("id", None)
        username = request.json.get("username", None)
        email = request.json.get("email", None)
        telephone = request.json.get("telephone", None)
        name = request.json.get("name", None)
        avatar = request.json.get("avatar", None)
        location = request.json.get("location", None)

        # user = Account.query.filter_by(id=user_id).first()
        # if not user:
        #     user = Account.query.filter_by(username=username).first()
        user = current_token.user
        if user:
            user.username = username
            user.email = email
            user.telephone = telephone
            user.name = name
            user.avatar = avatar
            user.location = location
            db.session.add(user)
            db.session.commit()
        resp_body = dict(
            status="done",
            message="Succeed to update user '%s'" % username
        )
        status_code = 200
        return resp_body, status_code