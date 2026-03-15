from uuid import UUID

from sqlalchemy.orm import Session

from app.models.tournament import Tournament
from app.schemas.tournament import TournamentCreate, TournamentUpdate


def create_tournament(db: Session, data: TournamentCreate) -> Tournament:
    db_obj_data = data.model_dump(exclude_unset=True)
    tournament = Tournament(**db_obj_data)
    db.add(tournament)
    db.commit()
    db.refresh(tournament)
    return tournament


def get_tournament(db: Session, tournament_id: UUID) -> Tournament | None:
    return db.query(Tournament).filter(Tournament.id == tournament_id).first()


def get_tournament_by_hltv(db: Session, hltv_id: int) -> Tournament | None:
    return db.query(Tournament).filter(Tournament.hltv_id == hltv_id).first()


def get_tournaments(db: Session, skip: int = 0, limit: int = 50) -> list[Tournament]:
    return db.query(Tournament).offset(skip).limit(limit).all()


def update_tournament(db: Session, tournament_id: UUID, data: TournamentUpdate) -> Tournament | None:
    tournament = get_tournament(db, tournament_id)
    if not tournament:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(tournament, field, value)
    db.commit()
    db.refresh(tournament)
    return tournament


def delete_tournament(db: Session, tournament_id: UUID) -> bool:
    tournament = get_tournament(db, tournament_id)
    if not tournament:
        return False
    db.delete(tournament)
    db.commit()
    return True
