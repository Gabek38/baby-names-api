from fastapi import APIRouter, HTTPException
from database.db_manager import DBManager

router = APIRouter()
db = DBManager()

@router.get("/nameinfo", summary="Get name statistics",
            description="Returns estimatedage, first year, most popular, top years, and survivorship estimate for a given name.")
def get_name_info(name: str):
    results = db.search(name)

    if not results:
        raise HTTPException(status_code=404, detail=f"Name '{name}' not found in database.")
    
    total_count = sum(row[2] for row in results)
    weighted_year = sum(row[3] * row[2] for row in results) / total_count
    estimated_age = 2026 - round(weighted_year)
    first_year = min(row[3] for row in results)
    most_popular = max(results, key=lambda r: r[2])
    most_popular_year = most_popular[3]
    sorted_results = sorted(results, key=lambda r: r[2], reverse=True)
    top_years = [row[3] for row in sorted_results[:10]]

    survival_data = db.get_survivorship(name)
    total_estimated_living = sum(s["estimated_living"] for s in survival_data)

    return {
        "name": name,
        "estimated_age": estimated_age,
        "first_year": first_year,
        "most_popular_year": most_popular_year,
        "top_years": top_years,
        "total_records": total_count,
        "estimated_living": total_estimated_living,
        "survivorship_by_year": survival_data
    }