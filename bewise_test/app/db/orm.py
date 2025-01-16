from typing import Self
import uuid
from datetime import datetime

from sqlalchemy import TIMESTAMP, Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped
from app.db.base import Base
from app.models import Application


class ApplicationORM(Base):
    __tablename__ = "application"

    id: Mapped[uuid.UUID] = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_name: Mapped[str] = Column(String, nullable=False)
    description: Mapped[str] = Column(String)
    created_at: Mapped[datetime] = Column(TIMESTAMP, nullable=False)

    def from_orm(self) -> Application:
        return Application(
            id=self.id,
            user_name=self.user_name,
            description=self.description,
            created_at=self.created_at
        )
    
    @classmethod
    def to_orm(cls, data: Application) -> Self:
        return cls(
            id=data.id,
            user_name=data.user_name,
            description=data.description,
            created_at=data.created_at
        )