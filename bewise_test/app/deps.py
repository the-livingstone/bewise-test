import logging

from typing import AsyncGenerator, Callable, Type, TypeVar

from app.db.base import async_session
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repos import BaseSqlaRepo
from app.service import ApplicationService


_logger = logging.getLogger(__name__)


async def get_sqla_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


TSqlaRepo = TypeVar("TSqlaRepo", bound=BaseSqlaRepo)


def get_sqla_repo(repo_type: Type[TSqlaRepo]) -> Callable[[AsyncSession], TSqlaRepo]:
    def func(conn: AsyncSession = Depends(get_sqla_session, use_cache=True)) -> TSqlaRepo:
        return repo_type(conn)

    return func

def get_service(session: AsyncSession = Depends(get_sqla_session)):
    return ApplicationService(session)