import uuid
from datetime import datetime

from sqlalchemy import TIMESTAMP, Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped
from app.db.base import Base


class ApplicationORM(Base):
    __tablename__ = "person"

    id: Mapped[uuid.UUID] = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_name: Mapped[str] = Column(String, nullable=False)
    description: Mapped[str] = Column(String)
    created_at: Mapped[datetime] = Column(TIMESTAMP, nullable=False)