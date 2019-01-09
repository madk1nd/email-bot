import logging
from .handler import ITelegramHandler


logger = logging.getLogger('MessageHandler')


class MessageHandler(ITelegramHandler):

    __slots__ = ['methods', 'mongo']

    def __init__(self, session, mongo):
        super().__init__(session)
        self.methods = dict()
        self.init_methods()
        self.mongo = mongo

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

    async def on_login(self, update):
        command = update['message']['text'].split()
        if len(command) == 4:
            mail_box = command[1]
            logger.debug('mail_box :: {}'.format(mail_box))
            args = command[2:4]
            logger.debug('args :: {}'.format(args))
            await self.mongo.insert(
                update['message']['chat']['id'],
                mail_box,
                args[0],
                args[1]
            )
        method = 'sendMessage'
        text = 'success'
        params = {
            'chat_id': update['message']['chat']['id'],
            'text': text,
        }
        await self.send_to_telegram(method, params)

    async def on_accounts(self, update):
        docs = await self.mongo.find_by(update['message']['chat']['id'])
        logger.debug(docs)
        # text = 'At this moment you have {} accounts:'.format(len(docs))
        text = str(docs)
        method = 'sendMessage'
        buttons = {
            'inline_keyboard': [self.to_buttons(docs)]
        }
        params = {
            'chat_id': update['message']['chat']['id'],
            'text': text,
            # 'reply_markup': buttons
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
        # print(docs[0]['log'])
        return [{
            'text': doc['log'],
            'callback_data': '/mail {}'.format(str(doc['_id']))
        } for doc in docs]
