from typing import List, Literal, Optional
from pydantic import BaseModel

class Rag(BaseModel):
    reasoning_steps: List[str]
    answer: str