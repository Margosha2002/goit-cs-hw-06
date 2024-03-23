import asyncio
from functools import wraps
from typing import Coroutine, Callable

import websockets

import db
from db import Message


async def handler(websocket, path):
    data = await websocket.recv()
    reply = f"Data recieved as:  {data}!"

    message = Message.model_validate_json(data)
    await message.save()
    await websocket.send(reply)


def run_async(func: Callable[..., any]):
    @wraps(func)
    def wrapper(*args, **kwargs):
        loop = asyncio.new_event_loop()
        loop.run_until_complete(func(*args, **kwargs))
    return wrapper


@run_async
async def main():
    await db.init()
    async with websockets.serve(handler, "0.0.0.0", 5001):
        await asyncio.Future()


if __name__ == "__main__":
    main()
