import app
from chalice.test import Client
from unittest.mock import patch


def test_index():
    with Client(app.app) as client:
        response = client.http.get('/')
        assert response.status_code == 200
        assert response.json_body == {'hello': 'world'}


@patch('app.requests.get')
def test_get_post(mock_get):
    """Mocking with the patch decorator to get a post from an External API"""
    mock_get.return_value.ok = True
    response = app.get_post()
    assert response.ok


@patch('app.requests.get')
def test_no_get_post(mock_get):
    """Mock testing to check when no post is returned"""
    mock_get.return_value.ok = False
    response = app.get_post()
    assert response == None