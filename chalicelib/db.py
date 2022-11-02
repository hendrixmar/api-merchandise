import os
from pprint import pprint

from chalicelib.settings import Settings
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine, text

if not os.getenv("GITHUB_ACTION"):
    from dotenv import load_dotenv, find_dotenv

    load_dotenv(find_dotenv())

print("Start__ database")
engine = create_engine(Settings.DATABASE_URL)

Base = declarative_base()
print("Start__ connection started successfully")

def create_all_models():
    Base.metadata.create_all(engine)

TRIGGER_QUERY = """
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
         RAISE EXCEPTION
         'There is not enough stock for the article % it only have %',
         upper(product_name), stock_available;
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
-----------------------------------------------------------
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
       RAISE EXCEPTION
       'There is not enough stock for the article % to updated it only have %',
       upper(product_name), stock_available;
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

CREATE OR REPLACE FUNCTION delete_sales_items()
  RETURNS TRIGGER
  LANGUAGE PLPGSQL
  AS
$$
BEGIN


    -- Update the stock


    UPDATE "tblProducts"
        SET stock = stock + OLD.quantity_sold
            WHERE ID = OLD.product_id;


    IF pg_trigger_depth() = 1 THEN
       UPDATE "tblSales"
        set sale_amount = sale_amount - OLD.sale_amount
            WHERE ID = OLD.sales_id;
    END IF;

    -- Update total amount of the whole sale

    RETURN old;
END;
$$;

CREATE OR REPLACE FUNCTION delete_sales()
  RETURNS TRIGGER
  LANGUAGE PLPGSQL
  AS
$$
DECLARE
    id_sale_item integer;
BEGIN

    FOR id_sale_item IN
        SELECT "tblSalesItem".id FROM "tblSalesItem" where sales_id = OLD.id
    LOOP
        DELETE FROM "tblSalesItem"
         WHERE "tblSalesItem".id = id_sale_item;
        RAISE log '%', id_sale_item;
    END LOOP;

    RETURN old;
END;
$$;



CREATE TRIGGER create_new_sale
  BEFORE INSERT
  ON "tblSalesItem"
  FOR EACH ROW
  EXECUTE PROCEDURE stock_availability();


CREATE TRIGGER update_sales_amount
  BEFORE UPDATE
  ON "tblSalesItem"
  FOR EACH ROW
  EXECUTE PROCEDURE update_sales_items();

CREATE TRIGGER update_stocks_after_delete
  before delete
  ON "tblSalesItem"
  FOR EACH ROW
  EXECUTE PROCEDURE delete_sales_items();


CREATE TRIGGER delete_sale
  before DELETE
  ON "tblSales"
  FOR EACH ROW
  EXECUTE PROCEDURE delete_sales();


"""

def create_triggers():

    with Session() as session:
        stmt = """SELECT  event_object_table AS table_name, trigger_name
                        FROM information_schema.triggers"""

        exist = session.execute(stmt).scalar()
        if not exist:
            session.execute(TRIGGER_QUERY)
            session.commit()



Session = sessionmaker(bind=engine)


