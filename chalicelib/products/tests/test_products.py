import json

import pytest

import app
from chalice.test import Client
from http import HTTPStatus as status
from unittest.mock import patch
from decimal import Decimal

from chalicelib.products.args import ProductsSchema
from chalicelib.unit_measure.args import UnitMeasureSchema
from chalicelib.models import Products, UnitMeasure
from chalicelib.unit_measure.tests.config_test import gateway_factory
from sqlalchemy import delete, select, insert
import logging
from chalicelib.db import Session

logging.basicConfig(level=logging.DEBUG)
mylogger = logging.getLogger(__name__)


@pytest.fixture(autouse=True)
def run_before_and_after_tests(tmpdir):
    with Session() as session:
        session.query(Products).delete()
        session.query(UnitMeasure).delete()
        session.commit()

    yield

    with Session() as session:
        session.query(Products).delete()
        session.query(UnitMeasure).delete()
        session.commit()


class TestProducts(object):
    def test_retrieve_products(self, gateway_factory):
        with Session() as session:
            stmt = insert(UnitMeasure).values(name="liters")
            (id_new_unit_measure,) = session.execute(stmt).inserted_primary_key

            session.add_all(
                [
                    Products(
                        name="Coca Cola",
                        price=239,
                        unit_measure_id=id_new_unit_measure,
                        stock=1,
                    ),
                    Products(
                        name="Pepsi",
                        price=239,
                        unit_measure_id=id_new_unit_measure,
                        stock=1,
                    ),
                    Products(
                        name="Fanta",
                        price=239,
                        unit_measure_id=id_new_unit_measure,
                        stock=1,
                    ),
                ]
            )

            session.commit()

        gateway = gateway_factory()
        response = gateway.handle_request(
            method="GET",
            path="/products",
            headers={"Content-Type": "application/json"},
            body="",
        )

        with Session() as session:
            stmt = select(Products)
            result = session.execute(stmt).scalars().unique().all()
            products = ProductsSchema().dump(result, many=True)

        body, status_code = json.loads(response.get("body")), response.get("statusCode")

        assert status_code == status.OK
        assert body == products

    def test_retrieve_product_by_id(self, gateway_factory):
        with Session() as session:
            stmt = insert(UnitMeasure).values(name="ss")
            (id_new_unit_measure,) = session.execute(stmt).inserted_primary_key

            stmt = insert(Products).values(
                name="Coca Colaz", price=239, unit_measure_id=id_new_unit_measure
            )
            (id_new_product,) = session.execute(stmt).inserted_primary_key
            session.commit()

        gateway = gateway_factory()

        response = gateway.handle_request(
            method="GET",
            path=f"/products/{id_new_product}",
            headers={"Content-Type": "application/json"},
            body=json.dumps({}),
        )

        with Session() as session:
            result: Products = session.get(Products, id_new_product)
            products = ProductsSchema().dump(result)

        body, status_code = json.loads(response.get("body")), response.get("statusCode")

        assert status_code == status.OK
        assert body == products

    def test_create_product(self, gateway_factory):
        gateway = gateway_factory()

        with Session() as session:
            stmt = insert(UnitMeasure).values(name="liters")
            (id_new_unit_measure,) = session.execute(stmt).inserted_primary_key
            session.commit()

        response = gateway.handle_request(
            method="POST",
            path="/products",
            headers={"Content-Type": "application/json"},
            body=json.dumps(
                {
                    "name": "Wasser",
                    "unit_measure_id": id_new_unit_measure,
                    "stock": 10,
                    "price": 420.303,
                }
            ),
        )

        body = json.loads(response.get("body"))

        with Session() as session:
            temp = session.get(Products, body.get("id"))
            result = ProductsSchema().dump(temp)

        result["price"] = round(result["price"], 2)
        assert response.get("statusCode") == status.CREATED
        assert body == result

    def test_partial_update(self, gateway_factory):
        with Session() as session:
            stmt = insert(UnitMeasure).values(name="liters")
            (id_new_unit_measure,) = session.execute(stmt).inserted_primary_key
            stmt_product = insert(Products).values(
                name="coca cola",
                stock=10,
                unit_measure_id=id_new_unit_measure,
                price=420.23,
            )
            (id_new_product,) = session.execute(stmt_product).inserted_primary_key
            session.commit()

        gateway = gateway_factory()
        response = gateway.handle_request(
            method="PATCH",
            path=f"/products/{id_new_product}",
            headers={"Content-Type": "application/json"},
            body=json.dumps({"name": "pepsi"}),
        )

        body = json.loads(response.get("body"))
        with Session() as session:
            result: Products = session.get(Products, id_new_product)

        assert response.get("statusCode") == status.NO_CONTENT
        assert body is None
        assert result.name == "pepsi"

    def test_duplicate_product(self, gateway_factory):
        """Test trying to create a unit-measure that already exist"""
        with Session() as session:
            stmt = insert(UnitMeasure).values(name="liters")
            session.execute(stmt)
            session.commit()

        gateway = gateway_factory()
        response = gateway.handle_request(
            method="POST",
            path=f"/unit-measure",
            headers={"Content-Type": "application/json"},
            body=json.dumps({"name": "liters"}),
        )

        body = json.loads(response.get("body"))

        assert response.get("statusCode") == status.FORBIDDEN
        assert body.get("Code") == "ForbiddenError"
        assert body.get("Message") == "The unit-measure (liters) already exist"

    def test_delete_product(self, gateway_factory):
        with Session() as session:
            stmt = insert(UnitMeasure).values(name="liters")
            (id_new_product,) = session.execute(stmt).inserted_primary_key
            session.commit()

        gateway = gateway_factory()
        response = gateway.handle_request(
            method="DELETE",
            path=f"/products/{id_new_product}",
            headers={"Content-Type": "application/json"},
            body=json.dumps({}),
        )

        body = json.loads(response.get("body"))
        assert response.get("statusCode") == status.NO_CONTENT
        assert body is None

    def test_validate_new_product_input(self, gateway_factory):
        with Session() as session:
            stmt = insert(UnitMeasure).values(name="liters")
            (id_new_unit_measure,) = session.execute(stmt).inserted_primary_key
            session.commit()

        gateway = gateway_factory()
        _ = {
            "name": "cabronxxsh",
            "price": -402.2323,
            "stock": -100,
            "unit_measure_id": id_new_unit_measure,
        }
        response = gateway.handle_request(
            method="POST",
            path="/products",
            headers={"Content-Type": "application/json"},
            body=json.dumps(_),
        )

        with Session() as session:
            stmt = select(Products)
            result = session.execute(stmt).scalars().all()
            products = ProductsSchema().dump(result, many=True)

        body, status_code = json.loads(response.get("body")), response.get("statusCode")

        assert status_code == status.BAD_REQUEST
        assert "'price': ['Must be greater than or equal to 0" in body.get("Message")
        assert "'stock': ['Must be greater than or equal to 0" in body.get("Message")
