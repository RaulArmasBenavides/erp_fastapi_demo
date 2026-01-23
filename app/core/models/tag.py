from sqlmodel import Field

from pydantic import BaseModel
class Tag(BaseModel, table=True):
    user_token: str = Field()

    name: str = Field(unique=True)
    description: str = Field(default=None, nullable=True)
