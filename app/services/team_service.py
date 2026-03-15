from uuid import UUID

from sqlalchemy.orm import Session

from app.models.team import Team
from app.schemas.team import TeamCreate, TeamUpdate


def create_team(db: Session, team_data: TeamCreate) -> Team:
    db_obj_data = team_data.model_dump(exclude_unset=True)
    team = Team(**db_obj_data)
    db.add(team)
    db.commit()
    db.refresh(team)
    return team


def get_team(db: Session, team_id: UUID) -> Team | None:
    return db.query(Team).filter(Team.id == team_id).first()


def get_team_by_hltv(db: Session, hltv_id: int) -> Team | None:
    return db.query(Team).filter(Team.hltv_id == hltv_id).first()


def get_teams(db: Session, skip: int = 0, limit: int = 50) -> list[Team]:
    return db.query(Team).offset(skip).limit(limit).all()


def update_team(db: Session, team_id: UUID, team_data: TeamUpdate) -> Team | None:
    team = get_team(db, team_id)
    if not team:
        return None
    for field, value in team_data.model_dump(exclude_unset=True).items():
        setattr(team, field, value)
    db.commit()
    db.refresh(team)
    return team


def delete_team(db: Session, team_id: UUID) -> bool:
    team = get_team(db, team_id)
    if not team:
        return False
    db.delete(team)
    db.commit()
    return True
