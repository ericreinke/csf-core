from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.tournament import TournamentCreate, TournamentUpdate, TournamentResponse
from app.services import tournament_service

router = APIRouter(prefix="/tournaments", tags=["Tournaments"])


# TODO: gate write endpoints with OAuth superuser role check when auth is implemented
@router.post("/", response_model=TournamentResponse, status_code=201)
def create_tournament(data: TournamentCreate, db: Session = Depends(get_db)):
    if data.hltv_id and tournament_service.get_tournament_by_hltv(db, data.hltv_id):
        raise HTTPException(status_code=409, detail="Tournament with this HLTV ID already exists")
    return tournament_service.create_tournament(db, data)


@router.get("/", response_model=list[TournamentResponse])
def get_tournaments(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return tournament_service.get_tournaments(db, skip=skip, limit=limit)


@router.get("/{tournament_id}", response_model=TournamentResponse)
def get_tournament(tournament_id: UUID, db: Session = Depends(get_db)):
    tournament = tournament_service.get_tournament(db, tournament_id)
    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")
    return tournament


@router.patch("/{tournament_id}", response_model=TournamentResponse)
def update_tournament(tournament_id: UUID, data: TournamentUpdate, db: Session = Depends(get_db)):
    tournament = tournament_service.update_tournament(db, tournament_id, data)
    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")
    return tournament


@router.delete("/{tournament_id}", status_code=204)
def delete_tournament(tournament_id: UUID, db: Session = Depends(get_db)):
    if not tournament_service.delete_tournament(db, tournament_id):
        raise HTTPException(status_code=404, detail="Tournament not found")
