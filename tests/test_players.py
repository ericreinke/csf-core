def test_create_player(client):
    response = client.post("/players/", json={
        "hltv_id": 11893,
        "steam_id": 76561198031182239,
        "user_name": "ZywOo",
        "first_name": "Mathieu",
        "last_name": "Herbaut",
        "country": "France"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["user_name"] == "ZywOo"
    assert data["hltv_id"] == 11893


def test_create_player_duplicate_hltv(client):
    client.post("/players/", json={
        "hltv_id": 7998,
        "user_name": "s1mple"
    })
    
    response = client.post("/players/", json={
        "hltv_id": 7998,
        "user_name": "s1mple_fake"
    })
    assert response.status_code == 409


def test_get_player(client):
    create_response = client.post("/players/", json={
        "user_name": "NiKo",
    })
    player_id = create_response.json()["id"]

    response = client.get(f"/players/{player_id}")
    assert response.status_code == 200
    assert response.json()["user_name"] == "NiKo"


def test_list_players(client):
    client.post("/players/", json={"user_name": "device"})
    client.post("/players/", json={"user_name": "ropz"})

    response = client.get("/players/")
    assert response.status_code == 200
    # There are previously created players in this DB session from other test funcs above
    assert len(response.json()) >= 2


def test_update_player(client):
    create_response = client.post("/players/", json={
        "user_name": "m0NESY",
        "country": "Russia"
    })
    player_id = create_response.json()["id"]

    response = client.patch(f"/players/{player_id}", json={
        "user_name": "m0NESY_AWP",
    })
    assert response.status_code == 200
    assert response.json()["user_name"] == "m0NESY_AWP"
    assert response.json()["country"] == "Russia"


def test_delete_player(client):
    create_response = client.post("/players/", json={
        "user_name": "karrigan",
    })
    player_id = create_response.json()["id"]

    response = client.delete(f"/players/{player_id}")
    assert response.status_code == 204

    response = client.get(f"/players/{player_id}")
    assert response.status_code == 404
