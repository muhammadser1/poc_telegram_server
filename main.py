from fastapi import FastAPI

server = FastAPI()


@server.get("/")
def test():
    return {"message": "Welcome to the poc telegram  Server"}
