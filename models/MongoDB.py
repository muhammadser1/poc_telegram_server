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
        mongo = pymongo.MongoClient(mongodb_url)
        return mongo

    def storeNumber(self, number: int):
        result = self.collection.insert_one({'number': number})
        return result.inserted_id

    def getNumber(self, number: int):
        existing_document = self.collection.find_one({'number': number})
        return existing_document


def get_mongodb():
    return MongoDB()
