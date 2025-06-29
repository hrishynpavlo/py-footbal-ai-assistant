from fastapi import APIRouter
from .handlers import get_teams, create_team
from .schemas import TeamCreate, TeamResponse, TeamList

router = APIRouter(prefix="/teams", tags=["teams"])


@router.get("/", response_model=TeamList)
async def get_teams_route(
    skip: int = 0,
    limit: int = 100,
    sort_by: str = "name",
    sort_order: str = "asc"
):
    return await get_teams(skip=skip, limit=limit, sort_by=sort_by, sort_order=sort_order)


@router.post("/", response_model=TeamResponse)
async def create_team_route(team_data: TeamCreate):
    return await create_team(team_data) 