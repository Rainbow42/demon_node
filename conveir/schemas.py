from typing import Optional, List

from pydantic import BaseModel

from conveir.const import Pipelines


class Pipeline(BaseModel):
    name: Optional[str]
    version: Optional[str] = 'v1.0'
    extended_pipline: List[Pipelines]
