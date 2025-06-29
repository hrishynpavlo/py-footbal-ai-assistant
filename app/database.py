from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool
from app.logger import get_logger
from typing import AsyncGenerator

logger = get_logger(__name__)

DATABASE_URL = "postgresql+asyncpg://football_user:football_password@localhost:5432/football_ai"

engine = create_async_engine(
    DATABASE_URL,
    echo=True,  
    poolclass=NullPool, 
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            logger.error("Database session error", error=str(e))
            await session.rollback()
            raise
        finally:
            await session.close()

async def init_database():
    try:
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        logger.info("Database connection established successfully")
    except Exception as e:
        logger.error("Failed to connect to database", error=str(e))
        raise

async def close_database():
    await engine.dispose()
    logger.info("Database connections closed") 