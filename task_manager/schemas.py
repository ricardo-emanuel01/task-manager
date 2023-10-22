from pydantic import BaseModel, ConfigDict, EmailStr

from task_manager.models import TodoState


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


# Utilizado para retornar o usuario com id e sem expor a senha
class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr

    # Permite que o modelo do banco de dados possa ser processado como um objeto python
    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None


class UserList(BaseModel):
    users: list[UserPublic]


class Message(BaseModel):
    detail: str


class TodoSchema(BaseModel):
    title: str
    description: str
    state: TodoState


# Utilizado para retornar a tarefa com o id
class TodoPublic(BaseModel):
    id: int
    title: str
    description: str
    state: TodoState
    model_config = ConfigDict(from_attributes=True)


class TodoUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    state: TodoState | None = None


class TodoList(BaseModel):
    todos: list[TodoPublic]


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
