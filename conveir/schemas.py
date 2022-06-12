from typing import List, Optional

from pydantic import BaseModel

from conveir.const import PipelinesEnum


class Pipeline(BaseModel):
    name: str
    version: Optional[str] = 'v1.0'
    extended_pipline: List[PipelinesEnum]
