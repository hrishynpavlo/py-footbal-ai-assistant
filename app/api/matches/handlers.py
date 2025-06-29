from fastapi import HTTPException
from app.database import AsyncSessionLocal
from app.logger import get_logger
from app.models import Match
from .schemas import MatchCreate, MatchTeam, MatchResponse
from datetime import datetime
from sqlalchemy.orm import joinedload
from sqlalchemy import select
from operator import attrgetter

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
                id= attrgetter('id')(new_match),
                home_team=MatchTeam(id=attrgetter('home_team_id')(new_match), name=attrgetter('name')(new_match.home_team)),
                away_team=MatchTeam(id=attrgetter('away_team_id')(new_match), name=attrgetter('name')(new_match.away_team)),
                match_date=attrgetter('match_date')(new_match),
                home_score=attrgetter('home_score')(new_match),
                away_score=attrgetter('away_score')(new_match),
                status=attrgetter('status')(new_match),
                created_at=attrgetter('created_at')(new_match),
                updated_at=attrgetter('updated_at')(new_match)
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
                id=attrgetter('id')(match),
                home_team=MatchTeam(id=attrgetter('home_team_id')(match), name=attrgetter('name')(match.home_team)),
                away_team=MatchTeam(id=attrgetter('away_team_id')(match), name=attrgetter('name')(match.away_team)),
                match_date=attrgetter('match_date')(match),
                home_score=attrgetter('home_score')(match),
                away_score=attrgetter('away_score')(match),
                status=attrgetter('status')(match),
                created_at=attrgetter('created_at')(match),
                updated_at=attrgetter('updated_at')(match)
            )
        except Exception as e:
            await session.rollback()
            logger.error("Failed to get match by id", error=str(e))
            raise HTTPException(
                status_code=500,
                detail="Internal server error while fetching match"
            )