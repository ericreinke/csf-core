from uuid import UUID

from sqlalchemy.orm import Session

from app.models.roster import Roster
from app.schemas.roster import RosterCreate, RosterUpdate


def create_roster(db: Session, roster_data: RosterCreate) -> Roster:
    roster = Roster(**roster_data.model_dump())
    db.add(roster)
    db.commit()
    db.refresh(roster)
    return roster


def get_roster(db: Session, roster_id: UUID) -> Roster | None:
    return db.query(Roster).filter(Roster.id == roster_id).first()


def get_rosters(db: Session, skip: int = 0, limit: int = 20) -> list[Roster]:
    return db.query(Roster).offset(skip).limit(limit).all()


def get_rosters_by_league(db: Session, league_id: UUID, skip: int = 0, limit: int = 20) -> list[Roster]:
    return db.query(Roster).filter(Roster.league_id == league_id).offset(skip).limit(limit).all()


def update_roster(db: Session, roster_id: UUID, roster_data: RosterUpdate) -> Roster | None:
    roster = get_roster(db, roster_id)
    if not roster:
        return None

    # Only update fields that were explicitly provided
    for field, value in roster_data.model_dump(exclude_unset=True).items():
        setattr(roster, field, value)

    db.commit()
    db.refresh(roster)
    return roster


def delete_roster(db: Session, roster_id: UUID) -> bool:
    roster = get_roster(db, roster_id)
    if not roster:
        return False
    db.delete(roster)
    db.commit()
    return True
