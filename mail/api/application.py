import sys
import logging
from aiohttp import web
from aiohttp_swagger import setup_swagger
from .config import IP, PORT
from .views import routes

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def main():
    app = web.Application()
    app.router.add_routes(routes)

    setup_swagger(app)

    web.run_app(app, host=IP, port=PORT)
