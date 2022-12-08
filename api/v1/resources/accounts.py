# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
import time

from flask import current_app, g

from . import Resource
from ..models import db, Account, Oauth2Client


class Accounts(Resource):

    def post(self):
        # print(g.json)
        username = g.json["username"]
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
                password=g.json["password"],
                email=g.json["email"],
                telephone=g.json["telephone"]
            )
            db.session.add(user)
            db.session.commit()
            # 关联认证用到的客户端信息
            client = Oauth2Client(
                client_id=current_app.config["OAUTH2_CLIENT_ID"],
                client_secret=current_app.config["OAUTH2_CLIENT_SECRET"],
                client_id_issued_at=time.time(),
                client_secret_expires_at=0,
                user_id=user.id
            )
            db.session.add(client)
            db.session.commit()
            resp_body = dict(
                code=0,
                message="操作成功"
            )
            # status_code = 200
        return resp_body, 200
