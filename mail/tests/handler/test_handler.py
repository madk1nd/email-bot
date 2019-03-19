import asyncio
from unittest.mock import MagicMock

import aiohttp
import pytest
from api.config import TELEGRAM_API
from api.handler.handler import ITelegramHandler
from asynctest import CoroutineMock
from asynctest import patch


class SimpleHandler(ITelegramHandler):

    def __init__(self, session):
        super().__init__(session)

    async def dispatch(self):
        await asyncio.sleep(0)


class AsyncContextManagerMock(MagicMock):
    async def __aenter__(self):
        self.aenter.status = 'ok'
        return self.aenter

    async def __aexit__(self, *args):
        pass


@pytest.mark.asyncio
@patch('aiohttp.ClientSession.post', new_callable=AsyncContextManagerMock)
async def test_dispatch(post):
    coroutine = CoroutineMock()
    session = aiohttp.ClientSession()
    post.return_value.aenter.json.side_effect = coroutine
    handler = SimpleHandler(session)
    params = {'test': 'ok'}
    method = 'messageSend'

    await handler.send_to_telegram(method, params=params)

    post.assert_called_once_with(TELEGRAM_API + '/' + method, json=params)

