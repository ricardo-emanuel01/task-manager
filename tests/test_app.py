from fastapi.testclient import TestClient
from task_manager.app import app


def test_root_deve_retornar_200_e_hello_world():
    client = TestClient(app)

    response = client.get('/')

    assert response.status_code == 200
    assert response.json() == {'message': 'Hello, world!'}
