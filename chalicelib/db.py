import os

from chalicelib.settings import Settings
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine


if not os.getenv("GITHUB_ACTION"):
    from dotenv import load_dotenv, find_dotenv

    load_dotenv(find_dotenv())



engine = create_engine(Settings.DATABASE_URL)
Base = declarative_base()

Session = sessionmaker(bind=engine)





