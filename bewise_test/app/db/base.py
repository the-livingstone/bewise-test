import logging
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

import app.config as config

logger = logging.getLogger(__name__)

PG_URL = (
    f"postgresql+asyncpg://{config.POSTGRES_USER}:{config.POSTGRES_PASSWORD}"
    f"@{config.POSTGRES_HOST}:{config.POSTGRES_PORT}/{config.POSTGRES_NAME}"
)
PG_URL_MIGRATIONS = PG_URL.replace("asyncpg", "psycopg2")

Base = declarative_base()
engine_params = dict(
    pool_size=config.POSTGRES_MIN_POOL_SIZE,
    max_overflow=config.POSTGRES_MIN_POOL_SIZE + config.POSTGRES_MAX_POOL_SIZE,
)

engine = create_async_engine(
    PG_URL,
    connect_args={"server_settings": {"jit": "off"}},
    **engine_params,
)

async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False, autoflush=False)
