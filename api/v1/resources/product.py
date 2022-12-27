# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import jsonify, request

from . import Resource
# from ..models import Product as ProductModel, Specification
from ..models import (
    db, 
    Product as ProductModel,
    Specification
)


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
            resp_body = dict(
                id=prod.id,
                title=prod.title,
                price=float(prod.price),  # 这里必须转换为float类型，不然前端js报错：e.price.toFixed is not a function
                rate=float(prod.rate),
                description=prod.description,
                cover=prod.cover,
                detail=prod.detail,
                specifications=specs
            )
            return resp_body, 200
        else:
            resp_body = None
            return resp_body, 404

    def put(self, productId):
        data = request.json
        title = data.get("title", None)
        price = data.get("price", None)
        rate = data.get("rate", None)
        desc = data.get("description", None)
        cover = data.get("cover", None)
        detail = data.get("detail", None)

        product = ProductModel(
            title=title,
            price=price,
            rate=rate,
            description=desc,
            cover=cover,
            detail=detail
        )

        specs = data.get("specifications", None)
        for spec in specs:
            specification = Specification(
                item=spec.get("item", None),
                value=spec.get("value", None)
            )
            product.specifications.append(specification)
        
        db.session.add(product)
        db.session.commit()

        resp_body = dict(
            status="done",
            message="Succeed to update product"
        )
        status_code = 200
        return resp_body, status_code

    def delete(self, productId):
        product = ProductModel.query.filter_by(id=productId).first()
        if not product:
            resp_body = dict(
                status="fail",
                message="fail to remove product, because product '%s' not found" % productId
            )
            status_code = 404
        else:
            db.session.delete(product)
            db.session.commit()
            resp_body = dict(
                status="done",
                message="succeed to remove product '%s'" % productId
            )
            status_code = 200
        return resp_body, status_code
        