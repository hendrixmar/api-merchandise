import json

import app
from chalice.test import Client
from http import HTTPStatus as status
from unittest.mock import patch

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


class TestChalice(object):

    def test_index(self, gateway_factory):
        gateway = gateway_factory()
        response = gateway.handle_request(method='GET',
                                          path='/products/',
                                          headers={},
                                          body='')

        assert True

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

        body = json.loads(response.get('body'))
        assert body == unit_measure


    def test_create_unit_measure(self, gateway_factory):

        gateway = gateway_factory()
        response = gateway.handle_request(method='POST',
                                          path='/unit-measure',
                                          headers={'Content-Type': 'application/json'},
                                          body=json.dumps({'name': 'pounds'}))

        body = json.loads(response.get('body'))
        print(response)
        with Session() as session:
            temp = UnitMeasure(name="liters")
            session.add(temp)
            session.commit()




        assert True

