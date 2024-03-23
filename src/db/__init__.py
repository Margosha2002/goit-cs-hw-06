import asyncio

import beanie
from motor.core import AgnosticDatabase
from motor.motor_asyncio import AsyncIOMotorClient

from db.documents import (Message)

__all__: list[str] = [
    Message
]

client: AsyncIOMotorClient = AsyncIOMotorClient("mongodb://root:example@host.docker.internal:27017/mongo?authSource=admin", uuidRepresentation='standard')
# client: AsyncIOMotorClient = AsyncIOMotorClient("mongodb://root:example@localhost:27017/mongo?authSource=admin", uuidRepresentation='standard')

db: AgnosticDatabase = client.get_default_database()


async def init():
    client.get_io_loop = asyncio.get_running_loop

    await beanie.init_beanie(
        database=db,
        document_models=[
            Message
        ],
    )
