from os import environ

IP = environ.get('MAIL_BOT_IP', 'localhost')
PORT = int(environ.get('MAIL_BOT_PORT', '8081'))
TOKEN = environ.get('BOT_TOKEN')
