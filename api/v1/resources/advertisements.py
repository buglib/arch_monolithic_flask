# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import jsonify

from . import Resource
from ..models import Advertisement


class Advertisements(Resource):

    def get(self):
        # advs = Advertisement.query().all()
        # advs = Advertisement.query.all()
        q = Advertisement.query
        # print(q)
        advs = q.all()
        respBody = []
        for adv in advs:
            obj = dict(
                id=adv.id,
                image=adv.image,
                productId=adv.product_id
            )
            respBody.append(obj)
        resp = jsonify(respBody)
        return resp