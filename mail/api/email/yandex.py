import imaplib
from .mail import IMailReceiver


class YandexMailBox(IMailReceiver):

    async def get_conn(self, log, pas):
        conn = imaplib.IMAP4_SSL('imap.yandex.ru')
        conn.login(log, pas)
        return conn

    async def get_unseen(self, doc):
        pass

    async def get_count(self, doc):
        conn = await self.get_conn(doc['log'], doc['pass'])
        status, select_data = conn.select('INBOX')
        all_count = select_data[0].decode('utf-8')
        typ, data = conn.search(None, 'NEW')
        new_count = len(data[0])
        typ, data = conn.search(None, 'UNSEEN')
        unseen_count = len(data[0])
        conn.logout()
        return {
            'all': all_count,
            'new': new_count,
            'unseen': unseen_count
        }
