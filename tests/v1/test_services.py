import time
import pytest as pt

from api.v1.dtos import SettlementDTO
from api.v1.errors import (
    ArchMonolithicFlaskError,
    ModelObjectNotFoundError,
    OversellError,
    WithoutCheckingRequiredProductsError
)
from api.v1.extensions.cache import cache
from api.v1.models import (
    db,
    Stockpile,
    Product,
    PaymentState,
    Payment
)
from api.v1.services import (
    PaymentService,
    ProductService,
    SettlementService,
    StockpileService
)
from tests.fixtures import (
    testing_app_and_client,
    settlement_request_data
)


@pt.fixture(scope="class")
def payment_service():
    service = PaymentService(user_id=1)
    yield service


@pt.fixture(scope="class")
def product_service():
    service = ProductService()
    yield service


@pt.fixture(scope="class")
def settlement_service(testing_app_and_client):
    app, _ = testing_app_and_client
    service = SettlementService(
        flask_app=app,
        user_id=1,
        default_product_frozen_expires=3
    )
    yield service


@pt.fixture(scope="class")
def stockpile_service():
    service = StockpileService()
    yield service


@pt.fixture(scope="function")
def settlement_dto(settlement_request_data):
    dto = SettlementDTO()
    dto.from_dict(data=settlement_request_data)
    yield dto


@pt.fixture(scope="function")
def settlment_dto_after_computing_total_price(product_service, settlement_dto):
    product_service.check_required_products(settlement_dto)
    product_service.compute_total_price(settlement_dto)
    yield settlement_dto


@pt.fixture(scope="function")
def payment(settlment_dto_after_computing_total_price):
    payment_service = PaymentService(
        user_id=1,
        default_product_frozen_expires=3
    )
    payment = payment_service.generate(settlment_dto_after_computing_total_price)
    yield payment


@pt.mark.usefixtures("testing_app_and_client")
class TestPaymentService:
    
    def test_generate(self, payment_service, settlment_dto_after_computing_total_price):
        payment = payment_service.generate(settlment_dto_after_computing_total_price)
        data_expected = {
            # "id": 1,
            # "createTime": "2023-01-01T09:25:30.843+0000",
            # "payId": "c862e362-98bb-4ef6-b49c-d3ce896db4fa",
            "totalPrice": 208,
            "expires": 120,
            "paymentLink": "/v1/pay/modify/{pay_id}?state=WAITING&accountId=1",
            "payState": "WAITING"
        }
        assert payment.total_price == data_expected["totalPrice"]
        assert payment.expires == data_expected["expires"]
        assert payment.payment_link == data_expected["paymentLink"].format(pay_id=payment.pay_id)
        assert payment.pay_state == data_expected["payState"]


