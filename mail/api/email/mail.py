from abc import ABCMeta, abstractmethod


class IMailReceiver(metaclass=ABCMeta):

    @abstractmethod
    async def get_conn(self, log, pas):
        raise NotImplementedError

    @abstractmethod
    async def get_count(self, doc):
        raise NotImplementedError

    @abstractmethod
    async def get_unseen(self, doc):
        raise NotImplementedError
