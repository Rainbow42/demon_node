from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class Repositories(BaseModel):
    id_repositories: int
    reposition_token: str
    username: str  # от персонально токена
    user_id: int


class RepositoriesBase(BaseModel):
    id: int
    description: Optional[str]
    name: str
    created_at: Optional[datetime]


class UsersBase(BaseModel):
    id: int
    username: str
    name: str


class RepositoriesCreate(BaseModel):
    repositories: RepositoriesBase
    user: UsersBase
