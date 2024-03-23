import asyncio
import os.path
import multiprocessing

import websockets
from aiohttp import web
from socket_server import main


import db

PORT = 3000


EXTENSIONS_MAPPINGS = {
    'css': 'css',
    'png': 'picture'
}


async def handle_index(request):
    return web.FileResponse('html/index.html')


async def handle_message(request):
    return web.FileResponse('html/message.html')


async def handle_static(request):
    path = request.path
    file_extension = path[path.rfind('.') + 1:]
    file = f'./{EXTENSIONS_MAPPINGS.get(file_extension, "")}' + path
    if os.path.exists(file):
        return web.FileResponse(file)
    return web.FileResponse('html/error.html')


async def handle_error(request):
    return web.FileResponse('html/error.html')


async def handle_message_form(request):
    data = await request.post()
    message = data.get('message')
    username = data.get('username')
    if message and username:
        await send_to_socket(message, username)
        return web.Response(text="Message sent successfully!")
    else:
        return web.Response(text="Error: Both message and username are required.", status=400)


async def send_to_socket(message, username):
    # ws = await websockets.connect(uri="ws://host.docker.internal:5001")
    ws = await websockets.connect(uri="ws://localhost:5001")
    message = db.Message(message=message, username=username).json()
    await ws.send(message=message)


app = web.Application()
app.router.add_get('/', handle_index)
app.router.add_get('/index.html', handle_index)
app.router.add_get('/message', handle_message)
app.router.add_get('/message.html', handle_message)
app.router.add_post('/message', handle_message_form)
app.router.add_post('/message.html', handle_message_form)
app.router.add_get('/{file}', handle_static)
app.router.add_get('/*', handle_error)


def run_app():
    loop = asyncio.new_event_loop()
    loop.run_until_complete(db.init())
    web.run_app(app, port=PORT, loop=loop)


if __name__ == "__main__":
    processes = [
        multiprocessing.Process(target=run_app),
        multiprocessing.Process(target=main)
    ]

    for process in processes:
        process.start()

    for process in processes:
        process.join()
