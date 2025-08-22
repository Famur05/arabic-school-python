import asyncio
from app.datasources.database import async_engine, Base
import app.models.user


async def create_tables():
    async with async_engine.begin() as conn:
        # async_engine.echo = False
        await conn.run_sync(Base.metadata.drop_all)
        # await conn.run_sync(Base.metadata.create_all)
        # async_engine.echo = True


if __name__ == "__main__":
    asyncio.run(create_tables())
