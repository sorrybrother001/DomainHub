# DomainHub v4

A production-ready SaaS scaffold built with Flask (DomainHub v4).

Quickstart (development)
1. Copy `.env.example` to `.env` and fill values (leave placeholders for cloud keys).
2. Create a Python 3.13 virtualenv and install:
   pip install -r requirements.txt
3. Initialize the DB (SQLite dev default):
   export FLASK_APP=manage.py
   flask db init
   flask db migrate -m "Initial"
   flask db upgrade
4. Run:
   flask run
5. Admin UI: /admin
6. Tests:
   pytest

Docker:
- docker-compose up --build

Deployment:
- Files included for Railway, Render, Fly.io (placeholders).