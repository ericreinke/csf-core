def test_create_tournament(client):
    response = client.post("/tournaments/", json={"title": "IEM Katowice 2025", "hltv_id": 8001})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "IEM Katowice 2025"
    assert data["hltv_id"] == 8001


def test_create_tournament_duplicate_hltv(client):
    client.post("/tournaments/", json={"title": "IEM Katowice", "hltv_id": 9999})
    response = client.post("/tournaments/", json={"title": "IEM Katowice 2", "hltv_id": 9999})
    assert response.status_code == 409


def test_get_tournament(client):
    tid = client.post("/tournaments/", json={"title": "Blast Major"}).json()["id"]
    response = client.get(f"/tournaments/{tid}")
    assert response.status_code == 200
    assert response.json()["title"] == "Blast Major"


def test_get_tournament_not_found(client):
    import uuid
    assert client.get(f"/tournaments/{uuid.uuid4()}").status_code == 404


def test_list_tournaments(client):
    client.post("/tournaments/", json={"title": "T1"})
    client.post("/tournaments/", json={"title": "T2"})
    response = client.get("/tournaments/")
    assert response.status_code == 200
    assert len(response.json()) >= 2


def test_update_tournament(client):
    tid = client.post("/tournaments/", json={"title": "PGL Major"}).json()["id"]
    response = client.patch(f"/tournaments/{tid}", json={"title": "PGL Major 2025"})
    assert response.status_code == 200
    assert response.json()["title"] == "PGL Major 2025"


def test_delete_tournament(client):
    tid = client.post("/tournaments/", json={"title": "ESL Pro League"}).json()["id"]
    assert client.delete(f"/tournaments/{tid}").status_code == 204
    assert client.get(f"/tournaments/{tid}").status_code == 404
