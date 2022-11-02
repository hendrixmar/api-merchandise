import sqlalchemy
from chalice import Blueprint, Response
from sqlalchemy import delete, select, update, insert, exists, func
from http import HTTPStatus as status
from chalicelib.db import Session
from .schemas import ValidateJsonBodySales, ValidateJsonBodySalesPatch
from chalicelib.models import Products, Sales, SalesItem
from chalicelib.tools import ValidateId, serializer, marschal_with
from chalice import BadRequestError, ForbiddenError
from sqlalchemy.exc import IntegrityError

from chalicelib.sales.schemas import SalesSchema

sales_routes = Blueprint(__name__)


@sales_routes.route("/sales", methods=["GET"])
@marschal_with(
    scheme=SalesSchema(many=True),
    status_code=status.OK,
    content_type="application/json",
)
def retrieve_sales():
    with Session() as session:
        stmt = select(Sales).limit(100)
        sales = session.execute(stmt).scalars().unique().all()
    return sales


@sales_routes.route("/sales/estadistics", methods=["GET"])
@serializer(query_string_scheme=ValidateId())
@marschal_with(
    status_code=status.OK,
    content_type="application/json",
)
def retrieve_sales():
    query_string = sales_routes.current_request.query_params

    with Session() as session:
        stmt = select(func.extract(query_string.get('condition'), Sales.time_created),
                      func.sum(Sales.sale_amount)). \
            where((Sales.time_created >= query_string.get('from')) &
                  (Sales.time_created <= query_string.get('to'))
                  ). \
            group_by(func.extract(query_string.get('condition'), Sales.time_created))
        temp = session.execute(stmt).all()

    if query_string.get('condition') == 'month':
        months = ['January',
                  'February',
                  'March',
                  'April',
                  'May',
                  'June',
                  'July',
                  'August',
                  'September',
                  'October',
                  'November',
                  'December', ]
        return [(months[int(year) - 1], amount) for year, amount in temp]

    return


@sales_routes.route("/sales/{key}", methods=["GET"])
@serializer(query_string_scheme=ValidateId())
@marschal_with(
    scheme=SalesSchema(),
    status_code=status.OK,
    content_type="application/json"
)
def retrieve_sale(key: int, json_body: dict = {}):
    with Session() as session:
        result: Sales = session.get(Sales, key)

    return result


@sales_routes.route("/sales", methods=["POST"])
@serializer(json_scheme=ValidateJsonBodySales())
@marschal_with(
    scheme=SalesSchema(), status_code=status.CREATED, content_type="application/json"
)
def add_sale(json_body: dict = {}):
    with Session() as session:
        stmt = insert(Sales).limit(100)
        (sale_id,) = session.execute(stmt).inserted_primary_key

        session.bulk_save_objects(
            [
                SalesItem(sales_id=sale_id, **product)
                for product in json_body.get("products")
            ]
        )
        session.commit()
        result = session.get(Sales, sale_id)

    return result


@sales_routes.route("/sales/{key}", methods=["PATCH", "PUT"])
@serializer(query_string_scheme=ValidateId(), json_scheme=ValidateJsonBodySalesPatch())
@marschal_with(status_code=status.NO_CONTENT, content_type="application/json")
def modify_sale(key: int, json_body: dict = {}):
    with Session() as session:
        for sale_item in json_body.get("products"):
            stmt = (
                update(SalesItem)
                    .where(
                    (SalesItem.sales_id == key)
                    & (SalesItem.product_id == sale_item.get("product_id"))
                )
                    .values(quantity_sold=sale_item.get("quantity_sold"))
            )
            session.execute(stmt)
        session.commit()

    return None


@sales_routes.route("/sales/{key}", methods=["DELETE"])
@serializer(query_string_scheme=ValidateId())
@marschal_with(
    status_code=status.NO_CONTENT,
   content_type="application/json")
def delete_sale(key: int, json_body: dict = {}):
    with Session() as session:
        stmt = delete(Sales).where(Sales.id == key)
        try:
            session.execute(stmt)
            session.commit()
        except IntegrityError:
            raise ForbiddenError(f"The product ({key}) already exist")

    return None
