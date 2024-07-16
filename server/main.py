import pymongo
from fastapi import FastAPI, HTTPException, Depends
import requests
import random
from server.constans import pokemonApi_url
from models import MongoDB

server = FastAPI()


@server.get("/")
def test():
    return {"message": "Welcome to the poc telegram Server"}


@server.get("/random-numbers")
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
        print(mongodb,random_number)
        raise e


@server.get("/pokemon/{pokemon_name}")
def get_pokemon(pokemon_name: str):
    url = f"{pokemonApi_url}{pokemon_name}"
    response = requests.get(url)

    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="No Pokemon found with the given ID")

    pokemon_info = response.json()
    return {"message": f"Pokemon '{pokemon_name}' found", "name": pokemon_name, "id": pokemon_info["id"]}
