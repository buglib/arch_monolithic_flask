# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import jsonify

from . import Resource
from ..models import Product as ProductModel


class Product(Resource):

    def get(self, productId):
        prod = ProductModel.query.filter_by(id=productId).first()
        if prod:
            specs = []
            for spec in prod.specifications:
                specs.append(
                    dict(
                        id=spec.id,
                        item=spec.item,
                        value=spec.value
                    )
                )
            respBody = dict(
                id=prod.id,
                title=prod.title,
                price=float(prod.price),  # 这里必须转换为float类型，不然前端js报错：e.price.toFixed is not a function
                rate=float(prod.rate),
                description=prod.description,
                cover=prod.cover,
                detail=prod.detail,
                specifications=specs
            )
            resp = jsonify(respBody)
            return resp
        else:
            respBody = None
            return respBody, 404
        