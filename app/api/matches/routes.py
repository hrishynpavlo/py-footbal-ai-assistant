from fastapi import APIRouter
from .handlers import create_match, get_match_by_id, get_future_team_matches
from .schemas import MatchCreate, MatchResponse, MatchList

router = APIRouter(prefix="/matches", tags=["matches"])

@router.post("/", response_model=MatchResponse)
async def create_match_route(match_data: MatchCreate):
    return await create_match(match_data)

@router.get("/{match_id}", response_model=MatchResponse)
async def get_match_by_id_route(match_id: int):
    return await get_match_by_id(match_id)

@router.get("/team/{team_id}/future", response_model=MatchList)
async def get_future_team_matches_route(team_id: int):
    return await get_future_team_matches(team_id)