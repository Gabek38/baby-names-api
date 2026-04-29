# Baby Names API

A two-part application built with Python, SQLite, and FastAPI that ingests 
the Social Security Administration's baby names dataset and exposes it via 
a REST API with an interactive web interface.

## 🌐 Live Demo
**https://web-production-eafd3.up.railway.app**

## Team Members
- Gabriel Karpiel

## Project Description
This project loads SSA baby name data (1880–2024) — both national and 
state-level — into a SQLite database and provides:
- A console-based CRUD interface
- A REST API built with FastAPI
- An interactive web UI with Chart.js visualizations

## Features
- 📊 Name popularity charts by gender (national and state level)
- 📈 Trend indicator (Rising, Declining, Stable)
- 💀 Survivorship estimates using SSA life tables
- ⚕️ Life expectancy by gender and birth year
- 🏆 Top 10 names for any given year
- 🔍 Name comparison charts
- 💎 Name rarity badges
- 📍 State-level data for all 50 states

## How to Run Locally

### Setup
```bash
python -m venv venv
venv\Scripts\activate
pip install fastapi uvicorn aiofiles
```

### Console App
```bash
python console/app.py
```
- Select option 1 to load national SSA data first
- Select option 2 to load state data
- Use options 3-6 for CRUD operations

### API
```bash
uvicorn api.main:app --reload
```

Then open http://127.0.0.1:8000 in your browser.

## API Endpoints

### Get name info (national)