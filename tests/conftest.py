import pytest
from fastapi.testclient import TestClient
from task_manager.app import app


@pytest.fixture
def client():
    return TestClient(app)
