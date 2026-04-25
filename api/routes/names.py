from fastapi import APIRouter, HTTPException
from database.db_manager import DBManager

router = APIRouter()
db = DBManager()

@router.get("/nameinfo")
def get_name_info(name: str):
    results = db.search(name)

    if not results:
        raise HTTPException(status_code=404, detail=f"Name '{name}' not found in database.")
    
    total_count = sum(row[2] for row in results)

    # Weighted average year to estimate age
    weighted_year = sum(row[3] * row[2] for row in results) / total_count
    estimated_age = 2026 - round(weighted_year)

    first_year = min(row[3] for row in results)

    # Most popular year
    most_popular = max(results, key=lambda r: r[2])
    most_popular_year = most_popular[3]

    # Top 10 years by count
    sorted_results = sorted(results, key=lambda r: r[2], reverse=True)
    top_years = [row[3] for row in sorted_results[:10]]

    return {
        "name": name,
        "estimated_age": estimated_age,
        "first_year": first_year,
        "most_popular_year": most_popular_year,
        "top_years": top_years,
        "total_records": total_count
    }