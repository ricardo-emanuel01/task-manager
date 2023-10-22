from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from task_manager.database import get_session
from task_manager.models import User
from task_manager.schemas import (
    Message,
    UserList,
    UserPublic,
    UserSchema,
    UserUpdate,
)
from task_manager.security import get_current_user, get_password_hash

router = APIRouter(prefix='/users', tags=['users'])


Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post(
    '/', response_model=UserPublic, status_code=status.HTTP_201_CREATED
)
def create_user(user: UserSchema, session: Session):
    db_user = session.scalar(
        select(User).where(
            or_(User.email == user.email, User.username == user.username)
        )
    )

    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Email or username already registered',
        )

    hashed_password = get_password_hash(user.password)

    db_user = User(
        username=user.username, password=hashed_password, email=user.email
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.get('/', response_model=UserList)
def read_users(session: Session, skip: int = 0, limit: int = 100):
    users = session.scalars(select(User).offset(skip).limit(limit)).all()
    return {'users': users}


@router.patch('/{user_id}', response_model=UserPublic)
def update_user(
    user_id: int,
    user: UserUpdate,
    session: Session,
    current_user: CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Not enough permissions',
        )

    for key, value in user.model_dump(exclude_unset=True).items():
        setattr(current_user, key, value)

    session.commit()
    session.refresh(current_user)

    return current_user


@router.delete('/{user_id}', response_model=Message)
def delete_user(
    user_id: int,
    session: Session,
    current_user: CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Not enough permissions',
        )

    session.delete(current_user)
    session.commit()

    return {'detail': 'User deleted'}
