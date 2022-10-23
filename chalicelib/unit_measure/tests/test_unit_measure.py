import json

import pytest

import app
from chalice.test import Client
from http import HTTPStatus as status
from unittest.mock import patch
from decimal import Decimal
from chalicelib.unit_measure.args import UnitMeasureSchema
from chalicelib.unit_measure.models import UnitMeasure
from chalicelib.products.models import Products
from chalicelib.unit_measure.tests.config_test import gateway_factory
from sqlalchemy import delete, select
import logging
from chalicelib.db import Session

logging.basicConfig(level=logging.DEBUG)
mylogger = logging.getLogger(__name__)


def teardown_class():
    with Session() as session:
        session.query(UnitMeasure).delete()
        session.commit()
    mylogger.info("teardown_class_unit_measure")


def setup_class():
    with Session() as session:
        session.query(UnitMeasure).delete()
        session.commit()
    print("DELETED")

@pytest.fixture(autouse=True)
def run_before_and_after_tests(tmpdir):
    with Session() as session:
        session.query(UnitMeasure).delete()
        session.commit()

    yield

    with Session() as session:
        session.query(UnitMeasure).delete()
        session.commit()

class TestChalice(object):

    def test_retrieve_unit_measures(self, gateway_factory):
        with Session() as session:
            session.add_all([UnitMeasure(name="liters"),
                             UnitMeasure(name="kg"),
                             UnitMeasure(name="lb")])

            session.commit()

        gateway = gateway_factory()
        response = gateway.handle_request(method='GET',
                                          path='/unit-measure',
                                          headers={'Content-Type': 'application/json'},
                                          body=json.dumps({'name': 'kg'}))

        with Session() as session:
            stmt = select(UnitMeasure)
            result = session.execute(stmt)
            unit_measure = UnitMeasureSchema().dump([i[0] for i in result], many=True)

        body, status_code = json.loads(response.get('body')), response.get("statusCode")
        print(response)
        assert status_code == status.OK
        assert body == unit_measure

    def test_create_unit_measure(self, gateway_factory):
        gateway = gateway_factory()
        response = gateway.handle_request(method='POST',
                                          path='/unit-measure',
                                          headers={'Content-Type': 'application/json'},
                                          body='')

        body = json.loads(response.get('body'))
        print(response)
        with Session() as session:
            stmt = select(UnitMeasure).where(UnitMeasure.id == body.get('id'))
            temp, = session.execute(stmt).fetchone()
            result = UnitMeasureSchema().dump(temp)


        assert response.get("statusCode") == status.CREATED
        assert body == dict(result)

    def test_partial_update(self, gateway_factory):
        pass

    def test_full_update(self, gateway_factory):
        pass

    def test_duplicate_unit_measure(self, gateway_factory):
        pass

    def test_delete_unit_measure(self, gateway_factory):
        pass