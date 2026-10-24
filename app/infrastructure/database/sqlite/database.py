from app.infrastructure.database.models.user import User

from advanced_alchemy.extensions.fastapi import AdvancedAlchemy, SQLAlchemyAsyncConfig

from sqlalchemy.orm import DeclarativeBase


config = SQLAlchemyAsyncConfig(
    connection_string="sqlite+aiosqlite:///./test.db",
    create_all=True
)


alchemy = AdvancedAlchemy(config=config)


class Base(DeclarativeBase):
    pass


async def init_db() -> None:
    engine = config.get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_session():
    async with config.get_session() as session:
        yield session


async def close_db() -> None:
    await config.get_engine().dispose()
