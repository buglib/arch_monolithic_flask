# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import jsonify

from . import Resource
from ..models import Product


class Products(Resource):

    def get(self):
        prods = Product.query.all()
        respBody = []
        for prod in prods:
            specs = []
            for spec in prod.specifications:
                specs.append(
                    dict(
                        id=spec.id,
                        item=spec.item,
                        value=spec.value
                    )
                )
            respBody.append(
                dict(
                    id=prod.id,
                    title=prod.title,
                    price=float(prod.price),  # 这里必须转换为float类型，不然前端js报错：e.price.toFixed is not a function
                    rate=float(prod.rate),
                    description=prod.description,
                    cover=prod.cover,
                    detail=prod.detail,
                    specifications=specs
                )
            )
        resp = jsonify(respBody)
        resp.content_encoding = "utf-8"
        return resp