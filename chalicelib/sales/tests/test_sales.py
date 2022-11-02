import json
import random

import pytest
from typing import List
import app
from chalice.test import Client
from http import HTTPStatus as status
from unittest.mock import patch
from decimal import Decimal

from chalicelib.products.schemas import ProductsSchema
from chalicelib.sales.schemas import SalesSchema, ProductSale
from chalicelib.unit_measure.schemas import UnitMeasureSchema
from chalicelib.models import Products, UnitMeasure, Sales, SalesItem
from chalicelib.unit_measure.tests.config_test import gateway_factory
from sqlalchemy import delete, select, insert
import logging
from chalicelib.db import Session

logging.basicConfig(level=logging.DEBUG)
mylogger = logging.getLogger(__name__)


@pytest.fixture(autouse=True)
def run_before_and_after_tests(tmpdir):
    yield
    print("HOLA")


class TestSales(object):
    @classmethod
    def setup_class(cls):


        with Session() as session:
            stmt = insert(UnitMeasure).values(name="liters")
            (id_new_unit_measure,) = session.execute(stmt).inserted_primary_key
            stmt = insert(UnitMeasure).values(name="kg")
            (id_new_kg,) = session.execute(stmt).inserted_primary_key
            session.add_all(
                [
                    Products(
                        name="Coca Cola",
                        price=4.20,
                        unit_measure_id=id_new_unit_measure,
                        stock=100,
                    ),
                    Products(
                        name="Pepsi",
                        price=2.1,
                        unit_measure_id=id_new_unit_measure,
                        stock=100,
                    ),
                    Products(
                        name="Fanta",
                        price=23.23,
                        unit_measure_id=id_new_unit_measure,
                        stock=100,
                    ),
                    Products(
                        name="rice",
                        price=4.20,
                        unit_measure_id=id_new_kg,
                        stock=100,
                    ),
                    Products(
                        name="potatoes",
                        price=2.1,
                        unit_measure_id=id_new_kg,
                        stock=100,
                    ),
                    Products(
                        name="tomato",
                        price=23.23,
                        unit_measure_id=id_new_kg,
                        stock=100,
                    ),
                ]
            )

            # session.commit()

    @classmethod
    def teardown_class(cls):
        print("TEAR DOWN")
        with Session() as session:
            session.query(Sales).delete()
            session.query(Products).delete()
            session.query(UnitMeasure).delete()
            session.commit()

    def test_retrieve_sales(self, gateway_factory):
        """Test that all sales information is retrieve in the correct format"""
        gateway = gateway_factory()
        response = gateway.handle_request(
            method="GET",
            path="/sales",
            headers={"Content-Type": "application/json"},
            body=json.dumps({}),
        )

        with Session() as session:
            stmt = select(Sales)
            temp = session.execute(stmt).scalars().unique().all()
            sales_result = SalesSchema(many=True).dump(temp)

        body, status_code = json.loads(response.get("body")), response.get("statusCode")

        assert status_code == status.OK
        assert sales_result == body

    def test_retrieve_sale_by_id(self, gateway_factory):
        """Test a certain sales information is retrieve in the correct format"""
        with Session() as session:
            stmt = insert(Sales)
            (sales_id,) = session.execute(stmt).inserted_primary_key
            session.commit()

        gateway = gateway_factory()
        response = gateway.handle_request(
            method="GET",
            path=f"/sales/{sales_id}",
            headers={"Content-Type": "application/json"},
            body=json.dumps({}),
        )
        with Session() as session:
            temp = session.get(Sales, sales_id)
            sales = SalesSchema().dump(temp)
        body, status_code = json.loads(response.get("body")), response.get("statusCode")

        assert status_code == status.OK
        assert body == sales

    def test_create_sale(self, gateway_factory):
        """Test the creation of a sale by replicate the calculation of the quantity sold
        and checking if the stock is update in the table products"""
        gateway = gateway_factory()

        with Session() as session:
            stmt_product_fetch = select(Products)
            products: [Products] = (
                session.execute(stmt_product_fetch).scalars().unique().all()
            )

            products_sale = [
                {
                    "product_id": product.id,
                    "quantity_sold": 10,
                    "stock_available": product.stock,
                    "price": float(product.price),
                }
                for product in products
            ]
            request_body = [
                {
                    "product_id": product.get("product_id"),
                    "quantity_sold": product.get("quantity_sold"),
                }
                for product in products_sale
            ]

        response = gateway.handle_request(
            method="POST",
            path="/sales",
            headers={"Content-Type": "application/json"},
            body=json.dumps(
                {
                    "products": request_body,
                }
            ),
        )

        body = json.loads(response.get("body"))

        with Session() as session:
            temp = session.get(Sales, body.get("id"))
            result = SalesSchema().dump(temp)

        assert response.get("statusCode") == status.CREATED
        assert body == result
        total_amount = 0
        # recreating the calculation of the total cost and the total cost of each item
        for sale_item in body.get("sales_items"):
            total_cost = sale_item.get("quantity_sold") * sale_item.get("products").get(
                "price"
            )
            assert round(total_cost, 2) == sale_item.get("sale_amount")
            total_amount += total_cost
            """
            id_product = sale_item['products']['id']
            product = [product for product in products_sale if product.get('id') == id_product].pop()
            assert product.get("stock_available") ==
            """
        assert round(total_amount, 2) == body.get("sale_amount")

    def test_partial_update(self, gateway_factory):
        with Session() as session:
            stmt = insert(Sales)
            (sale_id,) = session.execute(stmt).inserted_primary_key

            stmt_product_fetch = select(Products)

            temp: List[Products] = (
                session.execute(stmt_product_fetch).scalars().unique().all()
            )
            products = [
                {
                    "quantity_sold": 10,
                    "product_id": product.id,
                }
                for product in temp
            ]
            session.bulk_save_objects(
                [SalesItem(sales_id=sale_id, **product) for product in products]
            )
            session.commit()

        gateway = gateway_factory()

        response = gateway.handle_request(
            method="PATCH",
            path=f"/sales/{sale_id}",
            headers={"Content-Type": "application/json"},
            body=json.dumps(
                {
                    "products": [
                        {"product_id": product.get("product_id"), "quantity_sold": 20}
                        for product in products
                    ]
                }
            ),
        )

        body = json.loads(response.get("body"))
        with Session() as session:
            result: Sales = session.get(Sales, sale_id)

        assert response.get("statusCode") == status.NO_CONTENT
        assert body is None

    def test_delete_product(self, gateway_factory):
        with Session() as session:
            stmt_product_fetch = select(Sales)
            sales: [Sales] = (
                session.execute(stmt_product_fetch).scalars().unique().first()
            )
            sale_id = sales.id

        gateway = gateway_factory()
        response = gateway.handle_request(
            method="DELETE",
            path=f"/sales/{sale_id}",
            headers={"Content-Type": "application/json"},
            body=json.dumps({}),
        )

        body = json.loads(response.get("body"))
        assert response.get("statusCode") == status.NO_CONTENT
        assert body is None

        with Session() as session:
            found = session.get(Sales, sale_id)
            assert not found
