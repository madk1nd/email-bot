import sys
import ssl
import logging
from aiohttp import web
from aiohttp_swagger import setup_swagger
from .config import IP, PORT, TOKEN, PRIVATE_PATH, PUBLIC_PATH
from .views import routes
from .dispatcher import Dispatcher
from .db.mongo import MongoClient

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def main():
    app = web.Application()
    app.router.add_routes(routes)

    client = MongoClient()
    app['mongo'] = client
    app['dispatcher'] = Dispatcher(client)
    app.on_startup.append(on_startup)

    setup_swagger(app)

    context = prepare_ssl()
    web.run_app(app, host=IP, port=PORT, ssl_context=context)


async def on_startup(app):
    await app['mongo'].on_startup()


def prepare_ssl():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    check_var(TOKEN, 'BOT_TOKEN')
    context.load_cert_chain(PUBLIC_PATH, PRIVATE_PATH)
    return context


def check_var(var, name):
    if not var:
        raise Exception('Can\'t find ({}) --> Failed to start'.format(name))
