from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class RepositoriesBase(BaseModel):
    id: int
    description: Optional[str]
    name: str
    created_at: Optional[datetime]


class MergeRequestBase(BaseModel):
    id: int
    author_id: int
    repositories_id: int
    title: str
    description: Optional[str]
    state: Optional[str]
    target_branch: Optional[str]
    source_branch: Optional[str]
    created_at: datetime
    updated_at: datetime


class UsersBase(BaseModel):
    id: int
    username: str
    name: str
