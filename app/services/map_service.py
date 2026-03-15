from uuid import UUID

from sqlalchemy.orm import Session

from app.models.map import Map
from app.schemas.map import MapCreate, MapUpdate


def create_map(db: Session, data: MapCreate) -> Map:
    db_obj_data = data.model_dump(exclude_unset=True)
    map_ = Map(**db_obj_data)
    db.add(map_)
    db.commit()
    db.refresh(map_)
    return map_


def get_map(db: Session, map_id: UUID) -> Map | None:
    return db.query(Map).filter(Map.id == map_id).first()


def get_map_by_hltv(db: Session, hltv_id: int) -> Map | None:
    return db.query(Map).filter(Map.hltv_id == hltv_id).first()


def get_maps(db: Session, skip: int = 0, limit: int = 50) -> list[Map]:
    return db.query(Map).offset(skip).limit(limit).all()


def update_map(db: Session, map_id: UUID, data: MapUpdate) -> Map | None:
    map_ = get_map(db, map_id)
    if not map_:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(map_, field, value)
    db.commit()
    db.refresh(map_)
    return map_


def delete_map(db: Session, map_id: UUID) -> bool:
    map_ = get_map(db, map_id)
    if not map_:
        return False
    db.delete(map_)
    db.commit()
    return True
