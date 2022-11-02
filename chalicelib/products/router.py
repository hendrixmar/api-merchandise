import sqlalchemy
from chalice import Blueprint, Response
from sqlalchemy import delete, select, update, insert, exists
from http import HTTPStatus as status
from chalicelib.db import Session
from .schemas import (
    ProductsSchema,
    ValidateJsonBodyProduct,
    ValidateJsonBodyProductPatch, ProductsSalesSchema,
)
from chalicelib.models import Products
from chalicelib.tools import ValidateId, serializer, marschal_with
from chalice import ForbiddenError
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
        stmt = select(Products).limit(100)
        products = session.execute(stmt).scalars().unique().all()
    return products


@product_routes.route("/products/{key}", methods=["GET"])
@serializer(query_string_scheme=ValidateId())
@marschal_with(
    scheme=ProductsSchema(),
    status_code=status.OK,
    content_type="application/json"
)
def retrieve_product(key: int, json_body: dict = {}):
    with Session() as session:
        result: Products = session.get(Products, key)

    return result


@product_routes.route("/products/estadistics", methods=["GET"])
@marschal_with(
    scheme=ProductsSalesSchema(many=True),
    status_code=status.OK,
    content_type="application/json",
)
def retrieve_products_estadistics():
    with Session() as session:
        stmt = select(Products).limit(100)
        products = session.execute(stmt).scalars().unique().all()
    return products


@product_routes.route("/products/estadistics/{key}", methods=["GET"])
@serializer(query_string_scheme=ValidateId())
@marschal_with(
    scheme=ProductsSalesSchema(),
    status_code=status.OK,
    content_type="application/json"
)
def retrieve_product_estadistics(key: int, json_body: dict = {}):
    with Session() as session:
        result: Products = session.get(Products, key)

    return result


@product_routes.route("/products", methods=["POST"])
@serializer(json_scheme=ValidateJsonBodyProduct())
@marschal_with(
    scheme=ProductsSchema(),
    status_code=status.CREATED,
    content_type="application/json"
)
def add_product(json_body: dict = {}):
    with Session() as session:
        stmt = insert(Products).values(**json_body)
        try:
            (id_new_product,) = session.execute(stmt) \
                .inserted_primary_key
            session.commit()
        except IntegrityError:
            raise ForbiddenError(f"The product ({json_body.get('name')}) already exist")
        result = session.get(Products, id_new_product)

    return result



@product_routes.route("/products/{key}", methods=["PATCH", "PUT"])
@serializer(
    query_string_scheme=ValidateId(), json_scheme=ValidateJsonBodyProductPatch()
)
@marschal_with(status_code=status.NO_CONTENT, content_type="application/json")
def modify_product(key: int, json_body: dict = {}):
    with Session() as session:
        result = session.get(Products, key)

    if not result:
        raise ForbiddenError(f"The products doesnt exist")

    with Session() as session:
        try:
            stmt = update(Products) \
                .where(Products.id == key) \
                .values(**json_body)
            session.execute(stmt)
            session.commit()
        except IntegrityError:
            raise ForbiddenError("The product "
                                 "name is already taken")

    return None


@product_routes.route("/products/{key}", methods=["DELETE"])
@serializer(query_string_scheme=ValidateId())
@marschal_with(
    status_code=status.NO_CONTENT,
    content_type="application/json")
def delete_product(key: int, json_body: dict = {}):
    with Session() as session:
        stmt = delete(Products).where(Products.id == key)
        try:
            session.execute(stmt)
            session.commit()
        except IntegrityError:
            raise ForbiddenError(f"The product ({key}) "
                                 f"is linked by an ItemSale")

    return None
