import os
from chalicelib.settings import Settings
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine

if not os.getenv("GITHUB_ACTION"):
    from dotenv import load_dotenv, find_dotenv

    load_dotenv(find_dotenv())

engine = create_engine(Settings.DATABASE_URL)

Base = declarative_base()


def create_all_models():
    Base.metadata.create_all(engine)


def create_triggers():
    with Session() as session:
        stmt = """SELECT  event_object_table AS table_name ,trigger_name
                        FROM information_schema.triggers"""
        exist = session.execute(stmt).scalar()
        if not exist:
            session.execute(TRIGGERS_DEFINITIONS)
            session.commit()


Session = sessionmaker(bind=engine)

TRIGGERS_DEFINITIONS = """
    CREATE OR REPLACE FUNCTION stock_availability()
      RETURNS TRIGGER
      LANGUAGE PLPGSQL
      AS
    $$
    declare
       stock_available integer;
        product_name text;
    BEGIN
    
        SELECT stock, name into stock_available, product_name FROM "tblProducts" as t where t.id = NEW.product_id;
    
        IF NEW.quantity_sold > stock_available THEN
             RAISE EXCEPTION 'There is not enough stock for the article % it only have %',  upper(product_name), stock_available;
        END IF;
    
        UPDATE "tblProducts"
            SET stock = stock - NEW.quantity_sold
            WHERE ID = NEW.product_id;
    
        RETURN NEW;
    END;
    $$;
    
    CREATE TRIGGER create_new_sale
      BEFORE INSERT
      ON "tblSalesItem"
      FOR EACH ROW
      EXECUTE PROCEDURE stock_availability();
"""

create_all_models()
