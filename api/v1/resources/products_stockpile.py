# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request

from . import Resource
from ..models import (
    db,
    Product,
    Stockpile
)


class ProductsStockpile(Resource):

    def get(self, productId):
        product = Product.query.filter_by(id=productId).first()
        if not product:
            resp_body = dict(
                status="fail",
                message="fail to get stockpile for product '%s', product '%s' may be not found" % (productId, productId)
            )
            status_code = 404
        else:
            stockpile = product.stockpiles[0]
            resp_body = dict(
                id=stockpile.id,
                product_id=stockpile.product_id,
                amount=stockpile.amount,
                frozen=stockpile.frozen
            )
            status_code = 200
        return resp_body, status_code

    def patch(self, productId):
        stockpile = Stockpile.query.filter_by(product_id=productId).first()
        if not stockpile:
            resp_body = dict(
                status="fail",
                message="fail to get stockpile for product '%s', product '%s' may be not found" % (productId, productId)
            )
            status_code = 400
        else:
            json_data = request.json
            try:
                # stockpile(**json_data)
                amount = json_data.get("amount", None)
                frozen = json_data.get("frozen", None)
                if amount:
                    stockpile.amount = amount
                if frozen:
                    stockpile.frozen = frozen
                db.session.add(stockpile)
                db.session.commit()
            except Exception as e:
                resp_body = dict(
                    status="fail",
                    message=str(e)
                )
                status_code = 400
            else:
                resp_body = dict(
                    status="done",
                    message="succeed to update stockpile for product {}".format(productId)
                )
                status_code = 200
            return resp_body, status_code
