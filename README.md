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
│   │   ├── game_stats.py
│   │   ├── league_pools.py
│   │   ├── league_registrations.py
│   │   ├── leagues.py
│   │   ├── maps.py
│   │   ├── matches.py
│   │   ├── players.py
│   │   ├── rosters.py
│   │   ├── teams.py
│   │   └── tournaments.py
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
│   │   ├── roster_player.py
│   │   ├── team.py
│   │   └── tournament.py
│   ├── schemas/        # Pydantic request/response schemas (DTOs)
│   │   ├── account.py
│   │   ├── game_stats.py
│   │   ├── league.py
│   │   ├── league_pool.py
│   │   ├── league_registration.py
│   │   ├── map.py
│   │   ├── match.py
│   │   ├── player.py
│   │   ├── roster.py
│   │   ├── roster_player.py
│   │   ├── team.py
│   │   └── tournament.py
│   ├── services/       # Business logic layer
│   │   ├── account_service.py
│   │   ├── game_stats_service.py
│   │   ├── league_pool_service.py
│   │   ├── league_registration_service.py
│   │   ├── league_service.py
│   │   ├── map_service.py
│   │   ├── match_service.py
│   │   ├── player_service.py
│   │   ├── roster_player_service.py
│   │   ├── roster_service.py
│   │   ├── team_service.py
│   │   └── tournament_service.py
│   ├── dependencies/   # Reusable FastAPI dependencies
│   │   └── admin.py    # Placeholder for future OAuth superuser check
│   ├── db/             # Database session & connection config
│   │   ├── base.py
│   │   └── session.py
│   ├── config.py       # App configuration (env vars)
│   └── main.py         # Application entrypoint
├── alembic/            # Database migrations
├── tests/              # Test suite
│   ├── conftest.py     # Test fixtures & DB setup
│   ├── test_accounts.py
│   ├── test_game_stats.py
│   ├── test_league_pools.py
│   ├── test_league_registrations.py
│   ├── test_leagues.py
│   ├── test_maps.py
│   ├── test_matches.py
│   ├── test_players.py
│   ├── test_roster_players.py
│   ├── test_rosters.py
│   ├── test_teams.py
│   └── test_tournaments.py
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
| `GET`    | `/pools/{pool_id}/rosters/{roster_id}`      | Get roster details (includes players)  |
| `PATCH`  | `/pools/{pool_id}/rosters/{roster_id}`      | Update a roster                        |
| `DELETE` | `/pools/{pool_id}/rosters/{roster_id}`      | Delete a roster                        |
| `POST`   | `/rosters/{roster_id}/players/`             | **Draft a player onto a roster**       |
| `GET`    | `/rosters/{roster_id}/players/`             | List players on a roster               |
| `DELETE` | `/rosters/{roster_id}/players/{player_id}`  | **Drop a player from a roster**        |
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

### Game Data Endpoints

These tables are primarily populated by **csf-scraper**. All endpoints are currently open; write access (POST/PATCH/DELETE) will be gated behind an OAuth superuser role once authentication is implemented.

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST`   | `/teams/`                         | Create a team                     |
| `GET`    | `/teams/`                         | List all teams                    |
| `GET`    | `/teams/{id}`                     | Get a team                        |
| `PATCH`  | `/teams/{id}`                     | Update a team                     |
| `DELETE` | `/teams/{id}`                     | Delete a team                     |
| `POST`   | `/tournaments/`                   | Create a tournament               |
| `GET`    | `/tournaments/`                   | List all tournaments              |
| `GET`    | `/tournaments/{id}`               | Get a tournament                  |
| `PATCH`  | `/tournaments/{id}`               | Update a tournament               |
| `DELETE` | `/tournaments/{id}`               | Delete a tournament               |
| `POST`   | `/matches/`                       | Create a match                    |
| `GET`    | `/matches/`                       | List all matches                  |
| `GET`    | `/matches/{id}`                   | Get a match                       |
| `PATCH`  | `/matches/{id}`                   | Update a match (e.g. demo status) |
| `DELETE` | `/matches/{id}`                   | Delete a match                    |
| `POST`   | `/maps/`                          | Create a map                      |
| `GET`    | `/maps/`                          | List all maps                     |
| `GET`    | `/maps/{id}`                      | Get a map                         |
| `PATCH`  | `/maps/{id}`                      | Update a map (e.g. parse status)  |
| `DELETE` | `/maps/{id}`                      | Delete a map                      |
| `POST`   | `/game-stats/`                    | Create game stats entry           |
| `GET`    | `/game-stats/?player_uuid=&map_uuid=` | List stats (filterable)       |
| `GET`    | `/game-stats/{id}`                | Get a game stats entry            |
| `PATCH`  | `/game-stats/{id}`                | Update game stats                 |
| `DELETE` | `/game-stats/{id}`                | Delete game stats                 |

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
