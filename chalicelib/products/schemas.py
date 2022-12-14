from marshmallow import Schema, fields
from marshmallow.validate import Range
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow_sqlalchemy.fields import Nested

from chalicelib.db import Session
from chalicelib.models import Products, SalesItem

from chalicelib.unit_measure.schemas import UnitMeasureSchema


class ProductsSchema(SQLAlchemySchema):
    class Meta:
        model = Products
        load_instance = True  # Optional: deserialize to model instances
        include_relationships = True
        sqla_session = Session

    id = auto_field()
    name = auto_field()
    price = fields.Float()
    stock = auto_field()
    unit_measure = Nested(UnitMeasureSchema, exclude=("id",))


class SalesItemsProductSchema(SQLAlchemySchema):
    class Meta:
        model = SalesItem
        include_relationships = True
    id_sale_item = auto_field("id")
    sale_amount = fields.Float()
    quantity_sold = auto_field()

class ProductsSalesSchema(SQLAlchemySchema):
    class Meta:
        model = Products
        load_instance = True  # Optional: deserialize to model instances
        include_relationships = True
        sqla_session = Session

    id = auto_field()
    name = auto_field()
    price = fields.Float()
    unit_measure = Nested(UnitMeasureSchema, exclude=("id",))
    sales_item = Nested(SalesItemsProductSchema, many=True)





class ValidateJsonBodyProduct(Schema):
    name = fields.String()
    stock = fields.Integer(validate=Range(min=0))
    price = fields.Decimal(validate=Range(min=0), required=True)
    unit_measure_id = fields.Integer(validate=Range(min=0))


class ValidateJsonBodyProductPatch(Schema):
    name = fields.String()
    stock = fields.Integer(validate=Range(min=0))
    price = fields.Decimal(validate=Range(min=0))
    unit_measure_id = fields.Integer(validate=Range(min=0))
