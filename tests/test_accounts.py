def test_create_account(client):
    response = client.post("/accounts/", json={
        "google_id": "google-123",
        "email": "eric@gmail.com",
        "display_name": "Eric",
    })
    assert response.status_code == 201
    data = response.json()
    assert data["google_id"] == "google-123"
    assert data["email"] == "eric@gmail.com"
    assert data["display_name"] == "Eric"
    assert data["is_active"] is True
    assert data["id"] is not None


def test_create_account_duplicate_google_id(client):
    client.post("/accounts/", json={
        "google_id": "google-123",
        "email": "eric@gmail.com",
        "display_name": "Eric",
    })
    response = client.post("/accounts/", json={
        "google_id": "google-123",
        "email": "other@gmail.com",
        "display_name": "Other",
    })
    assert response.status_code == 409


def test_get_account(client):
    create_response = client.post("/accounts/", json={
        "google_id": "google-123",
        "email": "eric@gmail.com",
        "display_name": "Eric",
    })
    account_id = create_response.json()["id"]

    response = client.get(f"/accounts/{account_id}")
    assert response.status_code == 200
    assert response.json()["display_name"] == "Eric"


def test_get_account_not_found(client):
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = client.get(f"/accounts/{fake_id}")
    assert response.status_code == 404


def test_list_accounts(client):
    client.post("/accounts/", json={"google_id": "g1", "email": "a@test.com", "display_name": "A"})
    client.post("/accounts/", json={"google_id": "g2", "email": "b@test.com", "display_name": "B"})

    response = client.get("/accounts/")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_update_account(client):
    create_response = client.post("/accounts/", json={
        "google_id": "google-123",
        "email": "eric@gmail.com",
        "display_name": "Eric",
    })
    account_id = create_response.json()["id"]

    response = client.patch(f"/accounts/{account_id}", json={
        "display_name": "Eric R",
    })
    assert response.status_code == 200
    assert response.json()["display_name"] == "Eric R"
    # email should be unchanged
    assert response.json()["email"] == "eric@gmail.com"


def test_deactivate_account(client):
    create_response = client.post("/accounts/", json={
        "google_id": "google-123",
        "email": "eric@gmail.com",
        "display_name": "Eric",
    })
    account_id = create_response.json()["id"]

    # Deactivate
    response = client.delete(f"/accounts/{account_id}")
    assert response.status_code == 204

    # Account still exists but is_active should be False
    response = client.get(f"/accounts/{account_id}")
    assert response.status_code == 200
    assert response.json()["is_active"] is False
