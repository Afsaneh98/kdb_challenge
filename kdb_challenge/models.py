from pydantic import BaseModel, Field
from typing import List


class SuggestionRequest(BaseModel):
    query: str
    top_k: int = 5
    min_score: float = 0


class SuggestionItem(BaseModel):
    text: str
    score: float


class SuggestionResponse(BaseModel):
    query: str
    suggestions: List[SuggestionItem]
