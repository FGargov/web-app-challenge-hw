import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    json_data = response.get_json()

    assert "status" in json_data
    assert json_data["status"] in ["ok", "healthy"]


def test_visit(client):
    response = client.get("/visit")

    assert response.status_code == 200
    assert b"visits" in response.data
