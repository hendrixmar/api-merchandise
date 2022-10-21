from marshmallow import Schema, fields


class ProductsSchema(Schema):
    name = fields.String()
    price = fields.Decimal()
    unit_measure = fields.Integer()

