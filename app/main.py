import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import (
    leagues_router,
    accounts_router,
    rosters_router,
    players_router,
    league_pools_router,
    league_registrations_router,
    teams_router,
    tournaments_router,
    matches_router,
    maps_router,
    game_stats_router,
)
from app.api.rosters_router import roster_player_router
from app.middleware import setup_middleware
from app.services.lifecycle_poller import poll_league_transitions
from app.db.session import SessionLocal

@asynccontextmanager
async def lifespan(app):
    """Start background tasks on startup, clean up on shutdown."""
    asyncio.create_task(poll_league_transitions(SessionLocal))
    yield


app = FastAPI(
    title="CSF Core",
    description="Backend API for Counter-Strike Fantasy league management",
    version="0.1.0",
    lifespan=lifespan,
)

setup_middleware(app)

app.include_router(leagues_router.router)
app.include_router(accounts_router.router)
app.include_router(rosters_router.router)
app.include_router(players_router.router)
app.include_router(league_pools_router.router)
app.include_router(league_registrations_router.router)
app.include_router(roster_player_router)

# Game data (populated by csf-scraper; reads public, writes admin-only)
app.include_router(teams_router.router)
app.include_router(tournaments_router.router)
app.include_router(matches_router.router)
app.include_router(maps_router.router)
app.include_router(game_stats_router.router)


@app.get("/health")
def health_check():
    """Simple health check endpoint to verify the app is running."""
    return {"status": "ok"}
