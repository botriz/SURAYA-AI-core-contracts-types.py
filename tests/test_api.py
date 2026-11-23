from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def test_public_health_endpoints_do_not_require_auth():
    assert client.get("/").status_code == 200
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_control_plane_fails_closed_without_token(monkeypatch):
    monkeypatch.delenv("SURAYA_API_TOKEN", raising=False)
    response = client.get("/status")
    assert response.status_code == 503
    assert response.json()["detail"] == "API access is not configured."


def test_control_plane_rejects_invalid_token(monkeypatch):
    monkeypatch.setenv("SURAYA_API_TOKEN", "expected-test-token")
    response = client.get("/status", headers={"Authorization": "Bearer wrong-token"})
    assert response.status_code == 401
    assert response.headers["www-authenticate"] == "Bearer"


def test_control_plane_accepts_valid_token(monkeypatch):
    monkeypatch.setenv("SURAYA_API_TOKEN", "expected-test-token")
    headers = {"Authorization": "Bearer expected-test-token"}

    response = client.get("/status", headers=headers)
    assert response.status_code == 200
    assert response.json()["name"] == "SURAYA AI"

    tools = client.get("/tools", headers=headers)
    assert tools.status_code == 200
    assert "echo" in [item["name"] for item in tools.json()]


def test_command_requires_token_and_runs_when_authenticated(monkeypatch):
    monkeypatch.setenv("SURAYA_API_TOKEN", "expected-test-token")
    response = client.post(
        "/command",
        headers={"Authorization": "Bearer expected-test-token"},
        json={"command": "hello"},
    )
    assert response.status_code == 200
    assert response.json()["success"] is True
