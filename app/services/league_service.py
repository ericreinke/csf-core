from uuid import UUID

from sqlalchemy.orm import Session

from app.models.league import League
from app.schemas.league import LeagueCreate, LeagueUpdate


def create_league(db: Session, league_data: LeagueCreate) -> League:
    league = League(**league_data.model_dump())
    db.add(league)
    db.commit()
    db.refresh(league)
    return league


def get_league(db: Session, league_id: UUID) -> League | None:
    return db.query(League).filter(League.id == league_id).first()


def get_leagues(db: Session, skip: int = 0, limit: int = 20) -> list[League]:
    return db.query(League).offset(skip).limit(limit).all()


def update_league(db: Session, league_id: UUID, league_data: LeagueUpdate) -> League | None:
    league = get_league(db, league_id)
    if not league:
        return None

    # Only update fields that were explicitly provided
    for field, value in league_data.model_dump(exclude_unset=True).items():
        setattr(league, field, value)

    db.commit()
    db.refresh(league)
    return league


def delete_league(db: Session, league_id: UUID) -> bool:
    league = get_league(db, league_id)
    if not league:
        return False
    db.delete(league)
    db.commit()
    return True
