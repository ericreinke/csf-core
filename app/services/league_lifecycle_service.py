"""
League lifecycle service.

Contains three core transition functions:
  - assign_pools_automatically: group unassigned registrations into pools
  - close_registration: OPEN → ACTIVE (auto-assigns pools first)
  - start_draft: ACTIVE → draft phase (marks all POOLED registrations as DRAFTING)

These functions are scheduler-agnostic — they can be called by the polling loop,
manual admin endpoints, or future Cloud Tasks triggers.
"""

import math
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.league import League, LeagueStatus
from app.models.league_pool import LeaguePool
from app.models.league_registration import LeagueRegistration, RegistrationStatus
from app.models.league import generate_uuid7


def assign_pools_automatically(db: Session, league_id: UUID) -> list[LeaguePool]:
    """
    Groups all unassigned (no pool) REGISTERED registrations into pools of league.pool_size.
    Creates the pool rows, assigns registrations, and marks them POOLED.
    Returns the created pools.
    """
    league = db.query(League).filter(League.id == league_id).first()
    if not league:
        raise HTTPException(status_code=404, detail="League not found")

    unassigned = (
        db.query(LeagueRegistration)
        .filter(
            LeagueRegistration.league_id == league_id,
            LeagueRegistration.pool_id == None,  # noqa: E711
            LeagueRegistration.status == RegistrationStatus.REGISTERED,
        )
        .all()
    )

    if not unassigned:
        return []

    pool_size = league.pool_size
    num_pools = math.ceil(len(unassigned) / pool_size)
    created_pools = []

    for i in range(num_pools):
        pool = LeaguePool(
            id=generate_uuid7(),
            league_id=league_id,
            name=f"Pool {i + 1}",
            max_teams=pool_size,
        )
        db.add(pool)
        db.flush()  # get pool.id without full commit

        chunk = unassigned[i * pool_size : (i + 1) * pool_size]
        for registration in chunk:
            registration.pool_id = pool.id
            registration.status = RegistrationStatus.POOLED

        created_pools.append(pool)

    db.commit()
    for pool in created_pools:
        db.refresh(pool)

    return created_pools


def close_registration(db: Session, league_id: UUID) -> League:
    """
    Transitions a league from OPEN → ACTIVE.
    Automatically assigns any unassigned registrations to pools first.
    Raises 400 if the league is not currently OPEN.
    """
    league = db.query(League).filter(League.id == league_id).first()
    if not league:
        raise HTTPException(status_code=404, detail="League not found")
    if league.status != LeagueStatus.OPEN:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot close registration — league is currently {league.status.value}",
        )

    # Auto-assign any unassigned registrations before closing
    assign_pools_automatically(db, league_id)

    league.status = LeagueStatus.ACTIVE
    db.commit()
    db.refresh(league)
    return league


def start_draft(db: Session, league_id: UUID) -> League:
    """
    Begins the draft phase for an ACTIVE league.
    Marks all POOLED registrations as DRAFTING.
    Raises 400 if the league is not currently ACTIVE.
    """
    league = db.query(League).filter(League.id == league_id).first()
    if not league:
        raise HTTPException(status_code=404, detail="League not found")
    if league.status != LeagueStatus.ACTIVE:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot start draft — league is currently {league.status.value}",
        )

    db.query(LeagueRegistration).filter(
        LeagueRegistration.league_id == league_id,
        LeagueRegistration.status == RegistrationStatus.POOLED,
    ).update({"status": RegistrationStatus.DRAFTING})

    db.commit()
    db.refresh(league)
    return league
