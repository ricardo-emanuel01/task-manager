from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from task_manager.database import get_session, patch_entity
from task_manager.models import Todo, User
from task_manager.schemas import (
    Message,
    TodoList,
    TodoPublic,
    TodoSchema,
    TodoUpdate,
)
from task_manager.security import get_current_user

router = APIRouter(prefix='/todos', tags=['todos'])

CurrentUser = Annotated[User, Depends(get_current_user)]
Session = Annotated[Session, Depends(get_session)]


@router.get('/', response_model=TodoList)
def list_todos(
    session: Session,
    user: CurrentUser,
    title: Annotated[str | None, Query(max_length=50)] = None,
    description: Annotated[str | None, Query(max_length=50)] = None,
    state: Annotated[str | None, Query(max_length=50)] = None,
    offset: Annotated[int | None, Query(ge=1)] = None,
    limit: Annotated[int | None, Query(ge=1)] = None,
):
    query = select(Todo).where(Todo.user_id == user.id)

    # Refinando a query de acordo com os "query parameters" passados no endpoint
    if title:
        # .contains verifica se a string fornecida está presente no campo title
        query = query.filter(Todo.title.contains(title))

    if description:
        query = query.filter(Todo.description.contains(description))

    if state:
        query = query.filter(Todo.state == state)

    todos = session.scalars(query.offset(offset).limit(limit)).all()

    return {'todos': todos}


@router.post(
    '/', response_model=TodoPublic, status_code=status.HTTP_201_CREATED
)
def create_todo(
    todo: TodoSchema,
    user: CurrentUser,
    session: Session,
):
    # Gera um model de Todo com os argumentos
    db_todo: Todo = Todo(
        title=todo.title,
        description=todo.description,
        state=todo.state,
        user_id=user.id,
    )

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo


@router.patch('/{todo_id}', response_model=TodoPublic)
def patch_todo(
    todo_id: int, session: Session, user: CurrentUser, todo: TodoUpdate
):
    db_todo = session.scalar(
        select(Todo).where(Todo.user_id == user.id, Todo.id == todo_id)
    )

    if not db_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Task not found'
        )

    patch_entity(db_todo, todo, session)

    return db_todo


@router.delete('/{todo_id}', response_model=Message)
def delete_todo(todo_id: int, session: Session, user: CurrentUser):
    todo = session.scalar(
        select(Todo).where(Todo.user_id == user.id, Todo.id == todo_id)
    )

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Task not found'
        )

    session.delete(todo)
    session.commit()

    return {'detail': 'Task has been deleted successfully'}
