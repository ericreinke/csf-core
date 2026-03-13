from fastapi import FastAPI

from app.api import leagues, accounts, rosters
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


@app.get("/health")
def health_check():
    """Simple health check endpoint to verify the app is running."""
    return {"status": "ok"}
