from dataclasses import dataclass, field
from typing import List, Dict

from app.core.models import *


@dataclass
class ProductRepo:
    receipts: List = field(default_factory=list)
    products: Dict[int, list] = field(default_factory=dict)

    def create_receipt(self, receipt_id: int, date: str) -> Response:
        self.receipts.append(Receipt(date=date, receipt_id=receipt_id, open=True))
        return Response(
            success=True, obtained=None, msg=f"Receipt #{receipt_id} opened"
        )

    def get_receipt_products(self, receipt_id: int) -> Response[List[Product]]:
        if receipt_id not in self.products:
            return Response(
                success=False,
                obtained=None,
                msg=f"Receipt #{receipt_id} not found",
            )
        return Response(
            success=True,
            obtained=self.products[receipt_id],
            msg=f"Products for receipt #{receipt_id} fetched",
        )

    def get_receipt_total(self, receipt_id: int) -> Response:
        if receipt_id not in self.products:
            return Response(
                success=False,
                obtained=None,
                msg=f"Receipt #{receipt_id} not found",
            )
        grand_total = 0
        for item in self.products[receipt_id]:
            grand_total += item.price
        return Response(
            success=True,
            obtained=grand_total,
            msg=f"Products for receipt #{receipt_id} fetched",
        )

    def close_receipt(self, receipt_id: int) -> Response:
        for receipt in self.receipts:
            if receipt.receipt_id == receipt_id:
                receipt.open = False
        return Response(
            success=True, obtained=None, msg=f"Receipt #{receipt_id} closed"
        )

    def add_to_receipt(self, receipt_id: int, product: Product) -> Response:
        if not product:
            return Response(success=False, obtained=None, msg="Product is None")

        if receipt_id in self.products:
            self.products[receipt_id].append(product)
        else:
            self.products[receipt_id] = [product]
        return Response(
            success=True,
            obtained=None,
            msg=f"{product.count}X {product.name} added to receipt #{receipt_id}",
        )

    def receipt_is_open(self, receipt_id: int):
        for receipt in self.receipts:
            if receipt.receipt_id == receipt_id:
                return receipt.open
        return False

    def fetch_reports_on_date(self, report_date: str) -> Response[XReport]:
        income = 0
        n_sold = 0
        n_receipts = 0
        for receipt in self.receipts:
            if receipt.date == report_date:
                n_receipts += 1
                for product in self.products[receipt.receipt_id]:
                    n_sold += product.count
                    income += product.price

        x_report = XReport(
            income=income,
            n_sold=n_sold,
            n_receipts=n_receipts,
        )
        return Response(
            success=True,
            obtained=x_report,
            msg=f"Found {n_receipts} receipts",
        )
