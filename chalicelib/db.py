import os
from sqlalchemy import Column, Integer, String,  Date
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine

print("DB")

if not os.getenv("GITHUB_ACTION"):
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv())

config = {key: os.getenv(key) for key in ['DB_USER', 'DB_PASS', 'DB_HOST', 'DB_NAME']}

DATABASE_URL = f"postgresql+psycopg2://{config.get('DB_USER')}:{config.get('DB_PASS')}@{config.get('DB_HOST')}/{config.get('DB_NAME')}"
engine = create_engine(DATABASE_URL)
Base = declarative_base()

Session = sessionmaker(bind=engine)

class Actor(Base):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    birthday = Column(Date)

    def __init__(self, name, birthday):
        self.name = name
        self.birthday = birthday
# create a Session
class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(Date)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

Base.metadata.create_all(engine)





