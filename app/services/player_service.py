from uuid import UUID

from sqlalchemy.orm import Session

from app.models.player import Player
from app.schemas.player import PlayerCreate, PlayerUpdate


def create_player(db: Session, player_data: PlayerCreate) -> Player:
    db_obj_data = player_data.model_dump(exclude_unset=True)
    player = Player(**db_obj_data)
    db.add(player)
    db.commit()
    db.refresh(player)
    return player


def get_player(db: Session, player_id: UUID) -> Player | None:
    return db.query(Player).filter(Player.id == player_id).first()


def get_player_by_hltv(db: Session, hltv_id: int) -> Player | None:
    return db.query(Player).filter(Player.hltv_id == hltv_id).first()


def get_player_by_steam(db: Session, steam_id: int) -> Player | None:
    return db.query(Player).filter(Player.steam_id == steam_id).first()


def get_players(db: Session, skip: int = 0, limit: int = 20) -> list[Player]:
    return db.query(Player).offset(skip).limit(limit).all()


def update_player(db: Session, player_id: UUID, player_data: PlayerUpdate) -> Player | None:
    player = get_player(db, player_id)
    if not player:
        return None

    for field, value in player_data.model_dump(exclude_unset=True).items():
        setattr(player, field, value)

    db.commit()
    db.refresh(player)
    return player


def delete_player(db: Session, player_id: UUID) -> bool:
    player = get_player(db, player_id)
    if not player:
        return False
    db.delete(player)
    db.commit()
    return True
