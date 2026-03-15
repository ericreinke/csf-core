def _make_match(client, hltv_id=None):
    body = {"maximum_maps": 3}
    if hltv_id:
        body["hltv_id"] = hltv_id
    return client.post("/matches/", json=body).json()


def test_create_match(client):
    response = client.post("/matches/", json={"hltv_id": 2001, "maximum_maps": 3})
    assert response.status_code == 201
    data = response.json()
    assert data["hltv_id"] == 2001
    assert data["demo_status"] == "PENDING"


def test_create_match_duplicate_hltv(client):
    _make_match(client, hltv_id=3000)
    response = client.post("/matches/", json={"hltv_id": 3000})
    assert response.status_code == 409


def test_get_match(client):
    mid = _make_match(client)["id"]
    assert client.get(f"/matches/{mid}").status_code == 200


def test_get_match_not_found(client):
    import uuid
    assert client.get(f"/matches/{uuid.uuid4()}").status_code == 404


def test_list_matches(client):
    _make_match(client)
    _make_match(client)
    response = client.get("/matches/")
    assert response.status_code == 200
    assert len(response.json()) >= 2


def test_update_match(client):
    mid = _make_match(client)["id"]
    response = client.patch(f"/matches/{mid}", json={"demo_status": "SUCCESS"})
    assert response.status_code == 200
    assert response.json()["demo_status"] == "SUCCESS"


def test_delete_match(client):
    mid = _make_match(client)["id"]
    assert client.delete(f"/matches/{mid}").status_code == 204
    assert client.get(f"/matches/{mid}").status_code == 404
