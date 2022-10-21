import app
from chalice.test import Client
from unittest.mock import patch





"""
def test_index():
    with Client(app.app) as client:
        response = client.http.get('/product/15')
        assert response.status_code == 200
        
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