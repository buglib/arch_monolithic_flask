from pprint import pprint

import pytest as pt

from api.v1.dtos import *


class TestSettlementDTO:

    def test_from_dict_and_to_dict(self):
        settlement_req_param = {
            "items": [
                {
                    "amount": 1,
                    "id": 1
                },
                {
                    "amount": 1,
                    "id": 6
                }
            ],
            "purchase": {
                "name": "周志明",
                "telephone": "18888888888",
                "delivery": True,
                "address": {
                    "province": "广东省",
                    "city": "广州市",
                    "area": "海珠区"
                },
                "location": "广东省  广州市 海珠区 唐家湾港湾大道科技一路3号远光软件股份有限公司",
                "pay": "wechat",
                "id": 1,
                "username": "icyfenix",
                "avatar": "https://www.gravatar.com/avatar/1563e833e42fb64b41eed34c9b66d723?d=mp",
                "email": "icyfenix@gmail.com"
            }
        }
        settlement_dto = SettlementDTO()
        settlement_dto.from_dict(data=settlement_req_param)
        
        data = settlement_dto.to_dict()
        assert data == settlement_req_param