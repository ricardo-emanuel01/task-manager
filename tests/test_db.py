from sqlalchemy import select

from task_manager.models import User


def test_create_user(session):
    test_name = 'mariana'
    new_user = User(
        username=test_name, password='segredo', email='mari@test.com'
    )

    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == test_name))

    assert user.username == test_name
