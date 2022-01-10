from app.core import *
from app.infra.in_mem import ProductRepo


def test_add_receipt():
    api_core = goodwillAPI(product_repo=ProductRepo())
    receipt = api_core.open_receipt(receipt_id=1, date="01.01.22").obtained
    assert receipt == None


def test_add_product():
    api_core = goodwillAPI(product_repo=ProductRepo())
    receipt = api_core.open_receipt(receipt_id=1, date="01.01.22").obtained

    api_core.add_to_receipt(receipt_id=1, product_name="Ghomi", product_count=1)
    response = api_core.fetch_receipt(receipt_id=1)
    assert response.obtained.grand_total == 4


def test_add_multiple_products():
    api_core = goodwillAPI(product_repo=ProductRepo())
    receipt = api_core.open_receipt(receipt_id=1, date="01.01.22").obtained

    api_core.add_to_receipt(receipt_id=1, product_name="Ghomi", product_count=1)
    api_core.add_to_receipt(receipt_id=1, product_name="Beer", product_count=6)
    api_core.add_to_receipt(receipt_id=1, product_name="Water", product_count=1)

    response = api_core.fetch_receipt(receipt_id=1)
    assert response.obtained.grand_total == 23


def test_x_report():
    api_core = goodwillAPI(product_repo=ProductRepo())
    receipt = api_core.open_receipt(receipt_id=1, date="01.01.22").obtained

    api_core.add_to_receipt(receipt_id=1, product_name="Ghomi", product_count=1)
    api_core.add_to_receipt(receipt_id=1, product_name="Beer", product_count=6)

    response = api_core.fetch_x_report(report_date="01.01.22")
    assert response.obtained.income == 22
