import logging
from .handler import ITelegramHandler
from ..email.yandex import YandexMailBox
from ..email.gmail import GMailBox

logger = logging.getLogger('CallbackHandler')


class CallbackHandler(ITelegramHandler):

    __slots__ = ['methods', 'mongo', 'email_boxes']

    def __init__(self, session, mongo):
        super().__init__(session)
        self.methods = dict()
        self.init_methods()
        self.mongo = mongo
        self.email_boxes = {
            'yandex': YandexMailBox(),
            'gmail': GMailBox()
        }

    def init_methods(self):
        self.methods['/yandex'] = self.on_yandex
        self.methods['/gmail'] = self.on_gmail
        self.methods['/mail'] = self.on_mail

    async def dispatch(self, update):
        logger.debug('callback_handler dispatch method call')
        method = self.methods.get(update['callback_query']['data'].split()[0])
        if method:
            await method(update)

    async def on_yandex(self, update):
        method = 'sendMessage'
        text = 'I order to use *me* you must create app credentials in *Yandex*.\n' \
               'Here you can find some [instructions]' \
               '(https://yandex.com/support/passport/authorization/app-passwords.html)\n' \
               'Please do not send me your account credentials because this is *not secure*\n' \
               'Send me your login and application password by typing:\n' \
               '`/login <mail_type> <login> <app_password>`\n' \
               'for example:\n' \
               '`/login yandex ivanov@yandex.ru your_app_pass`'
        params = {
            'chat_id': update['callback_query']['message']['chat']['id'],
            'text': text,
            'parse_mode': 'Markdown'
        }
        await self.send_to_telegram(method, params)

    async def on_gmail(self, update):
        method = 'sendMessage'
        text = 'I order to use *me* you must create app credentials in *Google*.\n' \
               'Here you can find some [instructions]' \
               '(https://support.google.com/mail/answer/185833?hl=en)\n' \
               'Please do not send me your account credentials because this is *not secure*\n' \
               'Send me your login and application password by typing:\n' \
               '`/login <mail_type> <login> <app_password>`\n' \
               'for example:\n' \
               '`/login gmail ivanov@yandex.ru your_app_pass`'
        params = {
            'chat_id': update['callback_query']['message']['chat']['id'],
            'text': text,
            'parse_mode': 'Markdown'
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
