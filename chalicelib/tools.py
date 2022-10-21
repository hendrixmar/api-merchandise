from marshmallow import Schema, fields, validate


class ValidateId(Schema):
    key = fields.Integer(validate=validate.Range(min=18, max=40))
