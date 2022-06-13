from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, validator


class RepositoriesBase(BaseModel):
    id: int
    description: Optional[str]
    name: str
    created_at: Optional[datetime]


class UsersBase(BaseModel):
    id: int
    username: str
    name: str


class MergeRequestBase(BaseModel):
    id: int
    title: str
    description: Optional[str]
    state: Optional[str]
    target_branch: Optional[str]
    source_branch: Optional[str]
    created_at: datetime
    updated_at: datetime
    author: UsersBase

    @validator('created_at')
    def created_at_replace(cls, value):
        return value.replace(tzinfo=None)

    @validator('updated_at')
    def updated_at_replace(cls, value):
        return value.replace(tzinfo=None)



