import sqlalchemy
from chalice import Blueprint, Response
from sqlalchemy import delete, select, update, insert, exists
from http import HTTPStatus as Status
from chalicelib.db import Session
from .args import UnitMeasureSchema
from chalicelib.models import UnitMeasure
from chalicelib.tools import ValidateId, serializer, marschal_with
from chalice import BadRequestError, ForbiddenError
from sqlalchemy.exc import IntegrityError

unit_measure_routes = Blueprint(__name__)


@unit_measure_routes.route("/unit-measure", methods=["GET"])
@marschal_with(
    scheme=UnitMeasureSchema(many=True),
    status_code=Status.OK,
    content_type="application/json",
)
def add_unit_measure(json_body: dict = {}):
    with Session() as session:
        stmt = select(UnitMeasure)
        unit_measures = session.execute(stmt).scalars().unique().all()

    return unit_measures


@unit_measure_routes.route("/unit-measure/{key}", methods=["GET"])
@serializer(query_string_scheme=ValidateId())
@marschal_with(
    scheme=UnitMeasureSchema(), status_code=Status.OK, content_type="application/json"
)
def add_unit_measure(key: int, json_body: dict = {}):
    with Session() as session:
        result: UnitMeasure = session.get(UnitMeasure, key)

    return result


@unit_measure_routes.route("/unit-measure", methods=["POST"])
@serializer()
@marschal_with(
    scheme=UnitMeasureSchema(),
    status_code=Status.CREATED,
    content_type="application/json",
)
def add_unit_measure(json_body: dict = {}):

    with Session() as session:
        stmt = insert(UnitMeasure).values(**json_body)
        try:
            (id_new_unit_measure,) = session.execute(stmt).inserted_primary_key
            session.commit()
        except IntegrityError:
            raise ForbiddenError(
                f"The unit-measure ({json_body.get('name')}) already exist"
            )

    return {**json_body, **{"id": id_new_unit_measure}}


@unit_measure_routes.route("/unit-measure/{key}", methods=["PATCH", "PUT"])
@serializer(query_string_scheme=ValidateId())
@marschal_with(status_code=Status.NO_CONTENT, content_type="application/json")
def add_unit_measure(key: int, json_body: dict = {}):
    with Session() as session:
        stmt = update(UnitMeasure).where(UnitMeasure.id == key).values(**json_body)
        try:
            session.execute(stmt)
            session.commit()
        except IntegrityError:
            raise ForbiddenError(
                f"The unit-measure ({json_body.get('name')}) already exist"
            )


@unit_measure_routes.route("/unit-measure/{key}", methods=["DELETE"])
@serializer(query_string_scheme=ValidateId())
@marschal_with(status_code=Status.NO_CONTENT, content_type="application/json")
def add_unit_measure(key: int, json_body: dict = {}):
    with Session() as session:
        stmt = delete(UnitMeasure).where(UnitMeasure.id == key)
        try:
            session.execute(stmt)
            session.commit()
        except IntegrityError:
            raise ForbiddenError(
                f"The unit measure with the id {key} is related with one more products"
            )

    return None
