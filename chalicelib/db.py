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

create_all_models()

Session = sessionmaker(bind=engine)
