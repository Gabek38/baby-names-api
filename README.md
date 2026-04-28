# Baby Names API

a two-part application build with python, SQLite, and FastAPI that ingests the Social Administration's baby names dataset and exposes it via a REST API.

## Team Member
- Gabriel Karpiel

## How To Run

https://web-production-eafd3.up.railway.app/

## Set up
'''bash
python -m venv venv
venv\Scripts\activate
pip install fastapi uvicorn
'''

## Console App
'''bash
python console/app.py
'''
- Select option 1 to load SSA data first
- Then use options 2-5 for CRUD operations

## API
'''bash
uvicorn api.main:app --reload
''

## API Usage

## Get name info