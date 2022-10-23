import json

from chalice import Blueprint, Response
from sqlalchemy import delete, select

from chalicelib.db import Session
from .models import Products
from .args import ProductsSchema
from marshmallow import Schema
from marshmallow.exceptions import ValidationError
from marshmallow import fields
from chalicelib.tools import ValidateId
from chalicelib.tools import serializer, marschal_with
from ..unit_measure.models import UnitMeasure

product_routes = Blueprint(__name__)


@product_routes.route('/products/{key}', methods=['GET'])
@serializer(scheme=ValidateId(), model=Products)
@marschal_with(scheme=ProductsSchema())
def retrieves_product(key: int):
    return [{'id': '1', 'name': 'The Bourne Identity', 'price': '420.13', 'unit_measure': '420'}]


@product_routes.route('/products', methods=['GET'])
@serializer(ValidateId(), Products)
def add_product():
    json_input = product_routes.current_request.json_body
    with Session() as session:
        stmt = select(UnitMeasure)
        unit_measure = session.execute(stmt)
        result = [dict(i[0]) for i in unit_measure]

    return \
        """
        Response(body=json.dumps(result),
                    headers={'Content-Type': 'application/json'},
                    status_code=200)
    """

@product_routes.route('/product/{key}', methods=['PATCH'])
def overwrite_product(key: int):
    return {'foo': f'bar{key}'}


@product_routes.route('/product/{key}', methods=['DELETE'])
def remove_product(key: int):
    return {'foo': f'bar{key}'}
