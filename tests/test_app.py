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


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
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


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'detail': 'User deleted'}


def test_get_token(client, user):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': user.plain_password},
    )

    token = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert 'access_token' in token
    assert 'token_type' in token


def test_get_token_wrong_email_without_user(client):
    wrong_email = 'wrong@wrong.com'
    response = client.post(
        '/token',
        data={'username': wrong_email, 'password': 'asdjkasjd'},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_get_token_wrong_email_with_user(client, user):
    wrong_email = 'wrong@wrong.com'
    response = client.post(
        '/token',
        data={'username': wrong_email, 'password': user.plain_password},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_get_token_wrong_password(client, user):
    response = client.post(
        '/token', data={'username': user.email, 'password': 'wrongPass'}
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': 'Incorrect email or password'}
