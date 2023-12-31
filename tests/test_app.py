from fastapi import status


def test_root_deve_retornar_200_e_hello_world(client):
    response = client.get('/')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'message': 'Hello, world!'}
