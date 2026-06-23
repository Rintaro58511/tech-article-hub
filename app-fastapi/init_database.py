from sqlalchemy.ext.asyncio import create_async_engine
from models.memo import Base
import asyncio

SQLALCHEMY_DATABASE_URI = 'sqlite+aiosqlite:///tech_hub.db'

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URI,
    echo = False
    )

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__" :
    asyncio.run(init_db())