from pydantic import BaseModel, Field
from typing import List
from datetime import datetime


class TeamCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="Team name")
    country: str = Field(..., min_length=1, max_length=100, description="Country")


class TeamResponse(BaseModel):
    id: int
    name: str
    country: str
    created_at: datetime
    updated_at: datetime


class TeamList(BaseModel):
    teams: List[TeamResponse]
    total: int 