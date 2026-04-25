import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI
from api.routes.names import router

app = FastAPI(title="Baby NamesAPI")

app.include_router(router)

@app.get("/")
def root():
    return {"message": "Baby Names API is running. Use /nameinfo?name=Emma to query a name."}