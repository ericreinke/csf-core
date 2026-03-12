from app.models.user import User
from app.models.league import League, generate_uuid7
from app.models.team import Team


def _create_test_user(db):
    """Helper to create a user needed for league/team ownership."""
    user = User(
        google_id="test-google-id-123",
        email="eric@test.com",
        display_name="Eric",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def _create_test_league(db, owner_id):
    """Helper to create a league needed for team association."""
    league = League(
        name="Test League",
        owner_id=owner_id,
    )
    db.add(league)
    db.commit()
    db.refresh(league)
    return league


def test_create_team(client, db):
    user = _create_test_user(db)
    league = _create_test_league(db, user.id)

    response = client.post("/teams/", json={
        "name": "Team Alpha",
        "tag": "ALPH",
        "league_id": str(league.id),
        "owner_id": str(user.id),
    })
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Team Alpha"
    assert data["tag"] == "ALPH"
    assert data["league_id"] == str(league.id)
    assert data["owner_id"] == str(user.id)
    assert data["id"] is not None


def test_create_team_without_tag(client, db):
    user = _create_test_user(db)
    league = _create_test_league(db, user.id)

    response = client.post("/teams/", json={
        "name": "Team Beta",
        "league_id": str(league.id),
        "owner_id": str(user.id),
    })
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Team Beta"
    assert data["tag"] is None


def test_get_team(client, db):
    user = _create_test_user(db)
    league = _create_test_league(db, user.id)

    create_response = client.post("/teams/", json={
        "name": "Team Alpha",
        "league_id": str(league.id),
        "owner_id": str(user.id),
    })
    team_id = create_response.json()["id"]

    response = client.get(f"/teams/{team_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Team Alpha"


def test_get_team_not_found(client):
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = client.get(f"/teams/{fake_id}")
    assert response.status_code == 404


def test_list_teams(client, db):
    user = _create_test_user(db)
    league = _create_test_league(db, user.id)

    client.post("/teams/", json={"name": "Team A", "league_id": str(league.id), "owner_id": str(user.id)})
    client.post("/teams/", json={"name": "Team B", "league_id": str(league.id), "owner_id": str(user.id)})

    response = client.get("/teams/")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_update_team(client, db):
    user = _create_test_user(db)
    league = _create_test_league(db, user.id)

    create_response = client.post("/teams/", json={
        "name": "Team Alpha",
        "tag": "ALPH",
        "league_id": str(league.id),
        "owner_id": str(user.id),
    })
    team_id = create_response.json()["id"]

    response = client.patch(f"/teams/{team_id}", json={
        "name": "Team Alpha - Updated",
        "tag": "ALPU",
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Team Alpha - Updated"
    assert response.json()["tag"] == "ALPU"
    # league and owner should be unchanged
    assert response.json()["league_id"] == str(league.id)
    assert response.json()["owner_id"] == str(user.id)


def test_update_team_partial(client, db):
    """Updating only name should not change tag."""
    user = _create_test_user(db)
    league = _create_test_league(db, user.id)

    create_response = client.post("/teams/", json={
        "name": "Team Alpha",
        "tag": "ALPH",
        "league_id": str(league.id),
        "owner_id": str(user.id),
    })
    team_id = create_response.json()["id"]

    response = client.patch(f"/teams/{team_id}", json={"name": "New Name"})
    assert response.status_code == 200
    assert response.json()["name"] == "New Name"
    assert response.json()["tag"] == "ALPH"  # unchanged


def test_update_team_not_found(client):
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = client.patch(f"/teams/{fake_id}", json={"name": "Ghost"})
    assert response.status_code == 404


def test_delete_team(client, db):
    user = _create_test_user(db)
    league = _create_test_league(db, user.id)

    create_response = client.post("/teams/", json={
        "name": "Team Alpha",
        "league_id": str(league.id),
        "owner_id": str(user.id),
    })
    team_id = create_response.json()["id"]

    response = client.delete(f"/teams/{team_id}")
    assert response.status_code == 204

    response = client.get(f"/teams/{team_id}")
    assert response.status_code == 404


def test_delete_team_not_found(client):
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = client.delete(f"/teams/{fake_id}")
    assert response.status_code == 404
