"""T-001, issue #4. Written from the issue spec alone, before any implementation existed."""


def test_health_returns_ok_json(api):
    response = api.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
