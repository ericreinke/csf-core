"""
Polling loop for automatic league lifecycle transitions.

Runs as an asyncio background task on FastAPI startup.
Every 60 seconds it checks for leagues whose deadlines have passed
and fires the appropriate service functions.

Replace this with Cloud Tasks (or similar) in production for:
  - Exact-time firing instead of up-to-60s delay
  - Cross-instance coordination when running multiple API replicas
"""

import asyncio
import logging
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.league import League, LeagueStatus
from app.services import league_lifecycle_service

logger = logging.getLogger(__name__)

POLL_INTERVAL_SECONDS = 60


async def poll_league_transitions(db_factory) -> None:
    """
    Background task: polls for due league lifecycle transitions.
    Pass the SQLAlchemy session factory (e.g. SessionLocal) as db_factory.
    """
    while True:
        try:
            _process_transitions(db_factory)
        except Exception:
            logger.exception("Error in league lifecycle poller")
        await asyncio.sleep(POLL_INTERVAL_SECONDS)


def _process_transitions(db_factory) -> None:
    db: Session = db_factory()
    now = datetime.now(timezone.utc).replace(tzinfo=None)  # naive UTC to match DB

    try:
        # 1. Close registration for OPEN leagues past their deadline
        due_close = (
            db.query(League)
            .filter(
                League.status == LeagueStatus.OPEN,
                League.registration_deadline != None,  # noqa: E711
                League.registration_deadline <= now,
            )
            .all()
        )
        for league in due_close:
            try:
                league_lifecycle_service.close_registration(db, league.id)
                logger.info("Auto-closed registration for league %s", league.id)
            except Exception:
                logger.exception("Failed to close registration for league %s", league.id)

        # 2. Start draft for ACTIVE leagues past their draft_start_time
        due_draft = (
            db.query(League)
            .filter(
                League.status == LeagueStatus.ACTIVE,
                League.draft_start_time != None,  # noqa: E711
                League.draft_start_time <= now,
            )
            .all()
        )
        for league in due_draft:
            try:
                league_lifecycle_service.start_draft(db, league.id)
                logger.info("Auto-started draft for league %s", league.id)
            except Exception:
                logger.exception("Failed to start draft for league %s", league.id)

    finally:
        db.close()
