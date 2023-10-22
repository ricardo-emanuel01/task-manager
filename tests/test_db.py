from sqlalchemy import select

from task_manager.models import Todo, User


def test_create_user(session):
    test_name = 'mariana'
    new_user = User(
        username=test_name, password='segredo', email='mari@test.com'
    )

    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == test_name))

    assert user.username == test_name


def test_create_todo(session, user):
    todo = Todo(
        title='Test Todo',
        description='Test Desc',
        state='draft',
        user_id=user.id,
    )

    session.add(todo)
    session.commit()
    session.refresh(todo)

    user = session.scalar(select(User).where(User.id == user.id))

    assert todo in user.todos
