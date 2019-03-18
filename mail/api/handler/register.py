import logging
from .handler import ITelegramHandler, button_row

logger = logging.getLogger('RegHandler')


class RegHandler(ITelegramHandler):

    __slots__ = ['mongo', 'methods']

    def __init__(self, session, mongo):
        super().__init__(session)
        self.mongo = mongo
        self.methods = dict()
        self.init_methods()

    def init_methods(self):
        self.methods['Gmail'] = self.on_mail_choose
        self.methods['Yandex'] = self.on_mail_choose
        self.methods['done'] = self.on_done

    async def dispatch(self, update):
        command = update['callback_query']['data'].split()[1]
        method = self.methods.get(command)
        if method:
            await method(update)
        else:
            await self.char_press(update)

    async def on_mail_choose(self, update):
        command = update['callback_query']['data'].split()[1]
        logger.debug('on_mail_choose method :: {}'.format(command))
        message = update['callback_query']['message']
        method = 'editMessageText'
        buttons = {
            'inline_keyboard': [
                button_row('q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'),
                button_row('a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', '-'),
                button_row('z', 'x', 'c', 'v', 'b', 'n', 'm', '.', '_', '@'),
                button_row('⬅️', 'done')
            ]
        }
        params = {
            'chat_id': message['chat']['id'],
            'message_id': message['message_id'],
            'text': 'Ok! We will register {} account!\n'
                    'Please insert your account name through the buttons clicks:\n'
                    'Account: \n'
                    'Press done button when you will be ready!'.format(command),
            'parse_mode': 'markdown',
            'reply_markup': buttons
        }
        await self.send_to_telegram(method, params)

    async def on_done(self, update):
        logger.debug('on_done method')

    async def char_press(self, update):
        text = update['callback_query']['message']['text']
        l = text.split()
        logger.debug('on_char_press method :: {}'.format(l.index('Account:')))
