from marshmallow import Schema, fields
from marshmallow.validate import Range
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from chalicelib.models import Products


class ProductsSchema(SQLAlchemySchema):
    class Meta:
        model = Products
        load_instance = True  # Optional: deserialize to model instances

    id = auto_field()
    name = auto_field()
    price = auto_field()
    unit_measure_id = auto_field()


class ValidateJsonBodyProduct(Schema):
    name = fields.String()
    stock = fields.Integer(validate=Range(min=0))
    price = fields.Decimal(validate=Range(min=0), required=True)
    unit_measure_id = fields.Integer(validate=Range(min=0))
