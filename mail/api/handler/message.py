import logging
from .handler import ITelegramHandler, button_row


logger = logging.getLogger('MessageHandler')


class MessageHandler(ITelegramHandler):

    __slots__ = ['methods', 'mongo', 'login_handler']

    def __init__(self, session, mongo):
        super().__init__(session)
        self.methods = dict()
        self.mongo = mongo
        self.init_methods()

    def init_methods(self):
        self.methods['/start'] = self.on_start
        self.methods['/help'] = self.on_help
        self.methods['/login'] = self.on_login
        self.methods['/accounts'] = self.on_accounts

    async def dispatch(self, update):
        method = self.methods.get(update['message']['text'].split()[0])
        if method:
            await method(update)
        else:
            await self.on_default(update)

    async def on_login(self, update):
        chat_id = update['message']['chat']['id']
        method = 'sendMessage'
        buttons = {
            'inline_keyboard': [
                button_row('Yandex', 'Gmail')
            ]
        }
        await self.send_to_telegram(method, {
            'chat_id': chat_id,
            'text': 'Ok. Let\'s start to register new account!\n'
                    'Please choose mailbox type:',
            'parse_mode': 'markdown',
            'reply_markup': buttons
        })

    async def on_start(self, update):
        method = 'sendMessage'
        text = 'Hello! I\'m your personal email manager!\n' \
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
                ]
            ]
        }
        params = {
            'chat_id': update['message']['chat']['id'],
            'text': text,
            'reply_markup': buttons
        }
        await self.send_to_telegram(method, params)

    async def on_help(self, update):
        method = 'sendMessage'
        text = """List of available commands:
        /start, /help
        """
        params = {
            'chat_id': update['message']['chat']['id'],
            'text': text,
        }
        await self.send_to_telegram(method, params)

    async def on_accounts(self, update):
        docs = await self.mongo.find_by(update['message']['chat']['id'])
        text = 'At this moment you have {} accounts:'.format(len(docs))
        method = 'sendMessage'
        buttons = {
            'inline_keyboard': self.to_buttons(docs)
        }
        params = {
            'chat_id': update['message']['chat']['id'],
            'text': text,
            'reply_markup': buttons
        }
        await self.send_to_telegram(method, params)

    async def on_default(self, update):
        text = 'Unrecognized command - try to type /help to list all available commands'
        params = {
            'chat_id': update['message']['chat']['id'],
            'text': text,
        }
        await self.send_to_telegram('sendMessage', params)

    @staticmethod
    def to_buttons(docs):
        return [[{
            'text': doc['log'],
            'callback_data': '/mail {}'.format(str(doc['_id']))
        }] for doc in docs]

