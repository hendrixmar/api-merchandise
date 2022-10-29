import os
from chalicelib.settings import Settings
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine, text

if not os.getenv("GITHUB_ACTION"):
    from dotenv import load_dotenv, find_dotenv

    load_dotenv(find_dotenv())

engine = create_engine(Settings.DATABASE_URL)

Base = declarative_base()


def create_all_models():
    Base.metadata.create_all(engine)


def create_triggers():

    with open("./chalicelib/triggers.sql") as file:
        stmt_triggers = text(file.read())

    with Session() as session:
        stmt = """SELECT  event_object_table AS table_name, trigger_name
                        FROM information_schema.triggers"""

        exist = session.execute(stmt).scalar()
        if not exist:
            session.execute(stmt_triggers)
            session.commit()


Session = sessionmaker(bind=engine)

TRIGGERS_DEFINITIONS = """
    CREATE TRIGGER create_new_sale
      BEFORE INSERT
      ON "tblSalesItem"
      FOR EACH ROW
      EXECUTE PROCEDURE stock_availability();
    
    
    CREATE TRIGGER update_sales_amount
      before UPDATE
      ON "tblSalesItem"
      FOR EACH ROW
      EXECUTE PROCEDURE update_sales_items();

"""


ROUTINES_DEFINITIONS = """
    
CREATE OR REPLACE FUNCTION stock_availability()
  RETURNS TRIGGER
  LANGUAGE PLPGSQL
  AS
$$
declare
   stock_available integer;
    product_name text;
    product_price DECIMAL;
BEGIN

    SELECT stock, name, price
        into stock_available, product_name, product_price
        FROM "tblProducts" as t where t.id = NEW.product_id;

    -- Check if there is availability of the product
	IF NEW.quantity_sold > stock_available THEN
		 RAISE EXCEPTION 'There is not enough stock for the article % it only have %',  upper(product_name), stock_available;
	END IF;

    UPDATE "tblProducts"
        SET stock = stock - NEW.quantity_sold
        WHERE ID = NEW.product_id;

    -- Update the sale_amount of the sale_amount
    NEW.sale_amount := (NEW.sale_amount + product_price * NEW.quantity_sold);
    UPDATE "tblSales"
        SET sale_amount = sale_amount + NEW.sale_amount
        WHERE id = NEW.sales_id;

	RETURN NEW;
END;
$$;



CREATE OR REPLACE FUNCTION update_sales_items()
  RETURNS TRIGGER
  LANGUAGE PLPGSQL
  AS
$$
declare
    stock_available integer;
    product_name text;
    product_price DECIMAL;
BEGIN

    SELECT stock, name, price
        into stock_available, product_name, product_price
        FROM "tblProducts" as t where t.id = NEW.product_id;

	IF NEW.quantity_sold > stock_available + OLD.quantity_sold  THEN
		 RAISE EXCEPTION 'There is not enough stock for the article % to updated it only have %',  upper(product_name), stock_available;
	END IF;

    UPDATE "tblProducts"
        SET stock = stock_available + OLD.quantity_sold  - NEW.quantity_sold
        WHERE ID = NEW.product_id;

    NEW.sale_amount := product_price * NEW.quantity_sold;

    UPDATE "tblSales"
        set sale_amount = sale_amount - OLD.sale_amount + NEW.sale_amount
        WHERE ID = NEW.sales_id;

	RETURN NEW;
END;
$$;
"""

create_all_models()
