# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import jsonify, request

from . import Resource
from ..extensions.oauth2 import require_oauth2
from ..models import db, Product, Specification


class Products(Resource):

    method_decorators = {
        "post": [require_oauth2(scopes="ALL")]
    }

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

    def post(self):
        data = request.json
        title = data.get("title", None)
        price = data.get("price", None)
        rate = data.get("rate", None)
        desc = data.get("description", None)
        cover = data.get("cover", None)
        detail = data.get("detail", None)
        product = Product(
            title=title,
            price=price,
            rate=rate,
            description=desc,
            cover=cover,
            detail=detail
        )
        db.session.add(product)
        db.session.commit()
        resp_body = dict(
            status="done",
            message="Succeed to add new product"
        )
        status_code = 200
        return resp_body, status_code