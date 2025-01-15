import logging

from typing import Generic, Type, TypeVar

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
    
    async def create(data: Application):
        pass

    async def get(id: str):
        pass

    async def get_many(username: str, page: int, page_size: int):
        pass