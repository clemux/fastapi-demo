def test_get_healthcheck(client):
    response = client.get(
        "/health",
    )
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
