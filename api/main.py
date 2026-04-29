import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI
from fastapi.responses import FileResponse
from api.routes.names import router

# Auto-build database if it doesn't exist
db_path = os.path.join(os.path.dirname(__file__), '..', 'db', 'baby_names.db')
db_path = os.path.abspath(db_path)

if not os.path.exists(db_path) or os.path.getsize(db_path) < 1000:
    print("Database not found — building now. This may take a few minutes...")
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    from database.db_manager import DBManager
    db = DBManager()
    db.create_table()
    db.load_from_csv()
    db.load_state_data()
    print("Database build complete!")
else:
    print(f"Database found at {db_path} ({os.path.getsize(db_path)} bytes)")

app = FastAPI(
    title="Baby Names API",
    description="Query SSA baby name data from 1880-2024. National and state-level data.",
    version="2.0.0"
)

app.include_router(router)

@app.get("/")
def root():
    return FileResponse("templates/chart.html")