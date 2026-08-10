from pydantic import BaseModel
from pydantic import Field

class SearchRequest(BaseModel):
    query: str
    top_k: int = Field(default=5, ge=1, le=20)