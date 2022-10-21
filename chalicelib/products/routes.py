import json

from chalice import Blueprint, Response
from chalicelib.db import Session
from .models import Products
from .args import ProductsSchema
from marshmallow import Schema
from marshmallow.exceptions import ValidationError
from marshmallow import fields
from chalicelib.tools import ValidateId
from chalicelib.tools import serializer, marschal_with

product_routes = Blueprint(__name__)


@product_routes.route('/product/{key}', methods=['GET'])
@serializer(ValidateId)
@marschal_with(ProductsSchema)
def retrieves_product(key: int):
    if key == 2:
        with Session() as session:
            bourne_identity = Products("The Bourne Identity", 420.13)
            session.add(bourne_identity)
            session.commit()
        with Session() as session:
            temp = session.query(Products).all()

        return temp

    return [{'id': '1', 'name': 'The Bourne Identity', 'price': '420.13', 'unit_measure': '420'}]


@product_routes.route('/product', methods=['POST'])
def add_product():
    json_input = product_routes.current_request.json_body
    return Response(body=json.dumps(json_input),
                    headers={'Content-Type': 'application/json'},
                    status_code=200)


@product_routes.route('/product/{key}', methods=['PATCH'])
def overwrite_product(key: int):
    return {'foo': f'bar{key}'}


@product_routes.route('/product/{key}', methods=['DELETE'])
def remove_product(key: int):
    return {'foo': f'bar{key}'}
