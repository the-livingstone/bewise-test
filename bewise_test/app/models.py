from datetime import datetime
from typing import Optional
import uuid
from pydantic import BaseModel, Field


class Application(BaseModel):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4)
    user_name: str
    description: str
    created_at: datetime = Field(default_factory=datetime.now)
