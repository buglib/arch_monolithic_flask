import pytest as pt

from tests.fixtures import (
    testing_app_and_client,
    testing_user_and_tokens
)


@pt.mark.usefixtures("testing_user_and_tokens")
@pt.mark.usefixtures("testing_app_and_client")
class TestSettlementResource:

    def test_post_return_200(
        self, 
        testing_app_and_client,
        testing_user_and_tokens
    ):
        _, client = testing_app_and_client
        headers, _, _, _ = testing_user_and_tokens
        req_data = {
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
        resp_data_expected = {
            # 'create_time': '2023-01-11 17:19:54',
            'expires': 3,
            # 'id': 1,
            # 'pay_id': "6bd75366-9191-11ed-a431-1e002322ba40",
            'pay_state': 'WAITING',
            'payemnt_link': '/v1/pay/modify/{pay_id}?state=WAITING&accountId=2',
            'total_price': 208.0
        }
        resp = client.post(
            "/v1/settlement",
            json=req_data,
            headers=headers
        )
        assert resp.status_code == 200
        # from pprint import pprint
        # pprint(resp.json)
        resp_data_actual = resp.json
        pay_id = resp_data_actual["pay_id"]
        resp_data_expected["payemnt_link"] = resp_data_expected["payemnt_link"].format(pay_id=pay_id)
        for key in ["create_time", "id", "pay_id"]:
            resp_data_actual.pop(key)
        assert resp_data_actual == resp_data_expected
        
