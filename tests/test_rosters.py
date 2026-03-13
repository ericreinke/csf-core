import pytest
from app.models.account import Account


def _create_test_account(db, google_id="rost-google-id", email="rost@test.com", display_name="Rost Test"):
    account = Account(google_id=google_id, email=email, display_name=display_name)
    db.add(account)
    db.commit()
    db.refresh(account)
    return account


def _setup_roster_environment(client, db):
    """
    Creates the required hierarchy to test a Roster:
    Account -> League -> Registration -> Pool -> Roster
    """
    account = _create_test_account(db)
    
    # 1. League
    league_id = client.post("/leagues/", json={"name": "L1", "owner_id": str(account.id)}).json()["id"]
    
    # 2. Registration
    reg_id = client.post(f"/leagues/{league_id}/registrations", json={"account_id": str(account.id)}).json()["id"]
    
    # 3. Pool
    pool_id = client.post(f"/leagues/{league_id}/pools", json={"league_id": league_id, "name": "P1"}).json()["id"]
    
    # 4. Mock admin assignment (Assign registration to pool)
    # Since we didn't build an explicit admin assignment API yet, we can bypass the API and do it via DB for the test, 
    # OR we can just hit the pool creation and assign it in the DB.
    from app.services.league_registration_service import assign_pool
    assign_pool(db, reg_id, pool_id)

    return account.id, league_id, reg_id, pool_id


def test_create_roster(client, db):
    account_id, league_id, reg_id, pool_id = _setup_roster_environment(client, db)

    response = client.post(f"/pools/{pool_id}/rosters", json={
        "name": "My Roster",
        "tag": "MYR",
        "registration_id": str(reg_id),
        "owner_id": str(account_id)
    })
    
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "My Roster"
    assert data["tag"] == "MYR"
    assert data["pool_id"] == str(pool_id)
    assert data["registration_id"] == str(reg_id)


def test_create_roster_wrong_pool(client, db):
    account_id, league_id, reg_id, pool_id = _setup_roster_environment(client, db)
    
    # Create a second pool
    pool_2_id = client.post(f"/leagues/{league_id}/pools", json={"league_id": league_id, "name": "P2"}).json()["id"]

    # Try to create a roster in pool 2, even though registration is in pool 1
    response = client.post(f"/pools/{pool_2_id}/rosters", json={
        "name": "Sneaky Roster",
        "registration_id": str(reg_id),
        "owner_id": str(account_id)
    })
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Registration is not assigned to this pool"


def test_get_rosters(client, db):
    account_id, _, reg_id, pool_id = _setup_roster_environment(client, db)

    client.post(f"/pools/{pool_id}/rosters", json={"name": "Roster 1", "registration_id": str(reg_id), "owner_id": str(account_id)})

    response = client.get(f"/pools/{pool_id}/rosters")
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_update_roster(client, db):
    account_id, _, reg_id, pool_id = _setup_roster_environment(client, db)
    roster_id = client.post(f"/pools/{pool_id}/rosters", json={"name": "Roster 1", "registration_id": str(reg_id), "owner_id": str(account_id)}).json()["id"]

    response = client.patch(f"/pools/{pool_id}/rosters/{roster_id}", json={
        "name": "Roster 1 - Updated",
        "tag": "UPD"
    })
    
    assert response.status_code == 200
    assert response.json()["name"] == "Roster 1 - Updated"
    assert response.json()["tag"] == "UPD"


def test_delete_roster(client, db):
    account_id, _, reg_id, pool_id = _setup_roster_environment(client, db)
    roster_id = client.post(f"/pools/{pool_id}/rosters", json={"name": "To Delete", "registration_id": str(reg_id), "owner_id": str(account_id)}).json()["id"]

    response = client.delete(f"/pools/{pool_id}/rosters/{roster_id}")
    assert response.status_code == 204

    response = client.get(f"/pools/{pool_id}/rosters/{roster_id}")
    assert response.status_code == 404
