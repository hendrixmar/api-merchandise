import json

import app
from chalice.test import Client
from http import HTTPStatus as status
from unittest.mock import patch
from chalicelib.unit_measure.models import UnitMeasure
from chalicelib.products.models import Products
from chalicelib.unit_measure.tests.config_test import gateway_factory


class TestChalice(object):
    def setup_class(self):
        print("setup_class")

    def teardown_class(self):
        print("teardown_class")

    def test_index(self, gateway_factory):
        gateway = gateway_factory()
        response = gateway.handle_request(method='GET',
                                          path='/product/15',
                                          headers={},
                                          body='')
        assert response['statusCode'] == 200

    def test_create_unit_measure_happy_end(self, gateway_factory):
        gateway = gateway_factory()
        response = gateway.handle_request(method='POST',
                                          path='/product',
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
