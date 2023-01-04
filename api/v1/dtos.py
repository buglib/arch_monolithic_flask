from dataclasses import (
    asdict,
    dataclass, 
    field
)
from enum import Enum, unique
from typing import Any, List


@dataclass
class ItemDTO:
    product_id: int = field(init=False)
    amount: int = field(init=False)

    def from_dict(self, data: dict):
        if not isinstance(data, dict):
            err_msg = "argument 'data' must be a instance of dict"
            raise TypeError(err_msg)

        keys = self.__dataclass_fields__.keys()
        for k in keys:
            if k == "product_id":
                k = "id"
            if k not in data:
                err_msg = "argument 'data' must be a instance of dict with key '%s'" % k
                raise KeyError(err_msg)
        
        self.product_id = data["id"]
        self.amount = data["amount"]

    def to_dict(self) -> dict:
        data = asdict(obj=self)
        data["id"] = self.product_id
        data.pop("product_id")
        return data


@dataclass
class AddressDTO:
    province: str
    city: str
    area: str


@unique
class PayType(Enum):
    wechat = 0
    alipay = 1


@dataclass
class PurchaseDTO:
    name: str = field(init=False)
    telephone: str = field(init=False)
    delivery: bool = field(init=False)
    address: AddressDTO = field(init=False)
    location: str = field(init=False)
    pay: PayType = field(init=False)
    user_id: int = field(init=False)
    username: str = field(init=False)
    avatar: str = field(init=False)
    email: str = field(init=False)

    def from_dict(self, data: dict):
        if not isinstance(data, dict):
            err_msg = "argument 'data' must be a instance of dict"
            raise TypeError(err_msg)

        keys = self.__dataclass_fields__.keys()
        for k in keys:
            if k == "user_id":
                k = "id"
            if k not in data:
                err_msg = "argument 'data' must be a instance of dict with key '%s'" % k
                raise KeyError(err_msg)

        self.name = data["name"]
        self.telephone = data["telephone"]
        self.delivery = data["delivery"]
        self.address = AddressDTO(
            province=data["address"].get("province", ""),
            city=data["address"].get("city", ""),
            area=data["address"].get("area", "")
        )
        self.location = data["location"]
        self.pay = PayType[data["pay"]]
        self.user_id = data["id"]
        self.username = data["username"]
        self.avatar = data["avatar"]
        self.email = data["email"]

    def to_dict(self) -> dict:
        data = asdict(obj=self, dict_factory=_purchase_dto_dict_factory)
        data["id"] = self.user_id
        data.pop("user_id")
        return data


def _purchase_dto_dict_factory(data: List[tuple[str, Any]]):
    # 不能命名为“__purchase_dto_dict_factory”
    def convert_enum_repr(obj: Any) -> Any:
        if isinstance(obj, Enum):
            return obj.name
        else:
            return obj
    
    return {k: convert_enum_repr(v) for k, v in data}


@dataclass
class SettlementDTO:
    """ 
    {
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
            "delivery": true,
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
    """
    items: List[ItemDTO] = field(init=False)
    purchase: PurchaseDTO = field(init=False)

    def from_dict(self, data: dict):
        if not isinstance(data, dict):
            err_msg = "argument 'data' must be a instance of dict"
            raise TypeError(err_msg)

        keys = self.__dataclass_fields__.keys()
        for k in keys:
            if k not in data:
                err_msg = "argument 'data' must be a instance of dict with key '%s'" % k
                raise KeyError(err_msg)

        items = data["items"]
        purchase = data["purchase"]

        item_dtos = []
        for item in items:
            item_dto = ItemDTO()
            item_dto.from_dict(data=item)
            item_dtos.append(item_dto)
        self.items = item_dtos

        purchase_dto = PurchaseDTO()
        purchase_dto.from_dict(data=purchase)
        self.purchase = purchase_dto

    def to_dict(self) -> dict:
        data = dict()
        data["items"] = [item.to_dict() for item in self.items]
        data["purchase"] = self.purchase.to_dict()
        return data