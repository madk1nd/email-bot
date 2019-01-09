import logging
from ..config import TELEGRAM_API
from abc import ABCMeta, abstractmethod

logger = logging.getLogger('ITelegramHandler')


class ITelegramHandler(metaclass=ABCMeta):

    __slots__ = ['session']

    def __init__(self, session):
        self.session = session

    @abstractmethod
    async def dispatch(self, update):
        raise NotImplementedError

    async def send_to_telegram(self, method, params=None):
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
