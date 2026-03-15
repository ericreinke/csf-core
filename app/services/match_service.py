from uuid import UUID

from sqlalchemy.orm import Session

from app.models.match import Match
from app.schemas.match import MatchCreate, MatchUpdate


def create_match(db: Session, data: MatchCreate) -> Match:
    db_obj_data = data.model_dump(exclude_unset=True)
    match = Match(**db_obj_data)
    db.add(match)
    db.commit()
    db.refresh(match)
    return match


def get_match(db: Session, match_id: UUID) -> Match | None:
    return db.query(Match).filter(Match.id == match_id).first()


def get_match_by_hltv(db: Session, hltv_id: int) -> Match | None:
    return db.query(Match).filter(Match.hltv_id == hltv_id).first()


def get_matches(db: Session, skip: int = 0, limit: int = 50) -> list[Match]:
    return db.query(Match).offset(skip).limit(limit).all()


def update_match(db: Session, match_id: UUID, data: MatchUpdate) -> Match | None:
    match = get_match(db, match_id)
    if not match:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(match, field, value)
    db.commit()
    db.refresh(match)
    return match


def delete_match(db: Session, match_id: UUID) -> bool:
    match = get_match(db, match_id)
    if not match:
        return False
    db.delete(match)
    db.commit()
    return True
