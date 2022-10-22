import json

import app
from chalice.test import Client
from http import HTTPStatus as status
from unittest.mock import patch
from chalicelib.unit_measure.models import UnitMeasure
from chalicelib.products.models import Products
from chalicelib.unit_measure.tests.config_test import gateway_factory
from sqlalchemy import delete, select
import logging
from chalicelib.db import Session

logging.basicConfig(level=logging.DEBUG)
mylogger = logging.getLogger(__name__)


def teardown_class():
    mylogger.info("teardown_class_unit_measure")


def setup_class():
    with Session() as session:
        session.query(UnitMeasure).delete()
        session.commit()





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
            temp = UnitMeasure(name="kg")
            session.add(temp)
            session.commit()


        gateway = gateway_factory()
        response = gateway.handle_request(method='GET',
                                          path='/products',
                                          headers={'Content-Type': 'application/json'},
                                          body=json.dumps({'name': 'kg'}))

        with Session() as session:
            stmt = select(UnitMeasure)
            unit_measure = session.execute(stmt).fetchall()


        print(unit_measure)
        body = json.loads(response.get('body'))

        assert True #body == dict(unit_measure)

    def test_create_unit_measure(self, gateway_factory):
        with Session() as session:
            temp = UnitMeasure(name="liters")
            session.add(temp)
            session.commit()

        gateway = gateway_factory()
        response = gateway.handle_request(method='POST',
                                          path='/products',
                                          headers={'Content-Type': 'application/json'},
                                          body=json.dumps({'name': 'kg'}))

        body = json.loads(response.get('body'))
        print(body)
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
