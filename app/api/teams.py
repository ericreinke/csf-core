from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.team import TeamCreate, TeamUpdate, TeamResponse
from app.services import team_service

router = APIRouter(prefix="/teams", tags=["Teams"])


@router.post("/", response_model=TeamResponse, status_code=201)
def create_team(team_data: TeamCreate, db: Session = Depends(get_db)):
    return team_service.create_team(db, team_data)


@router.get("/", response_model=list[TeamResponse])
def get_teams(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return team_service.get_teams(db, skip=skip, limit=limit)


@router.get("/{team_id}", response_model=TeamResponse)
def get_team(team_id: UUID, db: Session = Depends(get_db)):
    team = team_service.get_team(db, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team


@router.patch("/{team_id}", response_model=TeamResponse)
def update_team(team_id: UUID, team_data: TeamUpdate, db: Session = Depends(get_db)):
    team = team_service.update_team(db, team_id, team_data)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team


@router.delete("/{team_id}", status_code=204)
def delete_team(team_id: UUID, db: Session = Depends(get_db)):
    if not team_service.delete_team(db, team_id):
        raise HTTPException(status_code=404, detail="Team not found")
