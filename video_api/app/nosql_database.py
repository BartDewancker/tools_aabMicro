import os
from pymongo import MongoClient

# Package is `python-dotenv`
from dotenv import load_dotenv

load_dotenv() # Make sure we have our .env values


MONGO_USER = os.getenv('MONGO_USER')
if (os.getenv("ENVIRONMENT") == "DOCKER"):
    MONGO_HOST = os.getenv('MONGO_HOST')
else:
    MONGO_HOST = "localhost"

MONGO_PORT = os.getenv('MONGO_PORT')
MONGO_DATABASE = os.getenv('MONGO_DATABASE')
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD')

def get_database(collection_name: str):

    CONNECTION_STRING = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}/{MONGO_DATABASE}?authSource=admin"
    client = MongoClient(CONNECTION_STRING)
    db = client[MONGO_DATABASE]
    return db[collection_name]