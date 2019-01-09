from os import environ

IP = environ.get('MAIL_BOT_IP', 'localhost')
PORT = int(environ.get('MAIL_BOT_PORT', '8081'))
MAIL_CERT_PATH = environ.get('MAIL_CERT_PATH')
TOKEN = environ.get('BOT_TOKEN')
MONGO_URL = environ.get('MAIL_MONGO_URL', 'mongodb://localhost:27017')
TELEGRAM_API = 'https://api.telegram.org/bot{token}'.format(token=TOKEN)
# AES key must be either 16, 24, or 32 bytes long
PRIVATE_PATH = environ.get('MAIL_PRIVATE_SECRET')
PUBLIC_PATH = environ.get('MAIL_PUBLIC_SECRET')
