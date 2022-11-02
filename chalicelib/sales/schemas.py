from marshmallow import Schema, fields
from marshmallow.validate import Range
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field

from chalicelib.db import Session
from chalicelib.models import Sales, SalesItem
from chalicelib.products.schemas import ProductsSchema
from marshmallow_sqlalchemy.fields import Nested


class SalesItemsSchema(SQLAlchemySchema):
    class Meta:
        model = SalesItem
        include_relationships = True
        load_instance = True
        sqla_session = Session

    id_sale_item = auto_field("id")
    sale_amount = fields.Float()
    quantity_sold = auto_field()
    products = Nested(ProductsSchema, many=False)


class SalesSchema(SQLAlchemySchema):
    class Meta:
        model = Sales
        include_relationships = True
        load_instance = True
        sqla_session = Session

    id = auto_field()
    sale_amount = fields.Float()
    time_created = auto_field()
    sales_items = Nested(SalesItemsSchema, many=True)


class ProductSale(Schema):
    product_id = fields.Integer()
    quantity_sold = fields.Integer()


class ValidateJsonBodySales(Schema):
    date_time = fields.DateTime()
    products = fields.List(fields.Nested(ProductSale), required=True)


class ValidateJsonBodySalesPatch(Schema):
    products = fields.List(fields.Nested(ProductSale), required=True)

