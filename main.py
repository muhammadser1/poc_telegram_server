from fastapi import FastAPI, HTTPException, Depends
import random
from models import MongoDB

server = FastAPI()


@server.get("/")
def test():
    return {"message": "Welcome to the poc telegram Server"}


@server.post("/random-numbers")
def generate_and_store_random(mongodb: MongoDB = Depends(MongoDB.get_mongodb)):
    random_number = random.randint(1, 10)

    if mongodb.getNumber(random_number):
        raise HTTPException(status_code=500, detail="Failed to store random number")

    result = mongodb.storeNumber(random_number)
    if result:
        return {"message": f"Random number {random_number} stored successfully"}
