import json
import logging
from aiohttp import web
from . import routes

logger = logging.getLogger('Yandex Mail')


@routes.post('/test')
async def test(req):
    logger.info('query :: {}'.format(req.query))
    data = await req.json()

    logger.info('body number :: {}'.format(data))
    response_obj = {'status': data}

    return web.Response(text=json.dumps(response_obj))
