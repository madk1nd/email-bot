from .mail import IMailReceiver


class GMailBox(IMailReceiver):

    async def get_conn(self, log, pas):
        pass

    async def get_count(self, doc):
        return 0

    async def get_unseen(self, doc):
        pass
