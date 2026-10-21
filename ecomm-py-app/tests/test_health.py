from fastapi.testclient import TestClient


def test_health_returns_up(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "UP", "components": {"db": "UP"}}


def test_health_is_documented_in_openapi(client: TestClient) -> None:
    spec = client.get("/openapi.json").json()

    assert "/health" in spec["paths"]
