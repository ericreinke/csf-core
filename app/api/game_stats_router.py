from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.game_stats import GameStatsCreate, GameStatsUpdate, GameStatsResponse
from app.services import game_stats_service

router = APIRouter(prefix="/game-stats", tags=["Game Stats"])


# TODO: gate write endpoints with OAuth superuser role check when auth is implemented
@router.post("/", response_model=GameStatsResponse, status_code=201)
def create_game_stats(data: GameStatsCreate, db: Session = Depends(get_db)):
    return game_stats_service.create_game_stats(db, data)


@router.get("/", response_model=list[GameStatsResponse])
def get_game_stats_list(
    player_uuid: Optional[UUID] = None,
    map_uuid: Optional[UUID] = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
):
    return game_stats_service.get_game_stats_list(
        db, player_uuid=player_uuid, map_uuid=map_uuid, skip=skip, limit=limit
    )


@router.get("/{game_stats_id}", response_model=GameStatsResponse)
def get_game_stats(game_stats_id: UUID, db: Session = Depends(get_db)):
    gs = game_stats_service.get_game_stats(db, game_stats_id)
    if not gs:
        raise HTTPException(status_code=404, detail="Game stats not found")
    return gs


@router.patch("/{game_stats_id}", response_model=GameStatsResponse)
def update_game_stats(game_stats_id: UUID, data: GameStatsUpdate, db: Session = Depends(get_db)):
    gs = game_stats_service.update_game_stats(db, game_stats_id, data)
    if not gs:
        raise HTTPException(status_code=404, detail="Game stats not found")
    return gs


@router.delete("/{game_stats_id}", status_code=204)
def delete_game_stats(game_stats_id: UUID, db: Session = Depends(get_db)):
    if not game_stats_service.delete_game_stats(db, game_stats_id):
        raise HTTPException(status_code=404, detail="Game stats not found")
