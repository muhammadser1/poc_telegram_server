import pymongo
from fastapi import FastAPI, HTTPException, Depends
import random
from models import MongoDB

server = FastAPI()


@server.get("/")
def test():
    return {"message": "Welcome to the poc telegram Server"}


@server.post("/random-numbers")
def generate_and_store_random(mongodb: MongoDB = Depends(MongoDB.get_mongodb)):
    try:
        random_number = random.randint(1, 100)
        if mongodb.getNumber(random_number):
            raise HTTPException(status_code=400, detail=f"Number {random_number} already exists in the database")

        result = mongodb.storeNumber(random_number)
        if result:
            return {"message": f"Random number {random_number} stored successfully"}

    except pymongo.errors.OperationFailure as e:
        raise HTTPException(status_code=500, detail=f"Failed to connect to MongoDB: {str(e)}")

    except pymongo.errors.PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"PyMongo error occurred: {str(e)}")

    except HTTPException as e:
        raise e