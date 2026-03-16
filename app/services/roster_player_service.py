from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.roster import Roster
from app.models.roster_player import RosterPlayer
from app.schemas.roster_player import RosterPlayerCreate

MAX_ROSTER_SIZE = 5


def add_player(db: Session, roster: Roster, data: RosterPlayerCreate) -> RosterPlayer:
    """
    Draft a player onto a roster. Enforces:
    - No duplicate: same player can't be on the same roster twice.
    - Pool uniqueness: a player can only be on one roster per pool.
    - Roster size: max MAX_ROSTER_SIZE players per roster.
    """
    # 1. Duplicate check
    existing = (
        db.query(RosterPlayer)
        .filter(RosterPlayer.roster_id == roster.id, RosterPlayer.player_id == data.player_id)
        .first()
    )
    if existing:
        raise HTTPException(status_code=409, detail="Player is already on this roster")

    # 2. Pool uniqueness — player must not be on any other roster in the same pool
    conflict = (
        db.query(RosterPlayer)
        .join(Roster, Roster.id == RosterPlayer.roster_id)
        .filter(
            Roster.pool_id == roster.pool_id,
            RosterPlayer.player_id == data.player_id,
        )
        .first()
    )
    if conflict:
        raise HTTPException(
            status_code=409,
            detail="Player is already drafted on another roster in this pool",
        )

    # 3. Roster size limit
    current_size = (
        db.query(RosterPlayer).filter(RosterPlayer.roster_id == roster.id).count()
    )
    if current_size >= MAX_ROSTER_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"Roster is full (max {MAX_ROSTER_SIZE} players)",
        )

    roster_player = RosterPlayer(roster_id=roster.id, player_id=data.player_id)
    db.add(roster_player)
    db.commit()
    db.refresh(roster_player)
    return roster_player


def get_roster_players(db: Session, roster_id: UUID) -> list[RosterPlayer]:
    return db.query(RosterPlayer).filter(RosterPlayer.roster_id == roster_id).all()


def remove_player(db: Session, roster_id: UUID, player_id: UUID) -> bool:
    roster_player = (
        db.query(RosterPlayer)
        .filter(RosterPlayer.roster_id == roster_id, RosterPlayer.player_id == player_id)
        .first()
    )
    if not roster_player:
        return False
    db.delete(roster_player)
    db.commit()
    return True
