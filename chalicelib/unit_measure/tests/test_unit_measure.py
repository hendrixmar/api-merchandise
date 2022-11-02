import json

import pytest

import app
from chalice.test import Client
from http import HTTPStatus as status
from unittest.mock import patch
from decimal import Decimal
from chalicelib.unit_measure.schemas import UnitMeasureSchema
from chalicelib.models import UnitMeasure
from chalicelib.unit_measure.tests.config_test import gateway_factory
from sqlalchemy import delete, select, insert
import logging
from chalicelib.db import Session

logging.basicConfig(level=logging.DEBUG)
mylogger = logging.getLogger(__name__)


@pytest.fixture(autouse=True)
def run_before_and_after_tests(tmpdir):
    with Session() as session:
        session.query(UnitMeasure).delete()
        session.commit()
    yield

    with Session() as session:
        session.query(UnitMeasure).delete()
        session.commit()



class TestUnitMeasure(object):

    @classmethod
    def teardown_class(cls):
        print("TEAR DOWN")
        with Session() as session:
            session.query(UnitMeasure).delete()
            session.commit()

    def test_retrieve_unit_measures(self, gateway_factory):
        with Session() as session:
            session.add_all(
                [
                    UnitMeasure(name="xx"),
                    UnitMeasure(name="kxgs"),
                    UnitMeasure(name="lxbs"),
                ]
            )

            session.commit()

        gateway = gateway_factory()
        response = gateway.handle_request(
            method="GET",
            path="/unit-measure",
            headers={"Content-Type": "application/json"},
            body="",
        )

        with Session() as session:
            stmt = select(UnitMeasure)
            result = session.execute(stmt).scalars().unique().all()
            unit_measure = UnitMeasureSchema().dump(result, many=True)

        body, status_code = json.loads(response.get("body")), response.get("statusCode")

        assert status_code == status.OK
        assert body == unit_measure

    def test_retrieve_unit_measures_by_query(self, gateway_factory):
        with Session() as session:
            session.add_all(
                [
                    UnitMeasure(name="liters"),
                    UnitMeasure(name="grams"),
                    UnitMeasure(name="lb"),
                    UnitMeasure(name="pounds"),
                    UnitMeasure(name="kilograms"),
                    UnitMeasure(name="inches"),
                    UnitMeasure(name="gallons"),
                ]
            )

            session.commit()

        gateway = gateway_factory()
        response = gateway.handle_request(
            method="GET",
            path="/unit-measure?limit=10&orderby=name",
            headers={"Content-Type": "application/json"},
            body="",
        )

        with Session() as session:
            stmt = select(UnitMeasure)
            result = session.execute(stmt).scalars().unique().all()
            unit_measure = UnitMeasureSchema().dump(result, many=True)

        body, status_code = json.loads(response.get("body")), response.get("statusCode")

        assert status_code == status.OK
        assert body == unit_measure

    def test_create_unit_measure(self, gateway_factory):
        gateway = gateway_factory()

        response = gateway.handle_request(
            method="POST",
            path="/unit-measure",
            headers={"Content-Type": "application/json"},
            body=json.dumps({"name": "kilos"}),
        )

        body = json.loads(response.get("body"))

        with Session() as session:
            temp = session.get(UnitMeasure, body.get("id"))
            result = UnitMeasureSchema().dump(temp)

        assert response.get("statusCode") == status.CREATED
        assert body == result

    def test_partial_update(self, gateway_factory):
        with Session() as session:
            stmt = insert(UnitMeasure).values(name="liters")
            (id_new_unit_measure,) = session.execute(stmt).inserted_primary_key
            session.commit()

        gateway = gateway_factory()
        response = gateway.handle_request(
            method="PATCH",
            path=f"/unit-measure/{id_new_unit_measure}",
            headers={"Content-Type": "application/json"},
            body=json.dumps({"name": "kilos"}),
        )

        body = json.loads(response.get("body"))

        with Session() as session:
            result: UnitMeasure = session.get(UnitMeasure, id_new_unit_measure)

        assert response.get("statusCode") == status.NO_CONTENT
        assert body is None
        assert result.name == "kilos"

    def test_duplicate_unit_measure(self, gateway_factory):
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

    def test_delete_unit_measure(self, gateway_factory):
        with Session() as session:
            stmt = insert(UnitMeasure).values(name="kg")
            (id_new_unit_measure,) = session.execute(stmt)\
                .inserted_primary_key
            session.commit()

        gateway = gateway_factory()
        response = gateway.handle_request(
            method="DELETE",
            path=f"/unit-measure/{id_new_unit_measure}",
            headers={"Content-Type": "application/json"},
            body=json.dumps({}),
        )

        body = json.loads(response.get("body"))
        assert response.get("statusCode") == status.NO_CONTENT
        assert body is None
