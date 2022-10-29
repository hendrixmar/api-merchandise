from marshmallow import Schema, fields
from marshmallow.validate import Range
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from chalicelib.models import Sales, SalesItem
from chalicelib.products.args import ProductsSchema
from marshmallow_sqlalchemy.fields import Nested


class SalesItemsSchema(SQLAlchemySchema):
    class Meta:
        model = SalesItem
        include_relationships = True
        load_instance = True

    id = auto_field()
    sale_amount = auto_field()
    quantity_sold = auto_field()
    products = Nested(ProductsSchema, many=False, exclude=("id",))


class SalesSchema(SQLAlchemySchema):
    class Meta:
        model = Sales
        include_relationships = True
        load_instance = True

    id = auto_field()
    sale_amount = auto_field()
    time_created = auto_field()
    sales_items = Nested(SalesItemsSchema, many=True)


class ValidateJsonBodyProduct(Schema):
    name = fields.String()
    stock = fields.Integer(validate=Range(min=0))
    price = fields.Decimal(validate=Range(min=0), required=True)
    unit_measure_id = fields.Integer(validate=Range(min=0))


class ValidateJsonBodySales(Schema):
    name = fields.String()
    items = fields.Integer(validate=Range(min=0))
    price = fields.Decimal(validate=Range(min=0), required=True)
    unit_measure_id = fields.Integer(validate=Range(min=0))


