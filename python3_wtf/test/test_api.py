"""Basic API tests."""
from fastapi.testclient import TestClient
from wtf_api.main import app

client = TestClient(app)


def test_root():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "name" in response.json()


def test_health():
    """Test health endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "plugins_available" in data


def test_ping():
    """Test ping endpoint."""
    response = client.get("/api/v1/ping")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_list_plugins():
    """Test list plugins endpoint."""
    response = client.get("/api/v1/plugins")
    assert response.status_code == 200
    plugins = response.json()
    assert isinstance(plugins, list)


def test_execute_plugins():
    """Test plugin execution endpoint."""
    response = client.post(
        "/api/v1/execute",
        json={
            "timeout": 5,
            "max_concurrent": 4,
            "plugin_args": [],
            "output_dir": "/tmp"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "status" in data


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
