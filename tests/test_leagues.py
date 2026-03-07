def test_create_league(client):
    response = client.post("/leagues/", json={
        "name": "Season 1",
        "owner": "eric",
    })
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Season 1"
    assert data["owner"] == "eric"
    assert data["status"] == "open"
    assert data["max_teams"] == 8
    assert data["id"] is not None


def test_get_league(client):
    # Create first
    create_response = client.post("/leagues/", json={
        "name": "Season 1",
        "owner": "eric",
    })
    league_id = create_response.json()["id"]

    # Then fetch
    response = client.get(f"/leagues/{league_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Season 1"


def test_get_league_not_found(client):
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = client.get(f"/leagues/{fake_id}")
    assert response.status_code == 404


def test_list_leagues(client):
    client.post("/leagues/", json={"name": "League A", "owner": "eric"})
    client.post("/leagues/", json={"name": "League B", "owner": "eric"})

    response = client.get("/leagues/")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_update_league(client):
    create_response = client.post("/leagues/", json={
        "name": "Season 1",
        "owner": "eric",
    })
    league_id = create_response.json()["id"]

    response = client.patch(f"/leagues/{league_id}", json={
        "name": "Season 1 - Updated",
        "max_teams": 10,
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Season 1 - Updated"
    assert response.json()["max_teams"] == 10
    # owner should be unchanged
    assert response.json()["owner"] == "eric"


def test_delete_league(client):
    create_response = client.post("/leagues/", json={
        "name": "Season 1",
        "owner": "eric",
    })
    league_id = create_response.json()["id"]

    # Delete
    response = client.delete(f"/leagues/{league_id}")
    assert response.status_code == 204

    # Verify it's gone
    response = client.get(f"/leagues/{league_id}")
    assert response.status_code == 404
