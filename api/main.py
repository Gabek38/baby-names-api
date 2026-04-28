import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from api.routes.names import router

app = FastAPI(
    title="Baby Names API",
    description="Query SSA baby name data from 1880-2024.",
    version="1.0.0"
)

templates = Jinja2Templates(directory="templates")

app.include_router(router)

@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse("chart.html", {"request": request})