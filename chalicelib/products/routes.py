from chalice import Blueprint
from chalicelib.db import Session
from .models import Products
from .args import ProductsSchema
from marshmallow import Schema
from marshmallow import fields
from chalicelib.tools import ValidateId
product_routes = Blueprint(__name__)

"""

"""


def serializer(scheme: Schema):

    def decorator(function):
        def wrapper(*args, **kwargs):
            print("----serializeer----")
            print(scheme)
            print(kwargs)
            scheme().load(kwargs)
            print(function)
            result = function(*args, **kwargs)
            print(result)
            print("---------------------")
            return result

        return wrapper

    return decorator




def marschal_with(scheme: Schema):

    def decorator(function):
        def wrapper(*args, **kwargs):

            result = function(*args, **kwargs)
            return [dict(e) for e in result]

        return wrapper


    return decorator



@product_routes.route('/product/{key}', methods=['GET'])
@serializer(ValidateId)
@marschal_with(ProductsSchema)
def retrieves_product(key):
    with Session() as session:
        bourne_identity = Products("The Bourne Identity", 420.13)

        session.add(bourne_identity)

        session.commit()
    with Session() as session:
        temp = session.query(Products).all()

    return temp


@product_routes.route('/product/{key}', methods=['POST'])
def add_product(key):
    return {'foo': f'bar{key}'}


@product_routes.route('/product/{key}', methods=['PATCH'])
def overwrite_product(key):
    return {'foo': f'bar{key}'}


@product_routes.route('/product/{key}', methods=['DELETE'])
def remove_product(key):
    return {'foo': f'bar{key}'}
