from unittest import mock
from unittest.mock import MagicMock

import pytest
from api.handler.message import MessageHandler
from asynctest import CoroutineMock

SEND_TO_TELEGRAM = 'api.handler.message.MessageHandler.send_to_telegram'
ON_DEFAULT = 'api.handler.message.MessageHandler.on_default'

docs = [
    [{
        'log': 'log_{}{}'.format(x, y),
        '_id': 'hash_{}{}'.format(x, y)
    } for x in range(0, 5)]
    for y in range(0, 5)]


@pytest.mark.parametrize('doc', docs)
def test_buttons(doc):
    h = MessageHandler(MagicMock(), MagicMock())
    buttons = h.to_buttons(doc)
    for button in buttons:
        assert '/mail hash_' == button[0]['callback_data'][:-2]
        assert 'log_' == button[0]['text'][:-2]


@pytest.mark.asyncio
async def test_on_login():
    handler = MessageHandler(MagicMock(), MagicMock())
    with mock.patch(SEND_TO_TELEGRAM, new=CoroutineMock()) as send:
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
    with mock.patch(SEND_TO_TELEGRAM, new=CoroutineMock()) as send:
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


@pytest.mark.asyncio
async def test_on_help():
    handler = MessageHandler(MagicMock(), MagicMock())
    with mock.patch(SEND_TO_TELEGRAM, new=CoroutineMock()) as send:
        await handler.on_help({
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
        assert args[1]['text'][:7] == 'List of'


@pytest.mark.asyncio
async def test_on_default():
    handler = MessageHandler(MagicMock(), MagicMock())
    with mock.patch(SEND_TO_TELEGRAM, new=CoroutineMock()) as send:
        await handler.on_default({
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
        assert args[1]['text'][:20] == 'Unrecognized command'


@pytest.mark.asyncio
async def test_on_accounts():
    mongo = MagicMock()
    handler = MessageHandler(MagicMock(), mongo)
    with mock.patch(SEND_TO_TELEGRAM, new=CoroutineMock()) as send:
        docs_cor = CoroutineMock()
        docs_cor.return_value = [
            {
                'log': 'text1',
                '_id': 'hash1'
            },
            {
                'log': 'text2',
                '_id': 'hash2'
            },
        ]
        with mock.patch.object(mongo, 'find_by', new=docs_cor):
            await handler.on_accounts({
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
            assert args[1]['text'] == 'At this moment you have 2 accounts:'
            assert args[1]['reply_markup']['inline_keyboard'][0][0]['callback_data'] == '/mail hash1'
            assert args[1]['reply_markup']['inline_keyboard'][1][0]['callback_data'] == '/mail hash2'


@pytest.mark.asyncio
async def test_dispatch():
    handler = MessageHandler(MagicMock(), MagicMock())

    messages = []
    for key in handler.methods.keys():
        handler.methods[key] = CoroutineMock()
        messages.append({'key': key, 'message': {'text': '{} some params'.format(key)}})

    for message in messages:
        await handler.dispatch(message)
        handler.methods[message['key']].assert_called_once()

    with mock.patch(ON_DEFAULT, new=CoroutineMock()) as default:
        await handler.dispatch({'message': {'text': 'wrong param'}})
        default.assert_called_once()

