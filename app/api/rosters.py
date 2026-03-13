from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.roster import RosterCreate, RosterUpdate, RosterResponse
from app.services import roster_service

router = APIRouter(prefix="/rosters", tags=["Rosters"])


@router.post("/", response_model=RosterResponse, status_code=201)
def create_roster(roster_data: RosterCreate, db: Session = Depends(get_db)):
    return roster_service.create_roster(db, roster_data)


@router.get("/", response_model=list[RosterResponse])
def get_rosters(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return roster_service.get_rosters(db, skip=skip, limit=limit)


@router.get("/{roster_id}", response_model=RosterResponse)
def get_roster(roster_id: UUID, db: Session = Depends(get_db)):
    roster = roster_service.get_roster(db, roster_id)
    if not roster:
        raise HTTPException(status_code=404, detail="Roster not found")
    return roster


@router.patch("/{roster_id}", response_model=RosterResponse)
def update_roster(roster_id: UUID, roster_data: RosterUpdate, db: Session = Depends(get_db)):
    roster = roster_service.update_roster(db, roster_id, roster_data)
    if not roster:
        raise HTTPException(status_code=404, detail="Roster not found")
    return roster


@router.delete("/{roster_id}", status_code=204)
def delete_roster(roster_id: UUID, db: Session = Depends(get_db)):
    if not roster_service.delete_roster(db, roster_id):
        raise HTTPException(status_code=404, detail="Roster not found")
