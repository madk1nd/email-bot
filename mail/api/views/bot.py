from aiohttp import web
from . import routes
from ..config import TOKEN
from ..dispatcher import Dispatcher

dispatcher = Dispatcher()


@routes.post('/updates/{token}'.format(token=TOKEN))
async def dispatch(req):
    data = await req.json()
    updates = data['result']
    if updates:
        for update in updates:
            await dispatcher.dispatch(update)
    return web.Response()
