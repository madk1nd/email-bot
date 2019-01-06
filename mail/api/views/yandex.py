import base64
import json
import logging
import imaplib
import email
import email.message
from aiohttp import web
from . import routes

logger = logging.getLogger('Yandex Mail')


@routes.post('/test')
async def test(req):
    """
    ---
    description: This end-point allow to test that service is up.
    tags:
    - Health check
    produces:
    - text/plain
    responses:
        "200":
            description: successful operation. Return "pong" text
        "405":
            description: invalid HTTP Method
    """

    logger.info('query :: {}'.format(req.query))

    data = await req.json()
    logger.info('body number :: {}'.format(data))
    response_obj = {'status': data}

    conn = get_conn()
    # conn.select('INBOX')
    # (retcode, messages) = conn.search(None, '(UNSEEN)')

    logger.info('unseen count :: {}'.format(get_unseen_count(conn)))
    # logger.info(type(messages))
    # logger.info(messages[0])

    # if retcode == 'OK':
    #     inbox = [get_msg(num, conn) for num in messages[0].split()]
    #     logger.info('inbox :: {}'.format(inbox))

    # conn.select('INBOX')
    # status, data = conn.fetch(b'1333', '(RFC822)')
    # msg = email.message_from_bytes(data[0][1], _class=email.message.EmailMessage)
    # logger.info('message :: {}'.format(type(msg)))
    # logger.info('message keys :: {}'.format(msg.keys()))
    # logger.info('message from :: {}'.format(msg['From']))
    conn.logout()

    return web.Response(text=json.dumps(response_obj))


# class Yandex:
#     __slots__ = 'conn'
#
#     def __init__(self, conn):
#
#
#


def get_unseen_count(conn):
    conn.select('INBOX')
    (code, messages) = conn.search(None, '(UNSEEN)')
    if code == 'OK':
        return len(messages[0].split())
    else:
        raise Exception('Can\'t connect to mail server')


def get_conn():
    conn = imaplib.IMAP4_SSL('imap.yandex.ru')
    conn.login('madk1nd@yandex.ru', 'vbmstefoscpvxvsa')
    return conn


def decode(data):
    data_split_ = data.split()[0]
    if '?' in data_split_:
        split_ = data_split_.split('?')[3]
        logger.info('split :: {}'.format(split_))
        res = base64.b64decode(split_).decode('utf-8')
        logger.info('data :: {}'.format(data))
        return res
    else:
        return data


def get_msg(num, conn):
    typ, data = conn.fetch(num, '(RFC822)')
    msg = email.message_from_bytes(data[0][1], _class=email.message.EmailMessage)
    typ, data = conn.store(num, '-FLAGS', '\\Seen')
    logger.info('{}{}{}'.format(data, '\n', 30 * '-'))
    logger.info('message :: {}'.format(decode(msg['From'])))
    return msg['From']
