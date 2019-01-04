import json
import logging
from aiohttp import web
from . import routes

logger = logging.getLogger('Yandex Mail')


@routes.post('/test')
async def test(req):
    """
    ---
    description: This end-point allow to test that service is up.
    tags:
    - Health check
    produces:
    - text/plain
    responses:
        "200":
            description: successful operation. Return "pong" text
        "405":
            description: invalid HTTP Method
    """

    logger.info('query :: {}'.format(req.query))
    data = await req.json()

    logger.info('body number :: {}'.format(data))
    response_obj = {'status': data}

    return web.Response(text=json.dumps(response_obj))
