from marshmallow import Schema, fields
from marshmallow.exceptions import ValidationError
from chalice import BadRequestError, Response
from marshmallow_sqlalchemy import SQLAlchemySchema
from sqlalchemy import exists
from sqlalchemy.orm import DeclarativeMeta
from chalicelib.db import Session


def validate_quantity(n):
    if n < 0:
        raise ValidationError("Quantity must be greater than 0.")
    if n > 30:
        raise ValidationError("Quantity must not be greater than 30.")

    if n == 20:
        raise ValidationError("Quantity must not be greater than 30.")


class ValidateId(Schema):
    key = fields.Integer(validate=validate_quantity)


def serializer(model: DeclarativeMeta, scheme: Schema = None):
    def decorator(endpoint_function):
        def wrapper(*args, **kwargs):
            if scheme:
                try:
                    scheme.load(data=kwargs)

                except ValidationError as err:
                    raise BadRequestError(f"Invalid get parameter {err.messages}")



            result = endpoint_function(*args, **kwargs)
            return result

        return wrapper

    return decorator


def marschal_with(scheme: SQLAlchemySchema = None, status_code: int = 200, content_type: str = 'application/json'):
    def decorator(function):
        def wrapper(*args, **kwargs):
            if (result := function(*args, **kwargs)) and scheme:
                result = scheme.dump(result)

            return Response(body=result,
                            status_code=status_code,
                            headers={'Content-Type': content_type})

        return wrapper

    return decorator
