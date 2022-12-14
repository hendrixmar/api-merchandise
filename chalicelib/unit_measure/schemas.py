from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field

from chalicelib.db import Session
from chalicelib.models import UnitMeasure
from marshmallow import Schema, fields


class UnitMeasureSchema(SQLAlchemySchema):
    class Meta:
        model = UnitMeasure
        load_instance = True  # Optional: deserialize to model instances
        include_relationships = True
        sqla_session = Session

    name = auto_field()
    id = auto_field()


class ValidateJsonSorting(Schema):
    name = fields.Boolean()
