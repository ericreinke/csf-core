from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.match import MatchCreate, MatchUpdate, MatchResponse
from app.services import match_service

router = APIRouter(prefix="/matches", tags=["Matches"])


# TODO: gate write endpoints with OAuth superuser role check when auth is implemented
@router.post("/", response_model=MatchResponse, status_code=201)
def create_match(data: MatchCreate, db: Session = Depends(get_db)):
    if data.hltv_id and match_service.get_match_by_hltv(db, data.hltv_id):
        raise HTTPException(status_code=409, detail="Match with this HLTV ID already exists")
    return match_service.create_match(db, data)


@router.get("/", response_model=list[MatchResponse])
def get_matches(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return match_service.get_matches(db, skip=skip, limit=limit)


@router.get("/{match_id}", response_model=MatchResponse)
def get_match(match_id: UUID, db: Session = Depends(get_db)):
    match = match_service.get_match(db, match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    return match


@router.patch("/{match_id}", response_model=MatchResponse)
def update_match(match_id: UUID, data: MatchUpdate, db: Session = Depends(get_db)):
    match = match_service.update_match(db, match_id, data)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    return match


@router.delete("/{match_id}", status_code=204)
def delete_match(match_id: UUID, db: Session = Depends(get_db)):
    if not match_service.delete_match(db, match_id):
        raise HTTPException(status_code=404, detail="Match not found")
