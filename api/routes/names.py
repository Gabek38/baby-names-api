from fastapi import APIRouter, HTTPException
from database.db_manager import DBManager

router = APIRouter()
db = DBManager()

LIFE_EXPECTANCY = {
    "F": {
        1920: 61.0, 1930: 63.0, 1940: 66.0, 1950: 71.0, 1960: 73.0,
        1970: 75.0, 1980: 77.0, 1990: 79.0, 2000: 80.0, 2010: 81.0,
        2020: 81.5, 2024: 82.0
    },
    "M": {
        1920: 56.0, 1930: 58.0, 1940: 61.0, 1950: 65.0, 1960: 67.0,
        1970: 68.0, 1980: 70.0, 1990: 72.0, 2000: 74.0, 2010: 76.0,
        2020: 76.5, 2024: 77.0
    }
}

def estimate_life_expectancy(sex: str, year: int) -> float:
    table = LIFE_EXPECTANCY.get(sex.upper(), {})
    years = sorted(table.keys())
    if year <= years[0]:
        return table[years[0]]
    if year >= years[-1]:
        return table[years[-1]]
    for i in range(len(years) - 1):
        if years[i] <= year < years[i+1]:
            low, high = years[i], years[i+1]
            ratio = (year - low) / (high - low)
            return round(table[low] + ratio * (table[high] - table[low]), 1)
    return 0.0

def get_trend(results):
    year_counts = {}
    for row in results:
        yr = row[3]
        cnt = row[2]
        year_counts[yr] = year_counts.get(yr, 0) + cnt
    recent = sum(year_counts.get(y, 0) for y in range(2015, 2025))
    previous = sum(year_counts.get(y, 0) for y in range(2005, 2015))
    if previous == 0:
        return "📈 Rising"
    change = (recent - previous) / previous * 100
    if change > 10:
        return "📈 Rising"
    elif change < -10:
        return "📉 Declining"
    else:
        return "➡️ Stable"

def get_peak_decade(results):
    decade_counts = {}
    for row in results:
        decade = (row[3] // 10) * 10
        decade_counts[decade] = decade_counts.get(decade, 0) + row[2]
    if not decade_counts:
        return "Unknown"
    peak = max(decade_counts, key=decade_counts.get)
    return f"{peak}s"

def get_rarity(total_count):
    if total_count > 500000:
        return {"label": "Common", "color": "#90ee90"}
    elif total_count > 100000:
        return {"label": "Uncommon", "color": "#89CFF0"}
    elif total_count > 10000:
        return {"label": "Rare", "color": "#ff6eb4"}
    else:
        return {"label": "Extremely Rare", "color": "#ffd700"}

@router.get("/nameinfo", summary="Get name statistics")
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
    total_estimated_living = (
        sum(s["estimated_living"] for s in survival_data["female"]) +
        sum(s["estimated_living"] for s in survival_data["male"])
    )

    female_life_exp = estimate_life_expectancy("F", most_popular_year)
    male_life_exp = estimate_life_expectancy("M", most_popular_year)

    female_by_year = {}
    male_by_year = {}
    for row in results:
        yr = row[3]
        cnt = row[2]
        sex = row[1]
        if sex == "F":
            female_by_year[yr] = female_by_year.get(yr, 0) + cnt
        elif sex == "M":
            male_by_year[yr] = male_by_year.get(yr, 0) + cnt

    trend = get_trend(results)
    peak_decade = get_peak_decade(results)
    rarity = get_rarity(total_count)

    all_that_year = db.search_by_year(most_popular_year)
    top10 = sorted(all_that_year, key=lambda r: r[2], reverse=True)[:10]
    top10_names = [{"name": r[0], "count": r[2], "sex": r[1]} for r in top10]

    return {
        "name": name,
        "estimated_age": estimated_age,
        "first_year": first_year,
        "most_popular_year": most_popular_year,
        "top_years": top_years,
        "total_records": total_count,
        "estimated_living": total_estimated_living,
        "female_survivorship": survival_data["female"],
        "male_survivorship": survival_data["male"],
        "female_life_expectancy": female_life_exp,
        "male_life_expectancy": male_life_exp,
        "female_by_year": female_by_year,
        "male_by_year": male_by_year,
        "trend": trend,
        "peak_decade": peak_decade,
        "rarity": rarity,
        "top10_that_year": top10_names
    }

@router.get("/topnames")
def get_top_names(year: int):
    results = db.search_by_year(year)
    if not results:
        raise HTTPException(status_code=404, detail=f"No data found for year {year}.")
    top10 = sorted(results, key=lambda r: r[2], reverse=True)[:10]
    return {
        "year": year,
        "top_names": [{"name": r[0], "count": r[2], "sex": r[1]} for r in top10]
    }