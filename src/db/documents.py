from datetime import datetime as dt
from uuid import UUID, uuid4
from typing import Final

from beanie import Document
from pydantic import Field


class Message(Document):
    id: UUID = Field(default_factory=uuid4)
    date: dt = Field(default_factory=dt.now)
    username: str
    message: str

    class Settings:
        name: Final[str] = "messages"
