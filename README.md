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
| Testing     | pytest + httpx          |
| Data Source | csf-scraper (demo parsing & stat ingestion) |

---

## Project Structure

```
csf-core/
├── app/
│   ├── api/            # FastAPI route handlers (controllers)
│   │   ├── leagues.py
│   │   ├── rosters.py
│   │   └── accounts.py
│   ├── models/         # SQLAlchemy ORM models
│   │   ├── league.py
│   │   ├── roster.py
│   │   └── account.py
│   ├── schemas/        # Pydantic request/response schemas (DTOs)
│   │   ├── league.py
│   │   ├── roster.py
│   │   └── account.py
│   ├── services/       # Business logic layer
│   │   ├── league_service.py
│   │   ├── roster_service.py
│   │   └── account_service.py
│   ├── db/             # Database session & connection config
│   │   ├── base.py
│   │   └── session.py
│   ├── config.py       # App configuration (env vars)
│   └── main.py         # Application entrypoint
├── alembic/            # Database migrations
├── tests/              # Test suite
│   ├── conftest.py     # Test fixtures & DB setup
│   ├── test_leagues.py
│   ├── test_rosters.py
│   └── test_accounts.py
├── requirements.txt
└── README.md
```

---

## API Endpoints

| Method   | Endpoint              | Description            |
|----------|-----------------------|------------------------|
| `GET`    | `/health`             | Health check           |
| `POST`   | `/leagues/`           | Create a league        |
| `GET`    | `/leagues/`           | List all leagues       |
| `GET`    | `/leagues/{id}`       | Get a league by ID     |
| `PATCH`  | `/leagues/{id}`       | Update a league        |
| `DELETE` | `/leagues/{id}`       | Delete a league        |
| `POST`   | `/rosters/`             | Create a roster          |
| `GET`    | `/rosters/`             | List all rosters         |
| `GET`    | `/rosters/{id}`         | Get a roster by ID       |
| `PATCH`  | `/rosters/{id}`         | Update a roster          |
| `DELETE` | `/rosters/{id}`         | Delete a roster          |
| `POST`   | `/accounts/`            | Create an account          |
| `GET`    | `/accounts/`            | List all accounts         |
| `GET`    | `/accounts/{id}`        | Get an account by ID       |
| `PATCH`  | `/accounts/{id}`        | Update an account          |
| `DELETE` | `/accounts/{id}`        | Deactivate an account      |

---

## Getting Started

### Prerequisites

- Python 3.12+
- PostgreSQL 15+

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

# Configure environment variables (optional — defaults to local postgres)
# Set DATABASE_URL in a .env file to override
# Example: DATABASE_URL=postgresql://user:pass@localhost:5432/csf_core

# Run database migrations
alembic upgrade head

# Start the dev server
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000` with interactive docs at `/docs`.

### Running Tests

```bash
# Requires a csf_core_test database
pytest tests/ -v
```

---

## Related Projects

| Project | Description |
|---------|-------------|
| **csf-scraper** | Scrapes HLTV match data, downloads demos, and parses player statistics into PostgreSQL |
