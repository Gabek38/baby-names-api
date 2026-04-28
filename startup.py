import os
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from database.db_manager import DBManager

db_path = os.path.join(os.path.dirname(__file__), "db", "baby_names.db")

if not os.path.exists(db_path) or os.path.getsize(db_path) < 1000:
    print("Database not found or empty — building now...")
    db = DBManager()
    db.create_table()
    db.load_from_csv()
    db.load_state_data()
    print("Database ready!")
else:
    print("Database already exists, skipping build.")