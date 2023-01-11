from threading import Timer
import time
import uuid

from flask import Flask

from .errors import (
    ArchMonolithicFlaskError,
    ModelObjectNotFoundError,
    WithoutCheckingRequiredProductsError
)
from .extensions.cache import cache
from .dtos import SettlementDTO
from .models import (
    db,
    Payment, 
    PaymentState,
    Product,
    Stockpile
)


class PaymentService:

    def __init__(
        self, 
        user_id: int,
        default_product_frozen_expires: int = 2 * 60, # 2分钟，使用微秒表示
        payment_link_pattern: str = "/v1/pay/modify/{pay_id}?state={state}&accountId={account_id}"
    ) -> None:
        self.user_id = user_id
        self.default_product_frozen_expires = default_product_frozen_expires
        self.payment_link_pattern = payment_link_pattern

    def generate(self, settlement_dto: SettlementDTO) -> Payment:
        pay_id = str(uuid.uuid1())
        payment_link = self.payment_link_pattern.format(
            pay_id=pay_id,
            state=PaymentState["WAITING"].name,
            account_id=self.user_id
        )
        payment = Payment(
            pay_id=pay_id,
            create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            total_price=settlement_dto.total_price,
            expires=self.default_product_frozen_expires,
            payment_link=payment_link,
            pay_state=PaymentState["WAITING"].name,
            user_id=self.user_id
        )
        db.session.add(payment)
        db.session.commit()
        return payment

    def accomplish(self):
        pass

    def cancel(self):
        pass


class ProductService:

    def __init__(self) -> None:
        self.stockpile_service = StockpileService()

    def check_required_products(self, settlement_dto: SettlementDTO):
        products = dict()  # Dict[product_id, Product]
        for item in settlement_dto.items:
            product = Product.query.filter_by(id=item.product_id).first()
            if not product:
                err_msg = "Product identified by '%s' is not found" % item.product_id
                raise ModelObjectNotFoundError(
                    status_code=404,
                    message=err_msg
                )
            products[item.product_id] = product
        settlement_dto.products = products
        # is_oversell = self.stockpile_service.is_oversell(settlement_dto)
        # if is_oversell:
        #     err_msg = "The required quantities of products is greater than the quantities in stockpile"
        #     raise OversellError(
        #         status_code=400,
        #         message=err_msg
        #     )

    def compute_total_price(self, settlement_dto: SettlementDTO):
        total_price = 0.0
        for item in settlement_dto.items:
            try:
                product = settlement_dto.products[item.product_id]
            except AttributeError:
                err_msg = "without checking required products"
                raise WithoutCheckingRequiredProductsError(
                    status_code=500,
                    message=err_msg
                )
            else:
                self.stockpile_service.freeze(product, item.amount)
                total_price += float(product.price) * item.amount
        settlement_dto.total_price = total_price


class SettlementService:
    """ 订单服务
    """

    def __init__(
        self,
        flask_app: Flask,
        user_id: int,
        default_product_frozen_expires: int = 2 * 60, # 2分钟，使用秒表示
        payment_link_pattern: str = "/v1/pay/modify/{pay_id}?state={state}&accountId={account_id}"
    ) -> None:
        self.app = flask_app
        self.user_id = user_id
        self.product_service = ProductService()
        self.stockpile_service = StockpileService()
        self.payment_service = PaymentService(
            user_id=user_id,
            default_product_frozen_expires=default_product_frozen_expires,
            payment_link_pattern=payment_link_pattern
        )

    def generate(self, settlement_dto: SettlementDTO) -> Payment:
        """ 生成订单 """
        try:
            self.product_service.check_required_products(settlement_dto)
            self.product_service.compute_total_price(settlement_dto)
        except ArchMonolithicFlaskError:
            raise
        else:
            payment = self.payment_service.generate(settlement_dto)
            cache.set(payment.pay_id, settlement_dto)
            self.setup_timeout_trigger(payment)
            return payment

    def accomplish(self, pay_state: str, pay_id: str):
        """ 订单完成 """
        # settlement_dto = self.settlement_dto_cache.get(pay_id, None)
        settlement_dto = cache.get(pay_id)
        if settlement_dto is None:
            raise ArchMonolithicFlaskError(
                status_code=500,
                message="Unknown Error"
            )
        if pay_state == PaymentState.PAYED.name:    
            for item in settlement_dto.items:
                self.stockpile_service.decrease(item.product_id, item.amount)
        else:
            for item in settlement_dto.items:
                self.stockpile_service.thaw(item.product_id, item.amount)
        payment = Payment.query.filter_by(pay_id=pay_id).first()
        if payment is None:
            raise ModelObjectNotFoundError(
                status_code=500,
                message="Payment identified by pay_id '%s' is not found" % pay_id
            )
        payment.pay_state = pay_state
        # try:
        db.session.add(payment)
        db.session.commit()
        # except Exception as e:
        #     print(e)
        return

    def setup_timeout_trigger(self, payment: Payment):
        """ 为订单设置自动超时处理，超时后解冻商品库存 """
        def callback(pay_id: str):
            with self.app.app_context():
                current_payment = Payment.query.filter_by(pay_id=pay_id).first()
                if not current_payment:
                    raise ModelObjectNotFoundError(
                        status_code=500,
                        message="Payment identified by '%s' is not found when payment is timeout" % payment.id
                    )
                # if current_payment.get_payment_state() == PaymentState["WAITING"]:
                if current_payment.pay_state == PaymentState.WAITING.name:
                    self.accomplish(PaymentState["TIMEOUT"].name, payment.pay_id)
                # print(payment.pay_state)

        timer = Timer(
            interval=payment.expires,
            function=callback,
            kwargs=dict(pay_id=payment.pay_id)
        )
        timer.start()


class StockpileService:

    def __init__(self) -> None:
        pass

    # def is_oversell(self, settlement_dto: SettlementDTO) -> bool:
    #     for item in settlement_dto.items:
    #         product = settlement_dto.products[item.product_id]
    #         if item.amount > product.stockpile.amount - product.stockpile:
    #             return False
    #     return True

    def increase(self):
        pass

    def decrease(self, product_id: int, amount: int):
        stockpile = Stockpile.query.filter_by(product_id=product_id).first()
        if not stockpile:
            raise ModelObjectNotFoundError(
                status_code=404,
                message="Stockpile of product identified by '%s' is not found" % product_id
            )
        stockpile.decrease(amount)
        db.session.add(stockpile)
        db.session.commit()

    def freeze(self, product: Product, amount: int):
        # product.stockpile.amount -= amount
        # product.stockpile.frozen += amount
        product.stockpile.freeze(amount)
        db.session.add(product.stockpile)
        db.session.commit()

    def thaw(self, product_id: int, amount: int):
        stockpile = Stockpile.query.filter_by(product_id=product_id).first()
        if not stockpile:
            raise ModelObjectNotFoundError(
                status_code=404,
                message="Stockpile of product identified by '%s' is not found" % product_id
            )
        stockpile.thaw(amount)
        db.session.add(stockpile)
        db.session.commit()