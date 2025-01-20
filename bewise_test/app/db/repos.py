import logging

from typing import Generic, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

from app.db.orm import ApplicationORM
from app.models import Application


_logger = logging.getLogger(__name__)

TModel = TypeVar("TModel", bound=DeclarativeBase)


class BaseSqlaRepo(Generic[TModel]):
    __model__: Type[TModel]

    session: AsyncSession

    def __init__(self, session: AsyncSession):
        self.session = session
        super().__init__()


class ApplicationRepo(BaseSqlaRepo[ApplicationORM]):

    def query(self, username, page, page_size):
        query = select(ApplicationORM)
        if username:
            query = query.where(ApplicationORM.user_name == username)
        if page and page_size:
            offset = (page - 1) * page_size
            query = query.limit(page_size).offset(offset)
        return query

    async def create(self, data: Application):
        self.session.add(ApplicationORM.to_orm(data))

    async def get(self, id: str):
        result: ApplicationORM = await self.session.scalar(
            select(ApplicationORM).where(ApplicationORM.id == id)
        )
        return result.from_orm() if result is not None else None

    async def get_many(self, username: str, page: int, page_size: int):
        results: list[ApplicationORM] = await self.session.scalars(
            self.query(username, page, page_size)
        )
        return [result.from_orm() for result in results]
