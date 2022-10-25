from marshmallow import Schema, fields
from marshmallow.exceptions import ValidationError
from chalice import BadRequestError, Response
from marshmallow_sqlalchemy import SQLAlchemySchema
from sqlalchemy import exists
from sqlalchemy.orm import DeclarativeMeta
from chalicelib.db import Session


def validate_quantity(n):

    if n == 20:
        raise ValidationError("Quantity must not be greater than 30.")


class ValidateId(Schema):
    key = fields.Integer()


def serializer(scheme: Schema = None):
    def decorator(endpoint_function):
        def wrapper(*args, **kwargs):
            from app import app
            # TODO serializer the json body
            print(app.current_request.json_body, "si se pudo", kwargs)
            try:
                if scheme:
                    scheme.load(data=kwargs)
            except ValidationError as err:
                raise BadRequestError(f"Invalid get parameter {err.messages}")

            return endpoint_function(*args, **kwargs)

        return wrapper

    return decorator


def marschal_with(
    scheme: SQLAlchemySchema = None,
    status_code: int = 200,
    content_type: str = "application/json",
):
    def decorator(function):
        def wrapper(*args, **kwargs):
            if (result := function(*args, **kwargs)) and scheme:
                result = scheme.dump(result)

            return Response(
                body=result,
                status_code=status_code,
                headers={"Content-Type": content_type},
            )

        return wrapper

    return decorator
