import sqlite3
import os
from config import DB_PATH, DATA_DIR
from models.name_record import NameRecord

class DBManager:
    def __init__(self):
        self.db_path = DB_PATH

    def connect(self):
        return sqlite3.connect(self.db_path)

    def create_table(self):
        with self.connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS names (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    sex TEXT NOT NULL,
                    count INTEGER NOT NULL,
                    year INTEGER NOT NULL
                )
            """)
            conn.commit()
        print("Database table ready.")

    def load_from_csv(self):
        files = [f for f in os.listdir(DATA_DIR) if f.endswith(".txt")]
        if not files:
            print("No data files found.")
            return
        with self.connect() as conn:
            total = 0
            for filename in files:
                year = int(filename.replace("yob", "").replace(".txt", ""))
                filepath = os.path.join(DATA_DIR, filename)
                with open(filepath, "r") as f:
                    for line in f:
                        parts = line.strip().split(",")
                        if len(parts) != 3:
                            continue
                        name, sex, count = parts
                        conn.execute(
                            "INSERT INTO names (name, sex, count, year) VALUES (?, ?, ?, ?)",
                            (name, sex, int(count), year)
                        )
                        total += 1
            conn.commit()
        print(f"Loaded {total} records into the database.")

    def insert(self, record: NameRecord):
        with self.connect() as conn:
            conn.execute(
                "INSERT INTO names (name, sex, count, year) VALUES (?, ?, ?, ?)",
                (record.name, record.sex, record.count, record.year)
            )
            conn.commit()
        print("Record inserted.")

    def search(self, name):
        with self.connect() as conn:
            cursor = conn.execute(
                """SELECT name, sex, SUM(count) as count, year 
                   FROM names WHERE name = ? COLLATE NOCASE 
                   GROUP BY name, sex, year""",
                (name,)
            )
            rows = cursor.fetchall()
        return rows

    def update(self, name, year, sex, new_count):
        with self.connect() as conn:
            conn.execute(
                "UPDATE names SET count = ? WHERE name = ? AND year = ? AND sex = ?",
                (new_count, name, year, sex)
            )
            conn.commit()
        print("Record updated.")

    def delete(self, name, year, sex):
        with self.connect() as conn:
            conn.execute(
                "DELETE FROM names WHERE name = ? AND year = ? AND sex = ?",
                (name, year, sex)
            )
            conn.commit()
        print("Record deleted.")

    def get_survivorship(self, name):
        from database.life_tables import get_survival_probability
        rows = self.search(name)
        current_year = 2026
        female_survival = []
        male_survival = []
        for row in rows:
            birth_year = row[3]
            count = row[2]
            sex = row[1]
            age = current_year - birth_year
            survival_prob = get_survival_probability(age)
            estimated_living = round(count * survival_prob)
            entry = {
                "year": birth_year,
                "original_count": count,
                "estimated_living": estimated_living
            }
            if sex == "F":
                female_survival.append(entry)
            elif sex == "M":
                male_survival.append(entry)
        return {"female": female_survival, "male": male_survival}

    def search_by_year(self, year):
        with self.connect() as conn:
            cursor = conn.execute(
                """SELECT name, sex, SUM(count) as count, year
                   FROM names WHERE year = ?
                   GROUP BY name, sex
                   ORDER BY count DESC""",
                (year,)
            )
            rows = cursor.fetchall()
        return rows