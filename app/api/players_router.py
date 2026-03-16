from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.player import PlayerCreate, PlayerUpdate, PlayerResponse
from app.services import player_service

router = APIRouter(prefix="/players", tags=["Players"])


@router.post("/", response_model=PlayerResponse, status_code=201)
def create_player(player_data: PlayerCreate, db: Session = Depends(get_db)):
    if player_data.hltv_id and player_service.get_player_by_hltv(db, player_data.hltv_id):
        raise HTTPException(status_code=409, detail="Player with this HLTV ID already exists")
        
    if player_data.steam_id and player_service.get_player_by_steam(db, player_data.steam_id):
        raise HTTPException(status_code=409, detail="Player with this Steam ID already exists")
        
    return player_service.create_player(db, player_data)


@router.get("/", response_model=list[PlayerResponse])
def get_players(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return player_service.get_players(db, skip=skip, limit=limit)


@router.get("/{player_id}", response_model=PlayerResponse)
def get_player(player_id: UUID, db: Session = Depends(get_db)):
    player = player_service.get_player(db, player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player


@router.patch("/{player_id}", response_model=PlayerResponse)
def update_player(player_id: UUID, player_data: PlayerUpdate, db: Session = Depends(get_db)):
    player = player_service.update_player(db, player_id, player_data)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player


@router.delete("/{player_id}", status_code=204)
def delete_player(player_id: UUID, db: Session = Depends(get_db)):
    if not player_service.delete_player(db, player_id):
        raise HTTPException(status_code=404, detail="Player not found")
