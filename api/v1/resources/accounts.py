# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import g

from . import Resource
from ..models import db, Account


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
            user = Account(
                username=username,
                password=g.json["password"],
                email=g.json["email"],
                telephone=g.json["telephone"]
            )
            db.session.add(user)
            db.session.commit()
            resp_body = dict(
                code=0,
                message="操作成功"
            )
            # status_code = 200
        return resp_body, 200
