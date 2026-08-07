from fastapi.testclient import TestClient


def test_healthcheck_success(client: TestClient):
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "UP"}
