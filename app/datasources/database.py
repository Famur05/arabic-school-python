from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from typing import Annotated
from fastapi import Depends
from app.config.settings import settings

async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=True,
    # pool_size=5,
    # max_overflow=10,
)

async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)


async def get_async_session():
    async with async_session_maker() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


class Base(DeclarativeBase):
    pass
