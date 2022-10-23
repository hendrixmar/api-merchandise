from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from .models import UnitMeasure
from marshmallow import Schema, fields


class UnitMeasureSchema(SQLAlchemySchema):
    class Meta:
        model = UnitMeasure
        load_instance = True  # Optional: deserialize to model instances

    name = auto_field()
    id = auto_field()
