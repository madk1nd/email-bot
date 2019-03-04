from unittest import mock
from unittest.mock import MagicMock
from asynctest import CoroutineMock, patch

import pytest

from api.handler.message import MessageHandler


def test_buttons():
    h = MessageHandler(MagicMock(), MagicMock())
    buttons = h.to_buttons([
        {
            'log': 'text1',
            '_id': 'hash1'
        },
        {
            'log': 'text2',
            '_id': 'hash2'
        },
    ])
    assert '/mail hash1' == buttons[0][0]['callback_data']
    assert 'text1' == buttons[0][0]['text']
    assert '/mail hash2' == buttons[1][0]['callback_data']
    assert 'text2' == buttons[1][0]['text']


@pytest.mark.asyncio
async def test_on_login():
    handler = MessageHandler(MagicMock(), MagicMock())
    with mock.patch('api.handler.message.MessageHandler.send_to_telegram', new=CoroutineMock()) as send:
        await handler.on_login({
            'message': {
                'chat': {
                    'id': 12
                }
            }
        })
        args, _ = send.call_args
        send.assert_called_once()
        assert args[0] == 'sendMessage'
        assert args[1]['chat_id'] == 12
        assert args[1]['parse_mode'] == 'markdown'
        assert args[1]['reply_markup']['inline_keyboard'][0][0]['text'] == 'Yandex'
        assert args[1]['reply_markup']['inline_keyboard'][0][1]['text'] == 'Gmail'


@pytest.mark.asyncio
async def test_on_start():
    handler = MessageHandler(MagicMock(), MagicMock())
    with mock.patch('api.handler.message.MessageHandler.send_to_telegram', new=CoroutineMock()) as send:
        await handler.on_start({
            'message': {
                'chat': {
                    'id': 12
                }
            }
        })
        args, _ = send.call_args
        send.assert_called_once()
        assert args[0] == 'sendMessage'
        assert args[1]['chat_id'] == 12
        assert args[1]['text'][:6] == 'Hello!'
        assert args[1]['reply_markup']['inline_keyboard'][0][0]['text'] == 'Yandex'
        assert args[1]['reply_markup']['inline_keyboard'][0][1]['text'] == 'Gmail'
