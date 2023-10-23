from typing import Union

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from task_manager.models import Todo, User
from task_manager.schemas import TodoUpdate, UserUpdate
from task_manager.settings import Settings

engine = create_engine(Settings().DATABASE_URL)

Entity = Union[Todo, User]
NewEntity = Union[TodoUpdate, UserUpdate]

def get_session():
    with Session(engine) as session:
        yield session


# Para todos os campos nao nulos atribui no modelo do banco de dados
def patch_entity(entity: Entity, new_entity: NewEntity, session: Session):
    for key, value in new_entity.model_dump(exclude_unset=True).items():
        setattr(entity, key, value)

    session.add(entity)
    session.commit()
    session.refresh(entity)
