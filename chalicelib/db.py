import os
from chalicelib.settings import Settings
from sqlalchemy.orm import sessionmaker, DeclarativeMeta
from sqlalchemy import create_engine
from chalicelib.products.models import Base as BaseProduct
from chalicelib.unit_measure.models import Base as BaseUnitMeasure

if not os.getenv("GITHUB_ACTION"):
    from dotenv import load_dotenv, find_dotenv

    load_dotenv(find_dotenv())

engine = create_engine(Settings.DATABASE_URL)


def create_all_models():
    for base in [BaseProduct, BaseUnitMeasure]:
        base.metadata.create_all(engine)


print(DeclarativeMeta)
Session = sessionmaker(bind=engine)
