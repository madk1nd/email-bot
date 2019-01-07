from os import environ

IP = environ.get('MAIL_BOT_IP', 'localhost')
PORT = int(environ.get('MAIL_BOT_PORT', '8081'))
MAIL_CERT_PATH = environ.get('MAIL_CERT_PATH')
TOKEN = environ.get('BOT_TOKEN')
TELEGRAM_API = 'https://api.telegram.org/bot{token}'.format(token=TOKEN)
