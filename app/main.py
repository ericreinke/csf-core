from fastapi import FastAPI

from app.api import (
    leagues,
    accounts,
    rosters,
    players,
    league_pools,
    league_registrations,
    teams,
    tournaments,
    matches,
    maps,
    game_stats,
)
from app.middleware import setup_middleware

app = FastAPI(
    title="CSF Core",
    description="Backend API for Counter-Strike Fantasy league management",
    version="0.1.0",
)

setup_middleware(app)

app.include_router(leagues.router)
app.include_router(accounts.router)
app.include_router(rosters.router)
app.include_router(players.router)
app.include_router(league_pools.router)
app.include_router(league_registrations.router)

# Game data (populated by csf-scraper; reads public, writes admin-only)
app.include_router(teams.router)
app.include_router(tournaments.router)
app.include_router(matches.router)
app.include_router(maps.router)
app.include_router(game_stats.router)


@app.get("/health")
def health_check():
    """Simple health check endpoint to verify the app is running."""
    return {"status": "ok"}
