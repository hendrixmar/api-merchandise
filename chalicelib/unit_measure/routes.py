
"""
IMport examples

@app.route('/book/{id}', methods=['DELETE'])
def delete_book(id):
    book_as_json = app.current_request.json_body



"""

from chalice import Blueprint, Response
from sqlalchemy import delete, select
from http import HTTPStatus as status
from chalicelib.db import Session
from .args import UnitMeasureSchema
from .models import UnitMeasure
from chalicelib.tools import ValidateId
from chalicelib.tools import serializer, marschal_with


unit_measure_routes = Blueprint(__name__)


@unit_measure_routes.route('/unit-measure', methods=['GET'])
@serializer(model=UnitMeasure)
@marschal_with(scheme=UnitMeasureSchema(), status_code=status.OK, content_type='application/json')
def add_unit_measure():

    with Session() as session:
        stmt = select(UnitMeasure)
        unit_measures = [row[0] for row in session.execute(stmt)]

    return unit_measures


@unit_measure_routes.route('/unit-measure', methods=['POST'])
@serializer(model=UnitMeasure)
@marschal_with(scheme=UnitMeasureSchema(), status_code=status.CREATED, content_type='application/json')
def add_unit_measure():
    json_input = unit_measure_routes.current_request.json_body

    with Session() as session:
        new_unit_measure = UnitMeasure(**json_input)
        session.add(new_unit_measure)
        session.commit()

        print(dict(new_unit_measure))


    print(new_unit_measure.name)
    return new_unit_measure
