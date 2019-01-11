from os import environ

TOKEN = environ.get('BOT_TOKEN')
IP = environ.get('MAIL_BOT_IP', 'localhost')
PORT = int(environ.get('MAIL_BOT_PORT', '8081'))

MONGO_URL = environ.get('MAIL_MONGO_URL', 'mongodb://localhost:27017')
TELEGRAM_API = 'https://api.telegram.org/bot{token}'.format(token=TOKEN)

PRIVATE_PATH = environ.get('MAIL_PRIVATE_SECRET', 'cert/cert.key')
PUBLIC_PATH = environ.get('MAIL_PUBLIC_SECRET', 'cert/cert.pem')
ENC_KEY = environ.get('ENC_KEY', 'cert/encryption.key')
ENC_PUB = environ.get('ENC_PUB', 'cert/encryption.pem')
