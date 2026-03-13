import pytest
from app.models.account import Account


def _create_test_account(db, google_id="r-google-id", email="r@test.com", display_name="R Test"):
    account = Account(google_id=google_id, email=email, display_name=display_name)
    db.add(account)
    db.commit()
    db.refresh(account)
    return account


def test_create_league_registration(client, db):
    account1 = _create_test_account(db, "a1", "a1@test.com", "A1")
    account2 = _create_test_account(db, "a2", "a2@test.com", "A2")
    
    # Create League
    create_league_resp = client.post("/leagues/", json={"name": "L1", "owner_id": str(account1.id)})
    league_id = create_league_resp.json()["id"]

    # Register
    response = client.post(f"/leagues/{league_id}/registrations", json={
        "account_id": str(account2.id)
    })
    
    assert response.status_code == 201
    data = response.json()
    assert data["account_id"] == str(account2.id)
    assert data["league_id"] == league_id
    assert data["status"] == "REGISTERED"
    assert data["pool_id"] is None


def test_duplicate_registration(client, db):
    account1 = _create_test_account(db, "a1-dup", "a1dup@test.com", "A1 Dup")
    create_league_resp = client.post("/leagues/", json={"name": "L2", "owner_id": str(account1.id)})
    league_id = create_league_resp.json()["id"]

    client.post(f"/leagues/{league_id}/registrations", json={"account_id": str(account1.id)})
    
    # Duplicate
    response = client.post(f"/leagues/{league_id}/registrations", json={"account_id": str(account1.id)})
    assert response.status_code == 409


def test_get_league_registrations(client, db):
    account_admin = _create_test_account(db, "admin", "admin@test.com", "Admin")
    account_user1 = _create_test_account(db, "u1", "u1@test.com", "U1")
    account_user2 = _create_test_account(db, "u2", "u2@test.com", "U2")

    league_id = client.post("/leagues/", json={"name": "L3", "owner_id": str(account_admin.id)}).json()["id"]

    client.post(f"/leagues/{league_id}/registrations", json={"account_id": str(account_user1.id)})
    client.post(f"/leagues/{league_id}/registrations", json={"account_id": str(account_user2.id)})

    response = client.get(f"/leagues/{league_id}/registrations")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_delete_league_registration(client, db):
    account = _create_test_account(db, "deleter", "del@test.com", "Deleter")
    league_id = client.post("/leagues/", json={"name": "L4", "owner_id": str(account.id)}).json()["id"]

    reg_resp = client.post(f"/leagues/{league_id}/registrations", json={"account_id": str(account.id)})
    reg_id = reg_resp.json()["id"]

    response = client.delete(f"/leagues/{league_id}/registrations/{reg_id}")
    assert response.status_code == 204

    # Verify lists as empty
    response = client.get(f"/leagues/{league_id}/registrations")
    assert len(response.json()) == 0
