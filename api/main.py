import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI
from fastapi.responses import FileResponse
from api.routes.names import router

app = FastAPI(
    title="Baby Names API",
    description="Query SSA baby name data from 1880-2024. National and state-level data.",
    version="2.0.0"
)

app.include_router(router)

@app.get("/")
def root():
    return FileResponse("templates/chart.html")