from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.league_registration import LeagueRegistrationCreate, LeagueRegistrationResponse
from app.services import league_registration_service, league_service

router = APIRouter(prefix="/leagues", tags=["League Registrations"])


@router.post("/{league_id}/registrations", response_model=LeagueRegistrationResponse, status_code=201)
def register_for_league(league_id: UUID, registration_data: LeagueRegistrationCreate, db: Session = Depends(get_db)):
    league = league_service.get_league(db, league_id)
    if not league:
        raise HTTPException(status_code=404, detail="League not found")

    registration = league_registration_service.create_registration(db, league_id, registration_data)
    if not registration:
        raise HTTPException(status_code=409, detail="Account is already registered for this league")
    
    return registration


@router.get("/{league_id}/registrations", response_model=list[LeagueRegistrationResponse])
def get_league_registrations(league_id: UUID, skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    league = league_service.get_league(db, league_id)
    if not league:
        raise HTTPException(status_code=404, detail="League not found")
        
    return league_registration_service.get_registrations_by_league(db, league_id, skip=skip, limit=limit)


@router.delete("/{league_id}/registrations/{registration_id}", status_code=204)
def delete_league_registration(league_id: UUID, registration_id: UUID, db: Session = Depends(get_db)):
    # Verify the registration exists and belongs to this league
    registration = league_registration_service.get_registration(db, registration_id)
    if not registration or registration.league_id != league_id:
        raise HTTPException(status_code=404, detail="Registration not found in this league")
        
    league_registration_service.delete_registration(db, registration_id)
