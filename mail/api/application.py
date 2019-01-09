import sys
import ssl
import logging
from aiohttp import web
from aiohttp_swagger import setup_swagger
from .config import IP, PORT, MAIL_CERT_PATH, TOKEN, PRIVATE_PATH, PUBLIC_PATH
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

    check_var(MAIL_CERT_PATH)
    check_var(TOKEN)
    check_var(PRIVATE_PATH)
    check_var(PUBLIC_PATH)

    context.load_cert_chain(
        MAIL_CERT_PATH + 'email_bot.pem',
        MAIL_CERT_PATH + 'email_bot_private.key'
    )
    return context


def check_var(var):
    if not var:
        raise Exception('Can\'t find ({}) --> Failed to start'.format(var))
