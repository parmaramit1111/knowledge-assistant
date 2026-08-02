# Development Setup

## Requirements

- Python 3.12+
- PostgreSQL
- Git

## Clone

git clone ...

## Create Virtual Environment

python -m venv .venv

source .venv/bin/activate

## Install Dependencies

pip install -r requirements.txt

## Environment Variables

cp .env.example .env

Update:

DATABASE_URL
OPENAI_API_KEY
...

## Database

alembic upgrade head

## Run

uvicorn app.main:app --reload

## Background Worker

python -m app.workers.scheduler

## API Documentation

http://localhost:8000/docs
