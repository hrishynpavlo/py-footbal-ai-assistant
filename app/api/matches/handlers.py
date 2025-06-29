from fastapi import HTTPException
from app.database import AsyncSessionLocal
from app.logger import get_logger
from app.models import Match
from .schemas import MatchCreate, MatchTeam, MatchResponse
from datetime import datetime
from sqlalchemy.orm import joinedload
from sqlalchemy import select

logger = get_logger(__name__)


async def create_match(match_data: MatchCreate) -> MatchResponse:
    async with AsyncSessionLocal() as session:
        try:
            new_match = Match(
                home_team_id=match_data.home_team_id,
                away_team_id=match_data.away_team_id,
                match_date=match_data.match_date,
                home_score=0,
                away_score=0,
                status="scheduled",
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            session.add(new_match)
            await session.commit()
            await session.refresh(new_match, ["home_team", "away_team"])
            
            return MatchResponse(
                id=new_match.id,
                home_team=MatchTeam(id=new_match.home_team_id, name=new_match.home_team.name),
                away_team=MatchTeam(id=new_match.away_team_id, name=new_match.away_team.name),
                match_date=new_match.match_date,
                home_score=new_match.home_score,
                away_score=new_match.away_score,
                status=new_match.status,
                created_at=new_match.created_at,
                updated_at=new_match.updated_at
            )
        except Exception as e:
            await session.rollback()
            logger.error("Failed to create match", error=str(e))
            raise HTTPException(
                status_code=500,
                detail="Internal server error while creating match"
            )


async def get_match_by_id(match_id: int) -> MatchResponse:
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(select(Match).where(Match.id == match_id).options(joinedload(Match.home_team), joinedload(Match.away_team)))
            match = result.scalar_one_or_none()

            if not match:
                raise HTTPException(
                    status_code=404,
                    detail=f"Match with id {match_id} not found"
                )

            return MatchResponse(
                id=match.id,
                home_team=MatchTeam(id=match.home_team_id, name=match.home_team.name),
                away_team=MatchTeam(id=match.away_team_id, name=match.away_team.name),
                match_date=match.match_date,
                home_score=match.home_score,
                away_score=match.away_score,
                status=match.status,
                created_at=match.created_at,
                updated_at=match.updated_at
            )
        except Exception as e:
            await session.rollback()
            logger.error("Failed to get match by id", error=str(e))
            raise HTTPException(
                status_code=500,
                detail="Internal server error while fetching match"
            )