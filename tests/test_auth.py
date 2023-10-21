from fastapi import status


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
