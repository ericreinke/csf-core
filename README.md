# CSF Core

Core backend service for the **Counter-Strike Fantasy** application. Built with **FastAPI** and **PostgreSQL**, this service powers league management, player drafting, roster operations, and fantasy scoring — consuming game data collected by [csf-scraper](https://github.com/ericreinke/csf-scraper).

---

## Tech Stack

| Layer       | Technology              |
|-------------|-------------------------|
| Language    | Python 3.12+            |
| Framework   | FastAPI                 |
| Database    | PostgreSQL              |
| ORM         | SQLAlchemy              |
| Migrations  | Alembic                 |
| Data Source | csf-scraper (demo parsing & stat ingestion) |

---

## Features

- **League CRUD & Management** — Create, update, and manage fantasy leagues with configurable settings
- **Drafting** — Support for live drafts with pick/ban logic and draft order management
- **Roster Management** — Add, drop, and trade CS players across fantasy rosters
- **Scoring & Stats** — Fantasy point calculations driven by real match data from csf-scraper
- **Player Data** — Player lookup and resolution backed by scraped & parsed demo data

---

## Project Structure

```
csf-core/
├── app/
│   ├── api/            # FastAPI route handlers
│   ├── models/         # SQLAlchemy ORM models
│   ├── schemas/        # Pydantic request/response schemas
│   ├── services/       # Business logic layer
│   ├── db/             # Database session & connection config
│   └── main.py         # Application entrypoint
├── alembic/            # Database migrations
├── tests/              # Test suite
├── requirements.txt
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.12+
- PostgreSQL 15+
- A running instance of **csf-scraper** (or its populated database)

### Setup

```bash
# Clone the repo
git clone https://github.com/ericreinke/csf-core.git
cd csf-core

# Create a virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your database credentials

# Run database migrations
alembic upgrade head

# Start the dev server
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000` with interactive docs at `/docs`.

---

## Related Projects

| Project | Description |
|---------|-------------|
| **csf-scraper** | Scrapes HLTV match data, downloads demos, and parses player statistics into PostgreSQL |
