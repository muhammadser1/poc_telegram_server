from fastapi import HTTPException
from pymongo import MongoClient
import pymongo
import os
from dotenv import load_dotenv

load_dotenv()
mongodb_url = os.getenv('mongodb_url')


class MongoDB:
    def __init__(self):
        self.client = self.connect()
        self.db = self.client['telegram_bot_db']
        self.collection = self.db['random_numbers']

    def connect(self):
        try:
            print(mongodb_url)
            mongo = pymongo.MongoClient(mongodb_url)
            return mongo
        except pymongo.errors.ConnectionFailure as e:
            print(f"Failed to connect to MongoDB: {e}")
            raise e

    def storeNumber(self, number: int):
        try:
            result = self.collection.insert_one({'number': number})
            return result.inserted_id
        except pymongo.errors.PyMongoError as e:
            raise e

    def getNumber(self, number: int):
        try:
            existing_document = self.collection.find_one({'number': number})
            return existing_document
        except pymongo.errors.PyMongoError as e:
            raise e


def get_mongodb():
    return MongoDB()
