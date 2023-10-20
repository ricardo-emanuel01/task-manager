from fastapi import status


def test_root_deve_retornar_200_e_hello_world(client):
    response = client.get('/')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'message': 'Hello, world!'}


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'mariana',
            'email': 'mariana@example.com',
            'password': 'salgadinhodeuva',
        },
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        'username': 'mariana',
        'email': 'mariana@example.com',
        'id': 1,
    }


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'users': [
            {
                'username': 'mariana',
                'email': 'mariana@example.com',
                'id': 1,
            }
        ]
    }


def test_update_user(client):
    response = client.put(
        '/users/1',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'jasdasd',
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'username': 'bob',
        'email': 'bob@example.com',
        'id': 1,
    }


def test_update_user_error_from_id_less_than_1(client):
    response = client.put(
        '/users/0',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'jasdasd',
        },
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_update_user_error_from_id_greater_than_size(client):
    response = client.put(
        '/users/2',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'jasdasd',
        },
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_delete_user(client):
    response = client.delete('/users/1')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'detail': 'User deleted'}


def test_delete_user_error_from_id_less_than_1(client):
    response = client.delete('/users/0')

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_delete_user_error_from_id_greater_than_size(client):
    response = client.delete('/users/2')

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'User not found'}
