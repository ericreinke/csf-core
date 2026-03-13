from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.league_registration import LeagueRegistration
from app.schemas.league_registration import LeagueRegistrationCreate


def create_registration(db: Session, league_id: UUID, registration_data: LeagueRegistrationCreate) -> LeagueRegistration | None:
    registration = LeagueRegistration(
        league_id=league_id,
        account_id=registration_data.account_id
    )
    db.add(registration)
    try:
        db.commit()
        db.refresh(registration)
        return registration
    except IntegrityError:
        # Catches the unique constraint uq_account_league_registration
        db.rollback()
        return None


def get_registration(db: Session, registration_id: UUID) -> LeagueRegistration | None:
    return db.query(LeagueRegistration).filter(LeagueRegistration.id == registration_id).first()


def get_registrations_by_league(db: Session, league_id: UUID, skip: int = 0, limit: int = 50) -> list[LeagueRegistration]:
    return db.query(LeagueRegistration).filter(LeagueRegistration.league_id == league_id).offset(skip).limit(limit).all()


def assign_pool(db: Session, registration_id: UUID, pool_id: UUID) -> LeagueRegistration | None:
    """Admin function to move a registration into a specific pool."""
    registration = get_registration(db, registration_id)
    if not registration:
        return None
        
    registration.pool_id = pool_id
    registration.status = "POOLED"
    db.commit()
    db.refresh(registration)
    return registration


def delete_registration(db: Session, registration_id: UUID) -> bool:
    registration = get_registration(db, registration_id)
    if not registration:
        return False
    db.delete(registration)
    db.commit()
    return True
