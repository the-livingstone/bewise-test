import logging

from sqlalchemy import MetaData, NullPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import config

logger = logging.getLogger(__name__)

PG_URL = (
    f"postgresql+asyncpg://{config.postgres.user}:{config.postgres.password}"
    f"@{config.postgres.host}:{config.postgres.port}/{config.postgres.name}"
)
PG_URL_MIGRATIONS = PG_URL.replace("asyncpg", "psycopg2")

Base = declarative_base()
engine_params = dict(
    pool_size=config.postgres.MIN_POOL_SIZE,
    max_overflow=config.postgres.MIN_POOL_SIZE + config.postgres.MAX_POOL_SIZE,
)

engine = create_async_engine(
    PG_URL,
    connect_args={"server_settings": {"jit": "off"}},
    **engine_params,
)

async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False, autoflush=False)
