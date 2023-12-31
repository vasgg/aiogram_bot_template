import asyncio

from core.database.db import db
from core.database.models.base import Base


async def create_or_drop_db():
    async with db.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all, checkfirst=True)
        # await conn.run_sync(Base.metadata.drop_all)


if __name__ == '__main__':
    asyncio.run(create_or_drop_db())
