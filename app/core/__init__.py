from dataclasses import dataclass
from typing import List, Protocol
from app.core.entities import *
from app.core.response import Response
from app.core.models import *


class IProductRepo(Protocol):
    def create_receipt(self, receipt_id: int) -> Response:
        pass

    def get_receipt_products(self, receipt_id: int) -> Response[List[Product]]:
        pass

    def get_receipt_total(self, receipt_id: int) -> Response:
        pass

    def close_receipt(self, receipt_id: int) -> Response:
        pass

    def add_to_receipt(
        self, receipt_id: int, product_name: str, product_count: int
    ) -> Response:
        pass

    def receipt_is_open(self):
        pass

    def fetch_reports_on_date(self, report_date: str) -> Response[XReport]:
        pass


@dataclass
class goodwillAPI:
    product_repo: IProductRepo

    def open_receipt(self, receipt_id: int, date: str) -> Response:
        if self.product_repo.receipt_is_open(receipt_id):
            return Response(
                success=False,
                obtained=None,
                msg=f"Receipt {receipt_id} already open",
            )
        return self.product_repo.create_receipt(receipt_id=receipt_id, date=date)

    def add_to_receipt(
        self, receipt_id: int, product_name: str, product_count: int
    ) -> Response:
        product_response = get_product(
            product_name=product_name, product_count=product_count
        )

        product = Product(
            name=product_response.obtained.get_name(),
            price=product_response.obtained.get_price(),
            count=product_response.obtained.get_count(),
        )

        return self.product_repo.add_to_receipt(receipt_id, product)

    def close_receipt(self, receipt_id: int) -> Response:
        if not self.product_repo.receipt_is_open(receipt_id):
            return Response(
                success=False,
                obtained=None,
                msg=f"Receipt #{receipt_id} already closed",
            )
        return self.product_repo.close_receipt(receipt_id=receipt_id)

    def fetch_receipt(self, receipt_id: int) -> Response[CustomersReceipt]:
        if not self.product_repo.receipt_is_open(receipt_id):
            return Response(
                success=False,
                obtained=None,
                msg=f"Receipt #{receipt_id} is closed",
            )

        products = self.product_repo.get_receipt_products(receipt_id=receipt_id)
        grand_total = self.product_repo.get_receipt_total(receipt_id=receipt_id)
        return Response(
            success=True,
            obtained=CustomersReceipt(
                products=products.obtained, grand_total=grand_total.obtained
            ),
            msg=f"Successfully fetched receipt, grand total is {grand_total.obtained}",
        )

    def fetch_x_report(self, report_date: str) -> Response[XReport]:
        report = self.product_repo.fetch_reports_on_date(report_date=report_date)
        return Response(
            success=True,
            obtained=report.obtained,
            msg=f"Successfully fetched X reports for {report_date}",
        )
