from typing import List
from pydantic import BaseModel


class ResponseMsgModel(BaseModel):
    msg: str


class Product(BaseModel):
    name: str
    price: int
    count: int


class ReceiptModel(BaseModel):
    products: List[Product]
    total: int


class XReportModel(BaseModel):
    income: int
    n_sold: int
    n_receipts: int
