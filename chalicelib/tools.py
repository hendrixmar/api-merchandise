from marshmallow import Schema, fields
from marshmallow.exceptions import ValidationError
from chalice import BadRequestError
from sqlalchemy.orm import DeclarativeMeta


def validate_quantity(n):
    if n < 0:
        raise ValidationError("Quantity must be greater than 0.")
    if n > 30:
        raise ValidationError("Quantity must not be greater than 30.")

    if n == 20:
        raise ValidationError("Quantity must not be greater than 30.")


class ValidateId(Schema):
    key = fields.Integer(validate=validate_quantity)


def serializer(scheme: Schema, model: DeclarativeMeta):
    def decorator(endpoint_function):
        def wrapper(*args, **kwargs):
            try:
                print(scheme)
                scheme.load(data=kwargs)

            except ValidationError as err:
                raise BadRequestError(f"Invalid get parameter {err.messages}")

            if model:
                pass

            result = endpoint_function(*args, **kwargs)
            return result

        return wrapper

    return decorator


def marschal_with(scheme: Schema):
    def decorator(function):
        def wrapper(*args, **kwargs):
            result = function(*args, **kwargs)
            return [dict(e) for e in result]

        return wrapper

    return decorator
