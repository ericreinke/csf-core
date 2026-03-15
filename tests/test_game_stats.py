SAMPLE_STATS = {"kills": 20, "deaths": 15, "assists": 3, "rating": 1.12}


def _make_player(client, name="ZywOo"):
    return client.post("/players/", json={"user_name": name}).json()["id"]


def _make_map(client, name="de_dust2"):
    return client.post("/maps/", json={"map_name": name}).json()["id"]


def test_create_game_stats(client):
    player_id = _make_player(client)
    map_id = _make_map(client)
    response = client.post(
        "/game-stats/",
        json={"player_uuid": player_id, "map_uuid": map_id, "stats": SAMPLE_STATS},
    )
    assert response.status_code == 201
    assert response.json()["stats"]["kills"] == 20


def test_get_game_stats(client):
    player_id = _make_player(client, "NiKo")
    map_id = _make_map(client, "de_mirage")
    gs_id = client.post(
        "/game-stats/",
        json={"player_uuid": player_id, "map_uuid": map_id, "stats": SAMPLE_STATS},
    ).json()["id"]
    assert client.get(f"/game-stats/{gs_id}").status_code == 200


def test_get_game_stats_not_found(client):
    import uuid
    assert client.get(f"/game-stats/{uuid.uuid4()}").status_code == 404


def test_list_game_stats_filter_by_player(client):
    player1 = _make_player(client, "ropz")
    player2 = _make_player(client, "device")
    map1 = _make_map(client, "de_overpass")
    map2 = _make_map(client, "de_vertigo")

    client.post("/game-stats/", json={"player_uuid": player1, "map_uuid": map1, "stats": SAMPLE_STATS})
    client.post("/game-stats/", json={"player_uuid": player2, "map_uuid": map2, "stats": SAMPLE_STATS})

    response = client.get(f"/game-stats/?player_uuid={player1}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["player_uuid"] == player1


def test_update_game_stats(client):
    player_id = _make_player(client, "karrigan")
    map_id = _make_map(client, "de_ancient")
    gs_id = client.post(
        "/game-stats/",
        json={"player_uuid": player_id, "map_uuid": map_id, "stats": SAMPLE_STATS},
    ).json()["id"]
    response = client.patch(f"/game-stats/{gs_id}", json={"stats": {"kills": 25}})
    assert response.status_code == 200
    assert response.json()["stats"]["kills"] == 25


def test_delete_game_stats(client):
    player_id = _make_player(client, "broky")
    map_id = _make_map(client, "de_cbble")
    gs_id = client.post(
        "/game-stats/",
        json={"player_uuid": player_id, "map_uuid": map_id, "stats": SAMPLE_STATS},
    ).json()["id"]
    assert client.delete(f"/game-stats/{gs_id}").status_code == 204
    assert client.get(f"/game-stats/{gs_id}").status_code == 404
