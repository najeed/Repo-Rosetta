from pydantic import BaseModel
from typing import List, Optional, Dict

class CodeEntity(BaseModel):
    name: str
    type: str  # function, class, file, module
    path: str
    line_start: int
    line_end: int
    summary: Optional[str] = None
    dependencies: List[str] = []
    metadata: Dict[str, str] = {}

class RepositoryContext(BaseModel):
    name: str
    url: str
    entities: List[CodeEntity] = []
