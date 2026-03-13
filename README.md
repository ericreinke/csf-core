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
| Data Source | csf-scraper (background worker orchestrating HLTV scraping & demo parsing) |

---

## 🏛️ Architecture: The Shared Database Pattern

**CSF Core** and **csf-scraper** do not use separate or isolated databases. They operate on a powerful **Shared Database Architecture** where they point to the exact same Postgres connection URL.

- **`csf-core` is the Owner (Source of Truth):**
  This FastAPI backend completely owns the database schema. It dictates the SQLAlchemy ORM definitions, defines constraints, and is the only app allowed to execute `alembic` database migrations.
- **`csf-scraper` is the Worker:**
  The scraper functions as an asynchronous data pipeline. It fetches HLTV matches, parses CS2 demos, and executes `INSERT / UPDATE` queries directly against the tables created by `csf-core`. It simply treats the database as an API it writes to.

## 🔄 Core Flow: Joining a League
The backend enforces a strict logical pipeline to prevent empty teams and manage scale:
1. **Registration (`LeagueRegistration`):** An `Account` signs up for a `League`. This acts as a waitlist.
2. **Assignment (`LeaguePool`):** Once registration closes, the backend subdivides registered users into competitive pools of 10.
3. **Drafting (`Roster`):** Users draft their pro players. A `Roster` is created strictly within the context of their assigned `LeaguePool`.

---

## 📂 Project Structure

```
csf-core/
├── app/
│   ├── api/            # FastAPI route handlers (controllers)
│   │   ├── accounts.py
│   │   ├── league_pools.py
│   │   ├── league_registrations.py
│   │   ├── leagues.py
│   │   ├── players.py
│   │   └── rosters.py
│   ├── models/         # SQLAlchemy ORM models (Source of Truth)
│   │   ├── account.py
│   │   ├── game_stats.py
│   │   ├── league.py
│   │   ├── league_pool.py
│   │   ├── league_registration.py
│   │   ├── map.py
│   │   ├── match.py
│   │   ├── player.py
│   │   ├── roster.py
│   │   ├── team.py
│   │   └── tournament.py
│   ├── schemas/        # Pydantic request/response schemas (DTOs)
│   │   ├── account.py
│   │   ├── league.py
│   │   ├── league_pool.py
│   │   ├── league_registration.py
│   │   ├── player.py
│   │   └── roster.py
│   ├── services/       # Business logic layer
│   │   ├── account_service.py
│   │   ├── league_pool_service.py
│   │   ├── league_registration_service.py
│   │   ├── league_service.py
│   │   ├── player_service.py
│   │   └── roster_service.py
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
| `POST`   | `/leagues/`                                 | Create a league                        |
| `GET`    | `/leagues/`                                 | List all leagues                       |
| `GET`    | `/leagues/{id}`                             | Get a league                           |
| `PATCH`  | `/leagues/{id}`                             | Update a league                        |
| `DELETE` | `/leagues/{id}`                             | Delete a league                        |
| `POST`   | `/leagues/{id}/registrations`               | **Join a league** (Registers Account)  |
| `GET`    | `/leagues/{id}/registrations`               | List registered users                  |
| `DELETE` | `/leagues/{id}/registrations/{reg_id}`      | **Leave a league** (Drop out)          |
| `POST`   | `/leagues/{id}/pools`                       | Create a pool subdivision              |
| `GET`    | `/leagues/{id}/pools`                       | List pools within a league             |
| `GET`    | `/leagues/{id}/pools/{pool_id}`             | Get a specific pool                    |
| `PATCH`  | `/leagues/{id}/pools/{pool_id}`             | Update a pool                          |
| `DELETE` | `/leagues/{id}/pools/{pool_id}`             | Delete a pool                          |
| `POST`   | `/pools/{pool_id}/rosters/`                 | **Create a drafted Roster**            |
| `GET`    | `/pools/{pool_id}/rosters/`                 | List all rosters in pool               |
| `GET`    | `/pools/{pool_id}/rosters/{roster_id}`      | Get roster details                     |
| `PATCH`  | `/pools/{pool_id}/rosters/{roster_id}`      | Update a roster                        |
| `DELETE` | `/pools/{pool_id}/rosters/{roster_id}`      | Delete a roster                        |
| `POST`   | `/accounts/`                                | Create an account                      |
| `GET`    | `/accounts/`                                | List all accounts                      |
| `GET`    | `/accounts/{id}`                            | Get account info                       |
| `PATCH`  | `/accounts/{id}`                            | Update account                         |
| `DELETE` | `/accounts/{id}`                            | Deactivate account                     |
| `POST`   | `/players/`                                 | Create a pro player                    |
| `GET`    | `/players/`                                 | List all pro players                   |
| `GET`    | `/players/{id}`                             | Get pro player timeline                |
| `PATCH`  | `/players/{id}`                             | Update a pro player                    |
| `DELETE` | `/players/{id}`                             | Delete a pro player                    |

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
