from fastapi import FastAPI

from app.api import leagues

app = FastAPI(
    title="CSF Core",
    description="Backend API for Counter-Strike Fantasy league management",
    version="0.1.0",
)

app.include_router(leagues.router)


@app.get("/health")
def health_check():
    """Simple health check endpoint to verify the app is running."""
    return {"status": "ok"}
