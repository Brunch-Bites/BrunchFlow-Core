from fastapi.testclient import TestClient
import sys
import os

# 将 src 目录加入路径以便导入
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from api.server import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "BrunchFlow Core Orchestrator is operational"}

def test_orchestration_endpoint():
    payload = {"location": "New York"}
    response = client.post("/orchestrate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "demand" in data["results"]
    assert "logistics" in data["results"]
