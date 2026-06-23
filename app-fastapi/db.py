from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

SQLALCHEMY_DATABASE_URI = 'sqlite+aiosqlite:///tech_hub.db'

SQLALCHEMY_TRACK_MODIFICATIONS = False

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URI,
    echo = False
)

async_session = sessionmaker(
    engine,
    expire_on_commit = False,
    class_ = AsyncSession
)

async def get_db_session():
    async with async_session() as session:
        yield session