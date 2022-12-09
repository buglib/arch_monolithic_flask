# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g

from . import Resource
from ..models import Account


class AccountsUsername(Resource):

    def get(self, username):
        user = Account.query.filter_by(username=username).first()
        if not user:
            resp_body = dict(
                code=-1,
                message="按用户名查找用户失败，即用户不存在"
            )
            status_code = 404
        else:
            resp_body = dict(
                id=user.id,
                username=user.username,
                name=user.name,
                email=user.email,
                telephone=user.telephone,
                location=user.location,
                avatar=user.avatar
            )
            status_code = 200
        return resp_body, status_code, None