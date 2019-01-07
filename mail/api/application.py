import sys
import ssl
import logging
from aiohttp import web
from aiohttp_swagger import setup_swagger
from .config import IP, PORT, MAIL_CERT_PATH, TOKEN
from .views import routes

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def main():
    app = web.Application()
    app.router.add_routes(routes)

    setup_swagger(app)

    context = prepare_ssl()
    web.run_app(app, host=IP, port=PORT, ssl_context=context)


def prepare_ssl():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    if not MAIL_CERT_PATH:
        raise Exception('Can\'t find certificates MAIL_CERT_PATH--> Failed to start')
    if not TOKEN:
        raise Exception('Can\'t find bot token (BOT_TOKEN) --> Failed to start')
    context.load_cert_chain(
        MAIL_CERT_PATH + 'email_bot.pem',
        MAIL_CERT_PATH + 'email_bot_private.key'
    )
    return context
