import sqlalchemy
from chalice import Blueprint, Response
from sqlalchemy import delete, select, update, insert, exists
from http import HTTPStatus as status
from chalicelib.db import Session
from .args import ValidateJsonBodyProduct
from chalicelib.models import Products
from chalicelib.tools import ValidateId, serializer, marschal_with
from chalice import BadRequestError, ForbiddenError
from sqlalchemy.exc import IntegrityError

from ..products.args import ProductsSchema
from ..unit_measure.args import ValidateJsonSorting

product_routes = Blueprint(__name__)


@product_routes.route("/sales", methods=["GET"])
@marschal_with(
    scheme=ProductsSchema(many=True),
    status_code=status.OK,
    content_type="application/json",
)
def retrieve_sales():
    with Session() as session:
        stmt = select(Products)
        products = session.execute(stmt).scalars().all()
    return products


@product_routes.route("/sales/{key}", methods=["GET"])
@serializer(query_string_scheme=ValidateId())
@marschal_with(
    scheme=ProductsSchema(), status_code=status.OK, content_type="application/json"
)
def retrieve_sale(key: int):
    with Session() as session:
        result: Products = session.get(Products, key)

    return result


@product_routes.route("/sales", methods=["POST"])
@serializer(json_scheme=ValidateJsonBodyProduct())
@marschal_with(
    scheme=ProductsSchema(), status_code=status.CREATED, content_type="application/json"
)
def add_sale(json_body: dict = {}):

    with Session() as session:
        stmt = insert(Products).values(**json_body)
        try:
            (id_new_unit_measure,) = session.execute(stmt).inserted_primary_key
            session.commit()
        except IntegrityError:
            raise ForbiddenError(f"The product ({json_body.get('name')}) already exist")

    return {**json_body, **{"id": id_new_unit_measure}}


@product_routes.route("/sales/{key}", methods=["PATCH", "PUT"])
@serializer(query_string_scheme=ValidateId())
@marschal_with(status_code=status.NO_CONTENT, content_type="application/json")
def modify_sale(key: int, body: dict = {}):
    json_input = product_routes.current_request.json_body

    with Session() as session:
        stmt = select(Products).where(Products.name == json_input.get("name"))
        stmt = exists(stmt).select()
        result = session.execute(stmt).scalar()

    if result:
        raise ForbiddenError(f"The products already exist")

    with Session() as session:
        stmt = update(Products).where(Products.id == key).values(**json_input)
        session.execute(stmt)
        session.commit()

    return None


@product_routes.route("/sales/{key}", methods=["DELETE"])
@serializer(query_string_scheme=ValidateId())
@marschal_with(status_code=status.NO_CONTENT, content_type="application/json")
def delete_sale(key: int, json: dict = {}):
    with Session() as session:
        stmt = delete(Products).where(Products.id == key)
        try:

            session.execute(stmt)
            session.commit()
        except IntegrityError:
            raise ForbiddenError(f"The product ({key}) already exist")

    return None
