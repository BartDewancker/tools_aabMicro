import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

# Package is `python-dotenv`
from dotenv import load_dotenv

load_dotenv() # Make sure we have our .env values

MYSQL_USER = os.getenv('MYSQL_USER')
if (os.getenv("ENVIRONMENT") == "DOCKER"):
    MYSQL_HOST = os.getenv('MYSQL_HOST')
else:
    MYSQL_HOST = "127.0.0.1"

MYSQL_PORT = os.getenv('MYSQL_PORT')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')


engine = create_engine(
    f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}'
)
session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine) )

db = session()
Base = declarative_base()

def start_db():
    Base.metadata.create_all(engine)