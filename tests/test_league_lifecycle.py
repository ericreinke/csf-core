"""
Tests for league lifecycle service functions.

Service functions are tested directly (not via HTTP) since the polling loop
calls them the same way. The manual-trigger API endpoints are tested separately below.
"""

import pytest
from datetime import datetime, timedelta, timezone

from app.models.account import Account
from app.models.league import League, LeagueStatus
from app.models.league_registration import LeagueRegistration, RegistrationStatus
from app.services import league_lifecycle_service


# ── Helpers ───────────────────────────────────────────────────────────────────

def _make_account(db, google_id, email):
    account = Account(google_id=google_id, email=email, display_name=google_id)
    db.add(account)
    db.commit()
    db.refresh(account)
    return account


def _make_league(client, db, owner_id, pool_size=10):
    response = client.post("/leagues/", json={
        "name": "Test League",
        "owner_id": str(owner_id),
        "pool_size": pool_size,
    })
    assert response.status_code == 201
    league_id = response.json()["id"]
    return db.query(League).filter(League.id == league_id).first()


def _register_n_accounts(client, db, league_id, n, prefix="user"):
    """Creates n accounts and registers them to the league."""
    reg_ids = []
    for i in range(n):
        account = _make_account(db, f"{prefix}-{i}-gid", f"{prefix}{i}@test.com")
        resp = client.post(f"/leagues/{league_id}/registrations", json={"account_id": str(account.id)})
        assert resp.status_code == 201
        reg_ids.append(resp.json()["id"])
    return reg_ids


# ── assign_pools_automatically ────────────────────────────────────────────────

def test_assign_pools_chunks_correctly(client, db):
    """23 registrations with pool_size=10 → 3 pools (10 + 10 + 3)."""
    owner = _make_account(db, "owner-pool-gid", "owner-pool@test.com")
    league = _make_league(client, db, owner.id, pool_size=10)
    _register_n_accounts(client, db, league.id, 23)

    pools = league_lifecycle_service.assign_pools_automatically(db, league.id)

    assert len(pools) == 3
    sizes = sorted([p.max_teams for p in pools])
    assert sizes == [10, 10, 10]  # max_teams is set to pool_size for each pool

    # Verify actual registration counts per pool
    from app.models.league_pool import LeaguePool
    pool_ids = [p.id for p in pools]
    counts = [
        db.query(LeagueRegistration).filter(LeagueRegistration.pool_id == pid).count()
        for pid in pool_ids
    ]
    assert sorted(counts) == [3, 10, 10]


def test_assign_pools_marks_registrations_pooled(client, db):
    owner = _make_account(db, "owner-pooled-gid", "owner-pooled@test.com")
    league = _make_league(client, db, owner.id, pool_size=5)
    _register_n_accounts(client, db, league.id, 5)

    league_lifecycle_service.assign_pools_automatically(db, league.id)

    regs = db.query(LeagueRegistration).filter(LeagueRegistration.league_id == league.id).all()
    assert all(r.status == RegistrationStatus.POOLED for r in regs)
    assert all(r.pool_id is not None for r in regs)


def test_assign_pools_no_unassigned(client, db):
    """If all registrations are already pooled, no new pools are created."""
    owner = _make_account(db, "owner-noop-gid", "owner-noop@test.com")
    league = _make_league(client, db, owner.id)
    _register_n_accounts(client, db, league.id, 3)

    # First call assigns pools
    pools_first = league_lifecycle_service.assign_pools_automatically(db, league.id)
    # Second call: nothing left to assign
    pools_second = league_lifecycle_service.assign_pools_automatically(db, league.id)

    assert len(pools_second) == 0


# ── close_registration ────────────────────────────────────────────────────────

def test_close_registration(client, db):
    owner = _make_account(db, "owner-close-gid", "owner-close@test.com")
    league = _make_league(client, db, owner.id, pool_size=5)
    _register_n_accounts(client, db, league.id, 5)

    result = league_lifecycle_service.close_registration(db, league.id)

    assert result.status == LeagueStatus.ACTIVE
    # Auto-assign should have fired
    regs = db.query(LeagueRegistration).filter(LeagueRegistration.league_id == league.id).all()
    assert all(r.status == RegistrationStatus.POOLED for r in regs)


def test_close_registration_wrong_status(client, db):
    from fastapi import HTTPException
    owner = _make_account(db, "owner-wrong-gid", "owner-wrong@test.com")
    league = _make_league(client, db, owner.id)

    # Close once: OK
    league_lifecycle_service.close_registration(db, league.id)

    # Close again: should raise
    with pytest.raises(HTTPException) as exc:
        league_lifecycle_service.close_registration(db, league.id)
    assert exc.value.status_code == 400


# ── start_draft ───────────────────────────────────────────────────────────────

def test_start_draft(client, db):
    owner = _make_account(db, "owner-draft-gid", "owner-draft@test.com")
    league = _make_league(client, db, owner.id, pool_size=5)
    _register_n_accounts(client, db, league.id, 5)

    league_lifecycle_service.close_registration(db, league.id)  # → ACTIVE + POOLED
    league_lifecycle_service.start_draft(db, league.id)

    regs = db.query(LeagueRegistration).filter(LeagueRegistration.league_id == league.id).all()
    assert all(r.status == RegistrationStatus.DRAFTING for r in regs)


def test_start_draft_wrong_status(client, db):
    from fastapi import HTTPException
    owner = _make_account(db, "owner-draft-bad-gid", "owner-draft-bad@test.com")
    league = _make_league(client, db, owner.id)

    with pytest.raises(HTTPException) as exc:
        league_lifecycle_service.start_draft(db, league.id)
    assert exc.value.status_code == 400


# ── Admin endpoint smoke tests ────────────────────────────────────────────────

def test_manual_close_registration_endpoint(client, db):
    owner = _make_account(db, "owner-ep-close-gid", "owner-ep-close@test.com")
    league = _make_league(client, db, owner.id)
    _register_n_accounts(client, db, league.id, 3, prefix="ep-close")

    response = client.post(f"/leagues/{league.id}/close-registration")
    assert response.status_code == 200
    assert response.json()["status"] == "active"


def test_manual_assign_pools_endpoint(client, db):
    owner = _make_account(db, "owner-ep-assign-gid", "owner-ep-assign@test.com")
    league = _make_league(client, db, owner.id, pool_size=5)
    _register_n_accounts(client, db, league.id, 7, prefix="ep-assign")

    response = client.post(f"/leagues/{league.id}/assign-pools")
    assert response.status_code == 200
    assert len(response.json()) == 2  # 5 + 2


def test_manual_start_draft_endpoint(client, db):
    owner = _make_account(db, "owner-ep-draft-gid", "owner-ep-draft@test.com")
    league = _make_league(client, db, owner.id)
    _register_n_accounts(client, db, league.id, 3, prefix="ep-draft")

    client.post(f"/leagues/{league.id}/close-registration")  # → ACTIVE
    response = client.post(f"/leagues/{league.id}/start-draft")
    assert response.status_code == 200
