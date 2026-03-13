from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.roster import RosterCreate, RosterUpdate, RosterResponse
from app.services import roster_service, league_pool_service, league_registration_service

router = APIRouter(prefix="/pools", tags=["Rosters"])


@router.post("/{pool_id}/rosters", response_model=RosterResponse, status_code=201)
def create_roster(pool_id: UUID, roster_data: RosterCreate, db: Session = Depends(get_db)):
    # 1. Verify pool exists
    pool = league_pool_service.get_pool(db, pool_id)
    if not pool:
        raise HTTPException(status_code=404, detail="Pool not found")
        
    # 2. Verify registration exists
    registration = league_registration_service.get_registration(db, roster_data.registration_id)
    if not registration:
        raise HTTPException(status_code=404, detail="Registration not found")
        
    # 3. Verify the registration belongs to this pool!
    if registration.pool_id != pool_id:
        raise HTTPException(status_code=400, detail="Registration is not assigned to this pool")
        
    return roster_service.create_roster(db, pool_id, roster_data)


@router.get("/{pool_id}/rosters", response_model=list[RosterResponse])
def get_rosters(pool_id: UUID, skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    pool = league_pool_service.get_pool(db, pool_id)
    if not pool:
        raise HTTPException(status_code=404, detail="Pool not found")
        
    return roster_service.get_rosters_by_pool(db, pool_id, skip=skip, limit=limit)


@router.get("/{pool_id}/rosters/{roster_id}", response_model=RosterResponse)
def get_roster(pool_id: UUID, roster_id: UUID, db: Session = Depends(get_db)):
    roster = roster_service.get_roster(db, roster_id)
    if not roster or roster.pool_id != pool_id:
        raise HTTPException(status_code=404, detail="Roster not found in this pool")
    return roster


@router.patch("/{pool_id}/rosters/{roster_id}", response_model=RosterResponse)
def update_roster(pool_id: UUID, roster_id: UUID, roster_data: RosterUpdate, db: Session = Depends(get_db)):
    roster = roster_service.get_roster(db, roster_id)
    if not roster or roster.pool_id != pool_id:
        raise HTTPException(status_code=404, detail="Roster not found in this pool")
        
    return roster_service.update_roster(db, roster_id, roster_data)


@router.delete("/{pool_id}/rosters/{roster_id}", status_code=204)
def delete_roster(pool_id: UUID, roster_id: UUID, db: Session = Depends(get_db)):
    roster = roster_service.get_roster(db, roster_id)
    if not roster or roster.pool_id != pool_id:
        raise HTTPException(status_code=404, detail="Roster not found in this pool")
        
    roster_service.delete_roster(db, roster_id)
