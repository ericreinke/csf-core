def test_create_team(client):
    response = client.post("/teams/", json={"name": "Vitality", "hltv_id": 1})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Vitality"
    assert data["hltv_id"] == 1


def test_create_team_duplicate_hltv(client):
    client.post("/teams/", json={"name": "Vitality", "hltv_id": 1})
    response = client.post("/teams/", json={"name": "Vitality2", "hltv_id": 1})
    assert response.status_code == 409


def test_get_team(client):
    team_id = client.post("/teams/", json={"name": "NAVI"}).json()["id"]
    response = client.get(f"/teams/{team_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "NAVI"


def test_get_team_not_found(client):
    import uuid
    response = client.get(f"/teams/{uuid.uuid4()}")
    assert response.status_code == 404


def test_list_teams(client):
    client.post("/teams/", json={"name": "FaZe"})
    client.post("/teams/", json={"name": "G2"})
    response = client.get("/teams/")
    assert response.status_code == 200
    assert len(response.json()) >= 2


def test_update_team(client):
    team_id = client.post("/teams/", json={"name": "Furia"}).json()["id"]
    response = client.patch(f"/teams/{team_id}", json={"name": "Furia Esports"})
    assert response.status_code == 200
    assert response.json()["name"] == "Furia Esports"


def test_delete_team(client):
    team_id = client.post("/teams/", json={"name": "mouz"}).json()["id"]
    assert client.delete(f"/teams/{team_id}").status_code == 204
    assert client.get(f"/teams/{team_id}").status_code == 404
