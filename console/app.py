import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.db_manager import DBManager
from models.name_record import NameRecord

db = DBManager()

def main():
    db.create_table()
    while True:
        print("\n=== Baby Name Database ===")
        print("1. Load SSA national data")
        print("2. Load SSA state data")
        print("3. Add a new name")
        print("4. Search for a name")
        print("5. Update a name record")
        print("6. Delete a name record")
        print("7. Exit")

        choice = input("\nEnter choice: ").strip()

        if choice == "1":
            print("Loading national data... this may take a minute.")
            db.load_from_csv()

        elif choice == "2":
            print("Loading state data... this may take a few minutes.")
            db.load_state_data()

        elif choice == "3":
            name = input("Name: ").strip()
            sex = input("Sex (M/F): ").strip().upper()
            count = input("Count: ").strip()
            year = input("Year: ").strip()
            if not count.isdigit() or not year.isdigit():
                print("Count and year must be numbers.")
                continue
            record = NameRecord(name, sex, int(count), int(year))
            db.insert(record)

        elif choice == "4":
            name = input("Enter name to search: ").strip()
            results = db.search(name)
            if not results:
                print("No records found.")
            else:
                print(f"\n{'Name':<15} {'Sex':<5} {'Count':<10} {'Year'}")
                print("-" * 40)
                for row in results:
                    print(f"{row[0]:<15} {row[1]:<5} {row[2]:<10} {row[3]}")

        elif choice == "5":
            name = input("Name to update: ").strip()
            year = input("Year: ").strip()
            sex = input("Sex (M/F): ").strip().upper()
            new_count = input("New count: ").strip()
            if not year.isdigit() or not new_count.isdigit():
                print("Year and count must be numbers.")
                continue
            db.update(name, int(year), sex, int(new_count))

        elif choice == "6":
            name = input("Name to delete: ").strip()
            year = input("Year: ").strip()
            sex = input("Sex (M/F): ").strip().upper()
            if not year.isdigit():
                print("Year must be a number.")
                continue
            db.delete(name, int(year), sex)

        elif choice == "7":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please enter 1-7.")

if __name__ == "__main__":
    main()