from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "SURAYA AI"


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_tools():
    response = client.get("/tools")

    assert response.status_code == 200

    names = [
        item["name"]
        for item in response.json()
    ]

    assert "echo" in names


def test_command():
    response = client.post(
        "/command",
        json={
            "command": "hello",
        },
    )

    assert response.status_code == 200
    assert response.json()["success"] is True


def test_status():
    response = client.get("/status")

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "SURAYA AI"
    assert "runtime_running" in data
