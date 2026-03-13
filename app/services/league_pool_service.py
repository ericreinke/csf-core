from uuid import UUID

from sqlalchemy.orm import Session

from app.models.league_pool import LeaguePool
from app.schemas.league_pool import LeaguePoolCreate, LeaguePoolUpdate


def create_pool(db: Session, pool_data: LeaguePoolCreate) -> LeaguePool:
    db_obj_data = pool_data.model_dump(exclude_unset=True)
    pool = LeaguePool(**db_obj_data)
    db.add(pool)
    db.commit()
    db.refresh(pool)
    return pool


def get_pool(db: Session, pool_id: UUID) -> LeaguePool | None:
    return db.query(LeaguePool).filter(LeaguePool.id == pool_id).first()


def get_pools_by_league(db: Session, league_id: UUID, skip: int = 0, limit: int = 20) -> list[LeaguePool]:
    return db.query(LeaguePool).filter(LeaguePool.league_id == league_id).offset(skip).limit(limit).all()


def update_pool(db: Session, pool_id: UUID, pool_data: LeaguePoolUpdate) -> LeaguePool | None:
    pool = get_pool(db, pool_id)
    if not pool:
        return None

    for field, value in pool_data.model_dump(exclude_unset=True).items():
        setattr(pool, field, value)

    db.commit()
    db.refresh(pool)
    return pool


def delete_pool(db: Session, pool_id: UUID) -> bool:
    pool = get_pool(db, pool_id)
    if not pool:
        return False
    db.delete(pool)
    db.commit()
    return True
