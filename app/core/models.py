from abc import ABC
from dataclasses import dataclass
from typing import List, Protocol

from app.core import Response


@dataclass
class Product:
    name: str
    price: int
    count: int


@dataclass
class Receipt:
    date: str
    receipt_id: int
    open: bool


@dataclass
class CustomersReceipt:
    products: List[Product]
    grand_total: int


@dataclass
class XReport:
    income: int
    n_sold: int
    n_receipts: int


class AbstractItem(ABC):
    def get_name(self) -> str:
        pass

    def get_price(self) -> int:
        pass

    def get_count(self) -> int:
        pass


@dataclass
class Item(AbstractItem):
    name: str
    price: int

    def get_name(self) -> str:
        return self.name

    def get_price(self) -> int:
        return self.price

    def get_count(self) -> int:
        return 1


@dataclass
class Pack(AbstractItem):
    item: Item
    count: int

    def get_name(self) -> str:
        return self.item.get_name()

    def get_price(self) -> int:
        return self.item.get_price() * self.count

    def get_count(self) -> int:
        return self.count


warehouse: [AbstractItem] = []

water = Item(name="Water", price=1)
beer = Item(name="Beer", price=3)
ghomi = Item(name="Ghomi", price=4)

beer_pack = Pack(item=beer, count=6)
water_pack = Pack(item=water, count=3)

warehouse += [water_pack, beer_pack, ghomi, water, beer]


def get_product(product_name: str, product_count: int) -> Response[AbstractItem]:
    for item in warehouse:
        if item.get_name() == product_name and item.get_count() == product_count:
            return Response(
                success=True, obtained=item, msg=f"{product_name} found"
            )
    return Response(success=False, obtained=None, msg="No product found")
