from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from bookverse.config import settings

_engine: AsyncEngine | None = None
_factory: async_sessionmaker | None = None


def _init() -> None:
    global _engine, _factory
    if _engine is None:
        _engine = create_async_engine(
            f"{settings.db_driver}://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}",
            pool_size=settings.db_pool_size,
            future=True,
            pool_pre_ping=True,
        )
        _factory = async_sessionmaker(_engine, expire_on_commit=False)


def get_engine() -> AsyncEngine:
    if _engine is None:
        _init()
    return _engine  # type: ignore[return-value]


def get_session_factory() -> async_sessionmaker:
    if _factory is None:
        _init()
    return _factory  # type: ignore[return-value]


async_session_factory = get_session_factory()


class Base(DeclarativeBase):
    pass
