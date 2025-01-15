

from pydantic import BaseModel


class ApplicationSchema(BaseModel):
    user_name: str
    description: str