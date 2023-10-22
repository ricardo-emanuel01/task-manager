from fastapi import status


def test_create_todo(client, token):
    response = client.post(
        '/todos',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'Test todo',
            'description': 'Test todo desc',
            'state': 'draft',
        },
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        'id': 1,
        'title': 'Test todo',
        'description': 'Test todo desc',
        'state': 'draft',
    }


def test_list_todos(client, user, token, todos_generic):
    response = client.get(
        '/todos',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == 5


def test_list_todos_pagination(client, token, todos_generic):
    response = client.get(
        '/todos/?offset=1&limit=2',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == 2


def test_list_todos_filter_title(client, token, todos_title):
    response = client.get(
        '/todos/?title=Test todo 1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == 5


def test_list_todos_filter_desc(client, token, todos_desc):
    response = client.get(
        '/todos/?description=description',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == 5


def test_list_todos_filter_state(client, token, todos_state):
    response = client.get(
        '/todos/?state=draft',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == 5


def test_list_todos_filter_combined(client, token, todos_combined):
    response = client.get(
        '/todos/?title=Other&description=desc&state=draft',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == 3


def test_patch_todo_error(client, token):
    response = client.patch(
        '/todos/10',
        json={},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Task not found'}


def test_patch_todo(client, token, todos_generic):
    response = client.patch(
        '/todos/1',
        json={'title': 'teste!!!'},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['title'] == 'teste!!!'


def test_delete_todo(client, token, todos_generic):
    response = client.delete(
        '/todos/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'detail': 'Task has been deleted successfully'}


def test_delete_error(client, token, todos_generic):
    response = client.delete(
        '/todos/6',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Task not found'}
