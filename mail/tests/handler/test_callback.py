from unittest import mock
from unittest.mock import MagicMock

import pytest
from api.handler.callback import CallbackHandler
from asynctest import CoroutineMock

SEND_TO_TELEGRAM = 'api.handler.callback.CallbackHandler.send_to_telegram'


@pytest.mark.asyncio
async def test_dispatch():
    handler = CallbackHandler(MagicMock(), MagicMock())

    messages = []
    for key in handler.methods.keys():
        handler.methods[key] = CoroutineMock()
        messages.append({'key': key, 'callback_query': {'data': '{} some params'.format(key)}})

    for message in messages:
        await handler.dispatch(message)
        handler.methods[message['key']].assert_called_once()


@pytest.mark.asyncio
async def test_on_yandex():
    handler = CallbackHandler(MagicMock(), MagicMock())
    with mock.patch(SEND_TO_TELEGRAM, new=CoroutineMock()) as send:
        await handler.on_yandex({
            'callback_query': {
                'message': {
                    'chat': {
                        'id': 12
                    }
                }
            }
        })
        args, _ = send.call_args
        send.assert_called_once()
        assert args[0] == 'sendMessage'
        assert args[1]['chat_id'] == 12
        assert args[1]['text'][57:63] == 'Yandex'
        assert args[1]['parse_mode'] == 'Markdown'
        assert args[1]['disable_web_page_preview'] is True


@pytest.mark.asyncio
async def test_on_gmail():
    handler = CallbackHandler(MagicMock(), MagicMock())
    with mock.patch(SEND_TO_TELEGRAM, new=CoroutineMock()) as send:
        await handler.on_gmail({
            'callback_query': {
                'message': {
                    'chat': {
                        'id': 12
                    }
                }
            }
        })
        args, _ = send.call_args
        send.assert_called_once()
        assert args[0] == 'sendMessage'
        assert args[1]['chat_id'] == 12
        assert args[1]['text'][57:63] == 'Google'
        assert args[1]['parse_mode'] == 'Markdown'
        assert args[1]['disable_web_page_preview'] is True


@pytest.mark.asyncio
async def test_on_mail():
    mongo = MagicMock()
    handler = CallbackHandler(MagicMock(), mongo)
    with mock.patch(SEND_TO_TELEGRAM, new=CoroutineMock()) as send:
        with mock.patch.object(mongo, 'find_by_id', new=CoroutineMock()) as find:
            await handler.on_mail({
                'callback_query': {
                    'data': 'test 5c364c919303fc1628b07bf2',
                    'message': {
                        'chat': {
                            'id': 12
                        }
                    }
                }
            })
            find.assert_called_once_with('5c364c919303fc1628b07bf2')

            args, _ = send.call_args
            send.assert_called_once()
            assert args[0] == 'sendMessage'
            assert args[1]['chat_id'] == 12
