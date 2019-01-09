from aiohttp import web
from . import routes
from ..config import TOKEN


@routes.post('/updates/{token}'.format(token=TOKEN))
async def dispatch(req):
    data = await req.json()
    updates = data['result']
    if updates:
        for update in updates:
            await req.app['dispatcher'].dispatch(update)
    return web.Response()
