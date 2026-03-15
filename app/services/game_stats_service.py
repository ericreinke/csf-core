from uuid import UUID

from sqlalchemy.orm import Session

from app.models.game_stats import GameStats
from app.schemas.game_stats import GameStatsCreate, GameStatsUpdate


def create_game_stats(db: Session, data: GameStatsCreate) -> GameStats:
    db_obj_data = data.model_dump(exclude_unset=True)
    game_stats = GameStats(**db_obj_data)
    db.add(game_stats)
    db.commit()
    db.refresh(game_stats)
    return game_stats


def get_game_stats(db: Session, game_stats_id: UUID) -> GameStats | None:
    return db.query(GameStats).filter(GameStats.id == game_stats_id).first()


def get_game_stats_list(
    db: Session,
    player_uuid: UUID | None = None,
    map_uuid: UUID | None = None,
    skip: int = 0,
    limit: int = 50,
) -> list[GameStats]:
    query = db.query(GameStats)
    if player_uuid:
        query = query.filter(GameStats.player_uuid == player_uuid)
    if map_uuid:
        query = query.filter(GameStats.map_uuid == map_uuid)
    return query.offset(skip).limit(limit).all()


def update_game_stats(db: Session, game_stats_id: UUID, data: GameStatsUpdate) -> GameStats | None:
    game_stats = get_game_stats(db, game_stats_id)
    if not game_stats:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(game_stats, field, value)
    db.commit()
    db.refresh(game_stats)
    return game_stats


def delete_game_stats(db: Session, game_stats_id: UUID) -> bool:
    game_stats = get_game_stats(db, game_stats_id)
    if not game_stats:
        return False
    db.delete(game_stats)
    db.commit()
    return True
