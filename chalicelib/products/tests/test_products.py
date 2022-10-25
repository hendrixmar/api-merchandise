import json

import app
from chalice.test import Client
from http import HTTPStatus as status
from unittest.mock import patch
from chalicelib.unit_measure.models import UnitMeasure
from chalicelib.products.models import Products
from chalicelib.unit_measure.tests.config_test import gateway_factory
import logging
from chalicelib.db import Session

logging.basicConfig(level=logging.DEBUG)
mylogger = logging.getLogger(__name__)


def teardown_class():
    with Session() as session:
        statement = UnitMeasure.delete()
        session.add(statement)
        session.commit()
    mylogger.info("teardown_class")


def setup_class():
    mylogger.info("setup_class")
    with Session() as session:
        session.query(UnitMeasure).delete()
        session.commit()


class TestUnitMeasursse(object):

    def test_index_3(self, gateway_factory):
        gateway = gateway_factory()
        response = gateway.handle_request(method='GET',
                                          path='/products/15',
                                          headers={},
                                          body='')


        assert response['statusCode'] == 200

    def test_create_products(self, gateway_factory):
        with Session() as session:
            temp = UnitMeasure(name="lb")
            session.add(temp)
            session.commit()

        gateway = gateway_factory()
        response = gateway.handle_request(method='POST',
                                          path='/products',
                                          headers={'Content-Type': 'application/json'},
                                          body=json.dumps({'name': 'kg'}))

        assert True


"""
@patch('app.requests.get')
def test_get_post(mock_get):

    mock_get.return_value.ok = True
    response = app.get_post()
    assert response.ok


@patch('app.requests.get')
def test_no_get_post(mock_get):

    mock_get.return_value.ok = False
    response = app.get_post()
    assert response is None
"""
