from app.models.account import Account


def _create_test_account(db):
    account = Account(
        google_id="pool-test-google-id",
        email="pooltest@test.com",
        display_name="Pool Tester",
    )
    db.add(account)
    db.commit()
    db.refresh(account)
    return account


def test_create_league_pool(client, db):
    account = _create_test_account(db)
    
    # Needs a parent league first
    create_league_resp = client.post("/leagues/", json={
        "name": "Major League",
        "owner_id": str(account.id),
    })
    league_id = create_league_resp.json()["id"]

    response = client.post(f"/leagues/{league_id}/pools", json={
        "league_id": league_id,
        "name": "Alpha Pool",
        "max_teams": 10
    })
    
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Alpha Pool"
    assert data["max_teams"] == 10
    assert data["league_id"] == league_id


def test_create_pool_mismatched_league_id(client, db):
    account = _create_test_account(db)
    
    create_league_resp = client.post("/leagues/", json={"name": "L1", "owner_id": str(account.id)})
    league_id = create_league_resp.json()["id"]
    
    fake_id = "00000000-0000-0000-0000-000000000000"

    response = client.post(f"/leagues/{league_id}/pools", json={
        "league_id": fake_id,  # Body ID doesn't match URL ID
        "name": "Beta Pool",
        "max_teams": 10
    })
    
    assert response.status_code == 400


def test_get_league_pools(client, db):
    account = _create_test_account(db)
    create_league_resp = client.post("/leagues/", json={"name": "L2", "owner_id": str(account.id)})
    league_id = create_league_resp.json()["id"]

    client.post(f"/leagues/{league_id}/pools", json={"league_id": league_id, "name": "Pool 1"})
    client.post(f"/leagues/{league_id}/pools", json={"league_id": league_id, "name": "Pool 2"})

    response = client.get(f"/leagues/{league_id}/pools")
    
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_update_league_pool(client, db):
    account = _create_test_account(db)
    create_league_resp = client.post("/leagues/", json={"name": "L3", "owner_id": str(account.id)})
    league_id = create_league_resp.json()["id"]

    pool_resp = client.post(f"/leagues/{league_id}/pools", json={"league_id": league_id, "name": "P1"})
    pool_id = pool_resp.json()["id"]

    response = client.patch(f"/leagues/{league_id}/pools/{pool_id}", json={
        "name": "P1 - Updated",
        "max_teams": 12
    })
    
    assert response.status_code == 200
    assert response.json()["name"] == "P1 - Updated"
    assert response.json()["max_teams"] == 12


def test_delete_league_pool(client, db):
    account = _create_test_account(db)
    create_league_resp = client.post("/leagues/", json={"name": "L4", "owner_id": str(account.id)})
    league_id = create_league_resp.json()["id"]

    pool_resp = client.post(f"/leagues/{league_id}/pools", json={"league_id": league_id, "name": "P1"})
    pool_id = pool_resp.json()["id"]

    response = client.delete(f"/leagues/{league_id}/pools/{pool_id}")
    assert response.status_code == 204

    response = client.get(f"/leagues/{league_id}/pools/{pool_id}")
    assert response.status_code == 404
