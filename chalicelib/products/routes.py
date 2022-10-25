import sqlalchemy
from chalice import Blueprint, Response
from sqlalchemy import delete, select, update, insert, exists
from http import HTTPStatus as status
from chalicelib.db import Session
from .args import ProductsSchema
from chalicelib.models import Products
from chalicelib.tools import ValidateId, serializer, marschal_with
from chalice import BadRequestError, ForbiddenError
from sqlalchemy.exc import IntegrityError

product_routes = Blueprint(__name__)


@product_routes.route("/products", methods=["GET"])
@marschal_with(
    scheme=ProductsSchema(many=True),
    status_code=status.OK,
    content_type="application/json",
)
def retrieve_products():
    with Session() as session:
        stmt = select(Products)
        products = session.execute(stmt).scalars().all()
    return products


@product_routes.route("/products/{key}", methods=["GET"])
@serializer(scheme=ValidateId())
@marschal_with(
    scheme=ProductsSchema(), status_code=status.OK, content_type="application/json"
)
def add_product(key: int):

    with Session() as session:
        result: Products = session.get(Products, key)

    return result


@product_routes.route("/products", methods=["POST"])
@marschal_with(
    scheme=ProductsSchema(), status_code=status.CREATED, content_type="application/json"
)
def add_unit_measure():
    json_input = product_routes.current_request.json_body

    with Session() as session:
        stmt = insert(Products).values(**json_input)
        try:
            (id_new_unit_measure,) = session.execute(stmt).inserted_primary_key
            session.commit()
        except IntegrityError:
            raise ForbiddenError(
                f"The product ({json_input.get('name')}) already exist"
            )

    return {**json_input, **{"id": id_new_unit_measure}}


@product_routes.route("/products/{key}", methods=["PATCH", "PUT"])
@serializer(scheme=ValidateId())
@marschal_with(status_code=status.NO_CONTENT, content_type="application/json")
def add_product(key: int):
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


@product_routes.route("/products/{key}", methods=["DELETE"])
@serializer(scheme=ValidateId())
@marschal_with(status_code=status.NO_CONTENT, content_type="application/json")
def add_unit_measure(key: int):
    with Session() as session:
        stmt = delete(Products).where(Products.id == key)
        session.execute(stmt)
        session.commit()

    return None