from fastapi import FastAPI
from src.routes import pokemon

app = FastAPI()

app.include_router(pokemon.router)

@app.get("/")
def read_root():
    return {"message": "API FastAPI está rodando"}
