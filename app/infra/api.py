from typing import List
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from starlette.requests import Request
from app.core import goodwillAPI, CustomersReceipt
from app.core.entities import *

goodwill = APIRouter()


def get_core(request: Request) -> goodwillAPI:
    return request.app.state.core


@goodwill.post("/cashier/open_receipt", response_model=ResponseMsgModel)
def open_receipt(receipt_id: int, date: str, core: goodwillAPI = Depends(get_core)):
    response = core.open_receipt(receipt_id=receipt_id, date=date)
    if not response.succeeded():
        raise HTTPException(status_code=403, detail=response.msg)
    return ResponseMsgModel(msg=f"Receipt #{receipt_id} opened")


@goodwill.put(
    "/cashier/add_to_receipt/{product_name}", response_model=ResponseMsgModel
)
def add_to_receipt(
    receipt_id: int,
    product_name: str,
    product_count: int,
    core: goodwillAPI = Depends(get_core),
):
    response = core.add_to_receipt(receipt_id, product_name, product_count)
    return ResponseMsgModel(msg=f"{response.msg}")


@goodwill.put("/cashier/close_receipt", response_model=ResponseMsgModel)
def close_receipt(receipt_id: int, core: goodwillAPI = Depends(get_core)):
    response = core.close_receipt(receipt_id=receipt_id)
    if not response.succeeded():
        raise HTTPException(status_code=403, detail=response.msg)
    return ResponseMsgModel(msg=f"Receipt #{receipt_id} closed")


@goodwill.get("/customer/get_receipt", response_model=ReceiptModel)
def fetch_receipt(receipt_id: int, core: goodwillAPI = Depends(get_core)):
    response = core.fetch_receipt(receipt_id=receipt_id)
    return response.obtained


@goodwill.get("/manager/x_report", response_model=XReportModel)
def fetch_x_report(report_date: str, core: goodwillAPI = Depends(get_core)):
    response = core.fetch_x_report(report_date=report_date)
    return response.obtained
