# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
from datetime import datetime

from authlib.integrations.flask_oauth2 import current_token
from flask import current_app, request

from . import Resource
from ..dtos import SettlementDTO
from ..errors import ArchMonolithicFlaskError
from ..extensions.oauth2 import require_oauth2
from ..services import SettlementService


class Settlement(Resource):

    method_decorators = [require_oauth2(scopes="ALL")]

    def post(self):
        json_data = request.json
        user = current_token.user
        dto = SettlementDTO()
        dto.from_dict(data=json_data)
        service = SettlementService(
            flask_app=current_app._get_current_object(),
            user_id=user.id,
            default_product_frozen_expires=current_app.config["DEFAULT_PRODUCT_FROZEN_EXPIRES"]
        )
        try:
            payment = service.generate(settlement_dto=dto)
        except ArchMonolithicFlaskError as e:
            status_code = e
            resp_body = dict(
                code=1,
                message=e.message
            )
        else:
            status_code = 200
            resp_body = dict(
                id=payment.id,
                pay_id=payment.pay_id,
                # create_time=datetime.utcfromtimestamp(payment.create_time.timestamp()),
                create_time=str(payment.create_time),
                total_price=float(payment.total_price),
                expires=payment.expires,
                payemnt_link=payment.payment_link,
                pay_state=payment.pay_state
            )
        return resp_body, status_code