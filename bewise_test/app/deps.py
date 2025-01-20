import logging

from typing import AsyncGenerator, Callable, Type, TypeVar

from app.db.base import async_session
from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repos import BaseSqlaRepo
from app.service import ApplicationService
from bewise_test.app.messages import KafkaPublisher


_logger = logging.getLogger(__name__)


async def get_sqla_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


TSqlaRepo = TypeVar("TSqlaRepo", bound=BaseSqlaRepo)


def get_sqla_repo(repo_type: Type[TSqlaRepo]) -> Callable[[AsyncSession], TSqlaRepo]:
    def func(
        conn: AsyncSession = Depends(get_sqla_session, use_cache=True)
    ) -> TSqlaRepo:
        return repo_type(conn)

    return func


def get_publisher(request: Request) -> KafkaPublisher:
    return request.app.state.producer


def get_service(
    session: AsyncSession = Depends(get_sqla_session),
    message_publisher: KafkaPublisher = Depends(get_publisher),
):
    return ApplicationService(session, message_publisher)
