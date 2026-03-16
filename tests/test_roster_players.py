import pytest
from app.models.account import Account
from app.services.roster_player_service import MAX_ROSTER_SIZE


def _create_account(db, google_id="rp-google-id", email="rp@test.com", display_name="RP Test"):
    account = Account(google_id=google_id, email=email, display_name=display_name)
    db.add(account)
    db.commit()
    db.refresh(account)
    return account


def _setup_environment(client, db):
    """Creates Account → League → Registration → Pool → Roster."""
    account = _create_account(db)
    league_id = client.post("/leagues/", json={"name": "RP League", "owner_id": str(account.id)}).json()["id"]
    reg_id = client.post(f"/leagues/{league_id}/registrations", json={"account_id": str(account.id)}).json()["id"]
    pool_id = client.post(f"/leagues/{league_id}/pools", json={"league_id": league_id, "name": "Pool 1"}).json()["id"]

    from app.services.league_registration_service import assign_pool
    assign_pool(db, reg_id, pool_id)

    roster_id = client.post(
        f"/pools/{pool_id}/rosters",
        json={"name": "Test Roster", "registration_id": str(reg_id), "owner_id": str(account.id)},
    ).json()["id"]

    return account, league_id, reg_id, pool_id, roster_id


def _make_player(client, name="ZywOo"):
    return client.post("/players/", json={"user_name": name}).json()["id"]


# ── Happy path ────────────────────────────────────────────────────────────────

def test_add_player_to_roster(client, db):
    _, _, _, _, roster_id = _setup_environment(client, db)
    player_id = _make_player(client)

    response = client.post(f"/rosters/{roster_id}/players", json={"player_id": player_id})
    assert response.status_code == 201
    data = response.json()
    assert data["player_id"] == player_id
    assert data["roster_id"] == roster_id


def test_get_roster_players(client, db):
    _, _, _, _, roster_id = _setup_environment(client, db)
    player_id = _make_player(client, "s1mple")

    client.post(f"/rosters/{roster_id}/players", json={"player_id": player_id})

    response = client.get(f"/rosters/{roster_id}/players")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["player_id"] == player_id


def test_roster_response_includes_players(client, db):
    """GET /pools/{pool_id}/rosters/{roster_id} should embed the players list."""
    _, _, _, pool_id, roster_id = _setup_environment(client, db)
    player_id = _make_player(client, "NiKo")
    client.post(f"/rosters/{roster_id}/players", json={"player_id": player_id})

    response = client.get(f"/pools/{pool_id}/rosters/{roster_id}")
    assert response.status_code == 200
    players = response.json()["players"]
    assert len(players) == 1
    assert players[0]["player_id"] == player_id


def test_remove_player_from_roster(client, db):
    _, _, _, _, roster_id = _setup_environment(client, db)
    player_id = _make_player(client, "device")

    client.post(f"/rosters/{roster_id}/players", json={"player_id": player_id})
    response = client.delete(f"/rosters/{roster_id}/players/{player_id}")
    assert response.status_code == 204

    remaining = client.get(f"/rosters/{roster_id}/players").json()
    assert len(remaining) == 0


# ── Constraint: duplicate ─────────────────────────────────────────────────────

def test_add_duplicate_player(client, db):
    _, _, _, _, roster_id = _setup_environment(client, db)
    player_id = _make_player(client, "ropz")

    client.post(f"/rosters/{roster_id}/players", json={"player_id": player_id})
    response = client.post(f"/rosters/{roster_id}/players", json={"player_id": player_id})
    assert response.status_code == 409
    assert "already on this roster" in response.json()["detail"]


# ── Constraint: pool uniqueness ───────────────────────────────────────────────

def test_pool_uniqueness(client, db):
    """Same player cannot be on two rosters in the same pool."""
    account, league_id, _, pool_id, roster_id_1 = _setup_environment(client, db)

    # Create a second account + registration + roster in the same pool
    account2 = _create_account(db, google_id="acc2-google", email="acc2@test.com", display_name="Account 2")
    reg2_id = client.post(f"/leagues/{league_id}/registrations", json={"account_id": str(account2.id)}).json()["id"]
    from app.services.league_registration_service import assign_pool
    assign_pool(db, reg2_id, pool_id)
    roster_id_2 = client.post(
        f"/pools/{pool_id}/rosters",
        json={"name": "Roster 2", "registration_id": str(reg2_id), "owner_id": str(account2.id)},
    ).json()["id"]

    player_id = _make_player(client, "m0NESY")

    # Draft player onto roster 1
    client.post(f"/rosters/{roster_id_1}/players", json={"player_id": player_id})

    # Try to draft same player onto roster 2 — same pool
    response = client.post(f"/rosters/{roster_id_2}/players", json={"player_id": player_id})
    assert response.status_code == 409
    assert "another roster in this pool" in response.json()["detail"]


# ── Constraint: roster size limit ─────────────────────────────────────────────

def test_roster_size_limit(client, db):
    _, _, _, _, roster_id = _setup_environment(client, db)

    for i in range(MAX_ROSTER_SIZE):
        pid = _make_player(client, f"player_{i}")
        r = client.post(f"/rosters/{roster_id}/players", json={"player_id": pid})
        assert r.status_code == 201

    # One more should be rejected
    overflow_pid = _make_player(client, "overflow_player")
    response = client.post(f"/rosters/{roster_id}/players", json={"player_id": overflow_pid})
    assert response.status_code == 400
    assert "full" in response.json()["detail"]


# ── 404 cases ─────────────────────────────────────────────────────────────────

def test_add_player_roster_not_found(client, db):
    import uuid
    player_id = _make_player(client)
    response = client.post(f"/rosters/{uuid.uuid4()}/players", json={"player_id": player_id})
    assert response.status_code == 404


def test_add_player_player_not_found(client, db):
    import uuid
    _, _, _, _, roster_id = _setup_environment(client, db)
    response = client.post(f"/rosters/{roster_id}/players", json={"player_id": str(uuid.uuid4())})
    assert response.status_code == 404


def test_remove_player_not_found(client, db):
    import uuid
    _, _, _, _, roster_id = _setup_environment(client, db)
    response = client.delete(f"/rosters/{roster_id}/players/{uuid.uuid4()}")
    assert response.status_code == 404
