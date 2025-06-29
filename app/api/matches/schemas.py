from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class MatchCreate(BaseModel):
    home_team_id: int
    away_team_id: int
    match_date: datetime

class MatchTeam(BaseModel):
    id: int
    name: str

class MatchResponse(BaseModel):
    id: int
    home_team: MatchTeam
    away_team: MatchTeam
    match_date: datetime
    home_score: int
    away_score: int
    status: str
    created_at: datetime
    updated_at: datetime

class MatchList(BaseModel):
    matches: List[MatchResponse]
    total: int

class MatchUpdate(BaseModel):
    home_score: Optional[int] = None
    away_score: Optional[int] = None
    status: Optional[str] = None