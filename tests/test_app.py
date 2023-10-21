from fastapi import status

from task_manager.schemas import UserPublic


def test_root_deve_retornar_200_e_hello_world(client):
    response = client.get('/')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'message': 'Hello, world!'}


def test_create_new_user(client):
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


def test_create_user_with_existent_username(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'Teste',
            'password': 'fizzbyzz',
            'email': 'teste@test.com',
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': 'Username already registered'}


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'users': []}


def test_read_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()

    response = client.get('/users/')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user):
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


def test_update_user_error_from_id_less_than_1(client, user):
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


def test_update_user_error_from_id_greater_than_size_without_users(client):
    response = client.put(
        '/users/1',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'jasdasd',
        },
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_update_user_error_from_id_greater_than_size_with_users(client, user):
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


def test_delete_user(client, user):
    response = client.delete('/users/1')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'detail': 'User deleted'}


def test_delete_user_error_from_id_less_than_1(client):
    response = client.delete('/users/0')

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_delete_user_error_from_id_greater_than_size_without_users(client):
    response = client.delete('/users/1')

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_delete_user_error_from_id_greater_than_size_with_users(client, user):
    response = client.delete('/users/2')

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'User not found'}
