import logging
import aiohttp
from .config import TELEGRAM_API


logger = logging.getLogger('Dispatcher')


class Dispatcher:
    __slots__ = ['methods', 'session']

    def __init__(self):
        self.methods = dict()
        self.add_methods()
        self.session = aiohttp.ClientSession()

    def add_methods(self):
        self.methods['/start'] = self.on_start
        self.methods['/help'] = self.on_help

    async def dispatch(self, update):
        handler = self.methods.get(update['message']['text'])
        if handler:
            await handler(update)
        else:
            await self.default_handler(update)

    async def on_start(self, update):
        method = 'sendMessage'
        text = 'Hello! I\'m your https://youtu.be/zqxVI_kEdq8 personal email manager!\n' \
               'What kind of mail box do you want to manage?'
        buttons = {
            'inline_keyboard': [
                [
                    {
                        'text': 'Yandex',
                        'callback_data': '/yandex'
                    },
                    {
                        'text': 'Gmail',
                        'callback_data': '/gmail'
                    }
                ],
                [
                    {
                        'text': 'Test',
                        'callback_data': '/test'
                    }
                ]
            ]
        }
        await self.send_to_telegram(method, text, update, buttons=buttons)

    async def on_help(self, update):
        method = 'sendMessage'
        text = """"""
        await self.send_to_telegram(method, text, update)

    async def default_handler(self, update):
        text = 'Unrecognized command - try to type /help to list all available commands'
        await self.send_to_telegram('sendMessage', text, update)

    async def send_to_telegram(self, method, text, update, buttons=None):
        params = {
            'chat_id': update['message']['chat']['id'],
            'text': text,
        }
        if buttons:
            params['reply_markup'] = buttons
        async with self.session.post(TELEGRAM_API + '/' + method, json=params) as response:
            data = await response.json()
            status = response.status
            log_message = 'telegram api method :: {method} ' \
                          'response with code :: {status} ' \
                          'and data :: {json}'
            logger.debug(log_message.format(
                method=method,
                status=status,
                json=data
            ))
