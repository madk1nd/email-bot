import logging
from .handler import ITelegramHandler
from ..email.yandex import YandexMailBox
from ..email.gmail import GMailBox
from .register import RegHandler

logger = logging.getLogger('CallbackHandler')


class CallbackHandler(ITelegramHandler):

    __slots__ = ['methods', 'mongo', 'email_boxes', 'reg_handler']

    def __init__(self, session, mongo):
        super().__init__(session)
        self.methods = dict()
        self.mongo = mongo
        self.reg_handler = RegHandler(session, mongo)
        self.email_boxes = {
            'yandex': YandexMailBox(),
            'gmail': GMailBox()
        }
        self.init_methods()

    def init_methods(self):
        self.methods['/yandex'] = self.on_mail_choice
        self.methods['/gmail'] = self.on_mail_choice
        self.methods['/mail'] = self.on_mail
        self.methods['/answer'] = self.reg_handler.dispatch

    async def dispatch(self, update):
        logger.debug('callback_handler dispatch method call')
        method = self.methods.get(update['callback_query']['data'].split()[0])
        if method:
            await method(update)

    async def on_mail_choice(self, update):
        mail_type = update['callback_query']['data'][1:]
        method = 'sendMessage'
        text = 'In order to use *me* you must create app credentials in *{cap}*.\n' \
               'Here you can find some [instructions]' \
               '(https://yandex.com/support/passport/authorization/app-passwords.html)\n' \
               'Please do not send me your account credentials because this is *not secure*\n' \
               'Send me your login and application password by typing:\n' \
               '`/login {type} <login> <app_password>`\n' \
               'for example:\n' \
               '`/login {type} ivanov@yandex.ru your_app_pass`' \
            .format(
                cap=mail_type.capitalize(),
                type=mail_type
            )
        params = {
            'chat_id': update['callback_query']['message']['chat']['id'],
            'text': text,
            'parse_mode': 'Markdown',
            'disable_web_page_preview': True
        }
        await self.send_to_telegram(method, params)

    async def on_mail(self, update):
        object_id = update['callback_query']['data'].split()[1]
        doc = await self.mongo.find_by_id(object_id)
        # counts = await self.email_boxes[doc['mail']].get_count(doc)

        counts = 2
        method = 'sendMessage'
        text = 'All cool\n{}'.format(counts)
        params = {
            'chat_id': update['callback_query']['message']['chat']['id'],
            'text': text,
        }
        await self.send_to_telegram(method, params)