@pt.mark.usefixtures("testing_app_and_client")
class TestProductService:
    
    def test_check_required_products_successfully(self, product_service, settlement_dto):
        assert not hasattr(settlement_dto, "products")
        product_service.check_required_products(settlement_dto)
        assert hasattr(settlement_dto, "products")

    def test_check_required_products_raise_model_object_not_found_error(self, product_service):
        data = {
            "items": [
                {
                    "amount": 1,
                    "id": 1000
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
        dto = SettlementDTO()
        dto.from_dict(data=data)
        with pt.raises(ModelObjectNotFoundError) as e:
            product_service.check_required_products(dto)
            assert e.message == "Product identified by '%s' is not found" % 1000

    def test_compute_total_price_successfully(self, product_service, settlement_dto):
        assert not hasattr(settlement_dto, "total_price")
        product_service.check_required_products(settlement_dto)
        product_service.compute_total_price(settlement_dto)
        assert hasattr(settlement_dto, "total_price")

    def test_compute_total_price_raise_without_checking_required_products_error(self, product_service, settlement_dto):
        with pt.raises(WithoutCheckingRequiredProductsError) as e:
            product_service.compute_total_price(settlement_dto)
            assert e.message == "without checking required products"


@pt.mark.usefixtures("testing_app_and_client")
class TestSettlementService:

    # def test_accomplish_sucessfully_when_pay_state_is_timeout(
    #     self, 
    #     settlement_service, 
    #     payment,
    #     settlment_dto_after_computing_total_price
    # ):
    #     cache.set(
    #         payment.pay_id, 
    #         settlment_dto_after_computing_total_price
    #     )
    #     settlement_service.accomplish(
    #         pay_state=PaymentState.TIMEOUT.name,
    #         pay_id=payment.pay_id
    #     )
    #     assert payment.pay_state == PaymentState.TIMEOUT.name

    def test_accomplish_raise_arch_monolithic_flask_error(self):
        pass

    def test_accomplish_raise_model_object_not_found_error(self):
        pass

    def test_setup_timeout_trigger(
        self,
        settlement_service, 
        payment,
        settlment_dto_after_computing_total_price
    ):
        cache.set(
            payment.pay_id, 
            settlment_dto_after_computing_total_price
        )
        assert payment.pay_state == PaymentState.WAITING.name
        settlement_service.setup_timeout_trigger(payment)
        time.sleep(5)
        db.session.commit()
        current_payment = Payment.query.filter_by(pay_id=payment.pay_id).first()
        assert current_payment.pay_state == PaymentState.TIMEOUT.name

    def test_setup_timeout_trigger_raise_model_object_not_found_error(self):
        pass

    def test_generate(self, settlement_service, settlement_dto):
        payment = settlement_service.generate(settlement_dto)
        data_expected = {
            # "id": 1,
            # "createTime": "2023-01-01T09:25:30.843+0000",
            # "payId": "c862e362-98bb-4ef6-b49c-d3ce896db4fa",
            "totalPrice": 208,
            "expires": 3,
            "paymentLink": "/v1/pay/modify/{pay_id}?state=WAITING&accountId=1",
            "payState": "WAITING"
        }
        assert payment.total_price == data_expected["totalPrice"]
        assert payment.expires == data_expected["expires"]
        assert payment.payment_link == data_expected["paymentLink"].format(pay_id=payment.pay_id)
        assert payment.pay_state == data_expected["payState"]
        time.sleep(5)
        db.session.commit()
        current_payment = Payment.query.filter_by(pay_id=payment.pay_id).first()
        assert current_payment is not None
        assert current_payment.pay_state == PaymentState.TIMEOUT.name


@pt.mark.usefixtures("testing_app_and_client")
class TestStockpileService:

    def test_decrease(self, stockpile_service):
        product_id = 1
        amount = 2
        service = stockpile_service
        stock_before_decreasing = Stockpile.query.filter_by(product_id=product_id).first()
        assert stock_before_decreasing is not None
        amount_before = stock_before_decreasing.amount
        stock_before_decreasing.amount -= amount
        stock_before_decreasing.frozen += amount
        frozen_before = stock_before_decreasing.frozen
        db.session.add(stock_before_decreasing)
        db.session.commit()
        service.decrease(product_id, amount)
        stock_after_decreasing = Stockpile.query.filter_by(product_id=product_id).first()
        amount_after = stock_after_decreasing.amount
        frozen_after = stock_after_decreasing.frozen
        assert amount_after == amount_before - amount
        assert frozen_after == frozen_before - amount

    def test_freeze(self, stockpile_service):
        product_id = 1
        amount = 2
        product = Product.query.filter_by(id=product_id).first()
        assert product is not None
        stock = product.stockpile
        amount_before = stock.amount
        frozen_before = stock.frozen
        stockpile_service.freeze(product, amount)
        amount_after = stock.amount
        frozen_after = stock.frozen
        assert amount_after == amount_before - amount
        assert frozen_after == frozen_before + amount

    def test_thaw(self, stockpile_service):
        product_id = 1
        amount = 2
        product = Product.query.filter_by(id=product_id).first()
        assert product is not None
        stock = product.stockpile
        stock.freeze(amount)
        amount_before = stock.amount
        frozen_before = stock.frozen
        stockpile_service.thaw(product_id, amount)
        amount_after = stock.amount
        frozen_after = stock.frozen
        assert amount_after == amount_before + amount
        assert frozen_after == frozen_before - amount
