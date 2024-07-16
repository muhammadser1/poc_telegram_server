from unittest.mock import patch

import pytest
from fastapi import HTTPException
from httpx import AsyncClient
from fastapi.testclient import TestClient
from requests import RequestException
from models import MongoDB

from server import main

client = TestClient(main.server)


def test_welcome():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the poc telegram Server"}


def test_get_pokemon_found():
    pokemon_name = "ditto"
    expected_response = {"message": f"Pokemon '{pokemon_name}' found", "name": pokemon_name, "id": 132}
    response = client.get(f"http://localhost:8000/pokemon/{pokemon_name}")

    assert response.status_code == 200
    assert response.json() == expected_response


def test_get_pokemon_not_found():
    pokemon_name = "ditto2"
    response = client.get(f"http://localhost:8000/pokemon/{pokemon_name}")
    assert response.status_code == 404
    assert response.json()["detail"] == "No Pokemon found with the given ID"


def test_generate_and_store_random():
    response = client.get(f"http://localhost:8000/random-numbers")
    ## sucess
    if response.status_code == 200:
        print(response.json())
        assert "message" in response.json()
        assert "stored successfully" in response.json()["message"]
    ##fail
    if response.status_code == 400:
        print(response.json()["detail"])
        assert "already exists in the database" in response.json()["detail"]