from typing import List, Optional

from pydantic import BaseModel

from conveir.const import PipelinesEnum


class Repositories(BaseModel):
    id_repositories: int
    reposition_token: str
    username: str  # от персонально токена
    user_id: int
