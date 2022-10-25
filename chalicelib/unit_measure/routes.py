"""
IMport examples

@app.route('/book/{id}', methods=['DELETE'])
def delete_book(id):
    book_as_json = app.current_request.json_body



"""
import sqlalchemy
from chalice import Blueprint, Response
from sqlalchemy import delete, select, update, insert, exists
from http import HTTPStatus as status
from chalicelib.db import Session
from .args import UnitMeasureSchema
from .models import UnitMeasure
from chalicelib.tools import ValidateId, serializer, marschal_with
from chalice import BadRequestError, ForbiddenError
from sqlalchemy.exc import IntegrityError

unit_measure_routes = Blueprint(__name__)


@unit_measure_routes.route('/unit-measure', methods=['GET'])
@serializer(model=UnitMeasure)
@marschal_with(scheme=UnitMeasureSchema(many=True), status_code=status.OK, content_type='application/json')
def add_unit_measure():
    with Session() as session:
        stmt = select(UnitMeasure)
        unit_measures = session.execute(stmt).scalars().all()
    print(unit_measures)
    return unit_measures


@unit_measure_routes.route('/unit-measure/{key}', methods=['GET'])
@serializer(model=ValidateId())
@marschal_with(scheme=UnitMeasureSchema(), status_code=status.OK, content_type='application/json')
def add_unit_measure(key: int):
    with Session() as session:
        result: UnitMeasure = session.get(UnitMeasure, key)

    return result


@unit_measure_routes.route('/unit-measure', methods=['POST'])
@serializer(model=UnitMeasure)
@marschal_with(scheme=UnitMeasureSchema(), status_code=status.CREATED, content_type='application/json')
def add_unit_measure():
    json_input = unit_measure_routes.current_request.json_body

    with Session() as session:
        stmt = insert(UnitMeasure).values(**json_input)
        try:
            id_new_unit_measure, = session.execute(stmt).inserted_primary_key
            session.commit()
        except IntegrityError:
            raise ForbiddenError(f"The unit-measure ({json_input.get('name')}) already exist")

    return {**json_input, **{'id': id_new_unit_measure}}


@unit_measure_routes.route('/unit-measure/{key}', methods=['PATCH', 'PUT'])
@serializer(model=ValidateId())
@marschal_with(status_code=status.NO_CONTENT, content_type='application/json')
def add_unit_measure(key: int):
    json_input = unit_measure_routes.current_request.json_body

    with Session() as session:
        stmt = select(UnitMeasure).where(UnitMeasure.name == json_input.get('name'))
        stmt = exists(stmt).select()
        result = session.execute(stmt).scalar()

    if result:
        raise ForbiddenError(f"The unit-measure already exist")

    with Session() as session:
        stmt = update(UnitMeasure).where(UnitMeasure.id == key).values(**json_input)
        session.execute(stmt)
        session.commit()


@unit_measure_routes.route('/unit-measure/{key}', methods=['DELETE'])
@serializer(model=ValidateId())
@marschal_with(status_code=status.NO_CONTENT, content_type='application/json')
def add_unit_measure(key: int):
    with Session() as session:
        stmt = delete(UnitMeasure).where(UnitMeasure.id == key)
        session.execute(stmt)


