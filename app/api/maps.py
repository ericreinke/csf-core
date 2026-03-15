from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.map import MapCreate, MapUpdate, MapResponse
from app.services import map_service

router = APIRouter(prefix="/maps", tags=["Maps"])


# TODO: gate write endpoints with OAuth superuser role check when auth is implemented
@router.post("/", response_model=MapResponse, status_code=201)
def create_map(data: MapCreate, db: Session = Depends(get_db)):
    if data.hltv_id and map_service.get_map_by_hltv(db, data.hltv_id):
        raise HTTPException(status_code=409, detail="Map with this HLTV ID already exists")
    return map_service.create_map(db, data)


@router.get("/", response_model=list[MapResponse])
def get_maps(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return map_service.get_maps(db, skip=skip, limit=limit)


@router.get("/{map_id}", response_model=MapResponse)
def get_map(map_id: UUID, db: Session = Depends(get_db)):
    map_ = map_service.get_map(db, map_id)
    if not map_:
        raise HTTPException(status_code=404, detail="Map not found")
    return map_


@router.patch("/{map_id}", response_model=MapResponse)
def update_map(map_id: UUID, data: MapUpdate, db: Session = Depends(get_db)):
    map_ = map_service.update_map(db, map_id, data)
    if not map_:
        raise HTTPException(status_code=404, detail="Map not found")
    return map_


@router.delete("/{map_id}", status_code=204)
def delete_map(map_id: UUID, db: Session = Depends(get_db)):
    if not map_service.delete_map(db, map_id):
        raise HTTPException(status_code=404, detail="Map not found")
