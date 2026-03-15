def _make_map(client, map_name="de_dust2", hltv_id=None):
    body = {"map_name": map_name}
    if hltv_id:
        body["hltv_id"] = hltv_id
    return client.post("/maps/", json=body).json()


def test_create_map(client):
    response = client.post("/maps/", json={"map_name": "de_mirage", "hltv_id": 5001})
    assert response.status_code == 201
    data = response.json()
    assert data["map_name"] == "de_mirage"
    assert data["demo_parsed_status"] == "PENDING"


def test_create_map_duplicate_hltv(client):
    _make_map(client, hltv_id=6000)
    response = client.post("/maps/", json={"map_name": "de_nuke", "hltv_id": 6000})
    assert response.status_code == 409


def test_get_map(client):
    map_id = _make_map(client)["id"]
    response = client.get(f"/maps/{map_id}")
    assert response.status_code == 200
    assert response.json()["map_name"] == "de_dust2"


def test_get_map_not_found(client):
    import uuid
    assert client.get(f"/maps/{uuid.uuid4()}").status_code == 404


def test_list_maps(client):
    _make_map(client, "de_ancient")
    _make_map(client, "de_vertigo")
    response = client.get("/maps/")
    assert response.status_code == 200
    assert len(response.json()) >= 2


def test_update_map(client):
    map_id = _make_map(client)["id"]
    response = client.patch(f"/maps/{map_id}", json={"demo_parsed_status": "SUCCESS"})
    assert response.status_code == 200
    assert response.json()["demo_parsed_status"] == "SUCCESS"


def test_delete_map(client):
    map_id = _make_map(client)["id"]
    assert client.delete(f"/maps/{map_id}").status_code == 204
    assert client.get(f"/maps/{map_id}").status_code == 404
