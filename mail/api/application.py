from aiohttp import web
from .config import IP, PORT


def main():
    app = web.Application()

    print('Start app')
    web.run_app(app, host=IP, port=PORT)
