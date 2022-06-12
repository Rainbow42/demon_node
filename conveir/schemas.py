from typing import Optional, List

from pydantic import BaseModel

from conveir.const import PipelinesEnum


class Pipeline(BaseModel):
    name: Optional[str]
    version: Optional[str] = 'v1.0'
    extended_pipline: List[PipelinesEnum]
