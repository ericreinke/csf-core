from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.league import LeagueCreate, LeagueUpdate, LeagueResponse
from app.services import league_service, league_lifecycle_service

router = APIRouter(prefix="/leagues", tags=["Leagues"])


@router.post("/", response_model=LeagueResponse, status_code=201)
def create_league(league_data: LeagueCreate, db: Session = Depends(get_db)):
    return league_service.create_league(db, league_data)


@router.get("/", response_model=list[LeagueResponse])
def get_leagues(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return league_service.get_leagues(db, skip=skip, limit=limit)


@router.get("/{league_id}", response_model=LeagueResponse)
def get_league(league_id: UUID, db: Session = Depends(get_db)):
    league = league_service.get_league(db, league_id)
    if not league:
        raise HTTPException(status_code=404, detail="League not found")
    return league


@router.patch("/{league_id}", response_model=LeagueResponse)
def update_league(league_id: UUID, league_data: LeagueUpdate, db: Session = Depends(get_db)):
    league = league_service.update_league(db, league_id, league_data)
    if not league:
        raise HTTPException(status_code=404, detail="League not found")
    return league


@router.delete("/{league_id}", status_code=204)
def delete_league(league_id: UUID, db: Session = Depends(get_db)):
    if not league_service.delete_league(db, league_id):
        raise HTTPException(status_code=404, detail="League not found")


# ── Lifecycle admin endpoints ─────────────────────────────────────────────────
# TODO: gate these behind OAuth superuser role when auth is implemented.
# These endpoints also serve as the future Cloud Tasks HTTP targets.

@router.post("/{league_id}/close-registration", response_model=LeagueResponse)
def close_registration(league_id: UUID, db: Session = Depends(get_db)):
    """Manually close registration and auto-assign pools. Also called by polling loop."""
    return league_lifecycle_service.close_registration(db, league_id)


@router.post("/{league_id}/assign-pools", response_model=list[dict])
def assign_pools(league_id: UUID, db: Session = Depends(get_db)):
    """Manually re-run pool assignment for any remaining unassigned registrations."""
    pools = league_lifecycle_service.assign_pools_automatically(db, league_id)
    return [{"id": str(p.id), "name": p.name} for p in pools]


@router.post("/{league_id}/start-draft", response_model=LeagueResponse)
def start_draft(league_id: UUID, db: Session = Depends(get_db)):
    """Manually start the draft phase. Also called by polling loop."""
    return league_lifecycle_service.start_draft(db, league_id)

