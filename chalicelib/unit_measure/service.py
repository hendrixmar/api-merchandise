from sqlalchemy import select

from chalicelib.models import UnitMeasure
from chalicelib.tools import database_context_decorator


@database_context_decorator
def get_unit_measure(key: int, session):
    stmt = select(UnitMeasure)
    return session.execute(stmt).scalars().unique().all()
