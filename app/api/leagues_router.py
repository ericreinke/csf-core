from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.league import LeagueCreate, LeagueUpdate, LeagueResponse
from app.services import league_service

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
