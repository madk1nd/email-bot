import logging
import aiohttp
from .handler.message import MessageHandler
from .handler.callback import CallbackHandler


logger = logging.getLogger('Dispatcher')


class Dispatcher:
    __slots__ = ['session', 'handlers']

    def __init__(self, mongo):
        self.session = aiohttp.ClientSession()
        self.handlers = [
            MessageHandler(self.session, mongo),
            CallbackHandler(self.session, mongo)
        ]

    async def dispatch(self, update):
        if update.get('message'):
            handler = self.handlers[0]
        elif update.get('callback_query'):
            handler = self.handlers[1]
        else:
            raise Exception('Unexpected update type')
        await handler.dispatch(update)
