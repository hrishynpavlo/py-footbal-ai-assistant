from fastapi import APIRouter
from .handlers import get_teams, create_team, get_team_by_id, delete_team
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


@router.post("/", response_model=TeamResponse, status_code=201)
async def create_team_route(team_data: TeamCreate):
    return await create_team(team_data)


@router.get("/{team_id}", response_model=TeamResponse)
async def get_team_by_id_route(team_id: int):
    return await get_team_by_id(team_id)

@router.delete("/{team_id}", status_code=204)
async def delete_team_route(team_id: int):
    return await delete_team(team_id)