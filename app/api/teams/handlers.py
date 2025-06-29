from fastapi import HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.database import AsyncSessionLocal
from app.logger import get_logger
from app.models import Team
from .schemas import TeamCreate, TeamResponse, TeamList
from operator import attrgetter

logger = get_logger(__name__)


async def get_teams(
    skip: int = Query(0, ge=0, description="Number of teams to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of teams to return"),
    sort_by: str = Query("name", description="Sort field: name, country, created_at"),
    sort_order: str = Query("asc", description="Sort order: asc, desc")
) -> TeamList:
    async with AsyncSessionLocal() as session:
        try:
            sort_field = getattr(Team, sort_by, Team.name)
            
            if sort_order.lower() == "desc":
                sort_field = sort_field.desc()
            
            total_count = await session.scalar(select(func.count(Team.id)))
            
            result = await session.execute(
                select(Team)
                .order_by(sort_field)
                .offset(skip)
                .limit(limit)
            )
            
            teams = result.scalars().all()
            
            team_responses = [
                TeamResponse(
                    id=attrgetter('id')(team),
                    name=attrgetter('name')(team),
                    country=attrgetter('country')(team),
                    created_at=attrgetter('created_at')(team),
                    updated_at=attrgetter('updated_at')(team)
                )
                for team in teams
            ]
            
            return TeamList(teams=team_responses, total=total_count or 0)
            
        except Exception as e:
            logger.error("Failed to get teams", error=str(e))
            raise HTTPException(
                status_code=500,
                detail="Internal server error while fetching teams"
            )


async def create_team(team_data: TeamCreate) -> TeamResponse:
    async with AsyncSessionLocal() as session:
        try:
            existing_team = await session.execute(
                select(Team).where(Team.name == team_data.name)
            )
            if existing_team.scalar_one_or_none():
                raise HTTPException(
                    status_code=400, 
                    detail=f"Team with name '{team_data.name}' already exists"
                )
            
            new_team = Team(name=team_data.name, country=team_data.country)
            session.add(new_team)
            await session.commit()
            await session.refresh(new_team)
            
            return TeamResponse(
                id=attrgetter('id')(new_team),
                name=attrgetter('name')(new_team),
                country=attrgetter('country')(new_team),
                created_at=attrgetter('created_at')(new_team),
                updated_at=attrgetter('updated_at')(new_team)
            )
            
        except HTTPException:
            raise
        except Exception as e:
            await session.rollback()
            logger.error("Failed to create team", error=str(e))
            raise HTTPException(
                status_code=500, 
                detail="Internal server error while creating team"
            )


async def get_team_by_id(team_id: int) -> TeamResponse:
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(select(Team).where(Team.id == team_id))
            team = result.scalar_one_or_none()
            
            if not team:
                raise HTTPException(
                    status_code=404,
                    detail=f"Team with id {team_id} not found"
                )
            
            return TeamResponse(
                id=attrgetter('id')(team),
                name=attrgetter('name')(team),
                country=attrgetter('country')(team),
                created_at=attrgetter('created_at')(team),
                updated_at=attrgetter('updated_at')(team)
            )
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error("Failed to get team by id", error=str(e))
            raise HTTPException(
                status_code=500,    
                detail="Internal server error while fetching team"
            )