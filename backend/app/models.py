from pydantic import BaseModel, Field
from typing import List, Optional

class UploadResponse(BaseModel):
    id: str

class MatchRequest(BaseModel):
    job_description: str
    top_k: int = Field(default=5, gt=0, le=50)

class MatchItem(BaseModel):
    id: str
    filename: str
    score: float
    skills:List[str]=[]