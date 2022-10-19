from chalice import Blueprint
from chalicelib.db import Session

product_routes = Blueprint(__name__)


@product_routes.route('/product/{key}', methods=['GET'])
def retrieves_product(key):

    return {'foo': f'bar{key}'}


@product_routes.route('/product/{key}', methods=['POST'])
def add_product(key):
    return {'foo': f'bar{key}'}


@product_routes.route('/product/{key}', methods=['PATCH'])
def overwrite_product(key):
    return {'foo': f'bar{key}'}


@product_routes.route('/product/{key}', methods=['DELETE'])
def remove_product(key):
    return {'foo': f'bar{key}'}
