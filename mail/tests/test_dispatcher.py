from unittest import mock
from unittest.mock import MagicMock

import pytest
from api.dispatcher import Dispatcher
from asynctest import CoroutineMock


@pytest.mark.asyncio
async def test_on_dispatch_message():
    dispatcher = Dispatcher(MagicMock())
    update = {'message': {'text': 'test', 'chat': {'id': 12}}}
    with mock.patch('api.handler.message.MessageHandler.dispatch', new=CoroutineMock()) as dispatch:
        await dispatcher.dispatch(update)
        dispatch.assert_called_once_with(update)


@pytest.mark.asyncio
async def test_on_dispatch_callback():
    dispatcher = Dispatcher(MagicMock())
    update = {'callback_query': {'text': 'test', 'chat': {'id': 12}}}
    with mock.patch('api.handler.callback.CallbackHandler.dispatch', new=CoroutineMock()) as dispatch:
        await dispatcher.dispatch(update)
        dispatch.assert_called_once_with(update)


@pytest.mark.asyncio
async def test_on_dispatch_error():
    dispatcher = Dispatcher(MagicMock())
    update = {'test': {'text': 'test', 'chat': {'id': 12}}}
    try:
        await dispatcher.dispatch(update)
        assert False
    except Exception as e:
        assert True
