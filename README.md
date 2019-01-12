# email-bot
Telegram bot to optimize email processing

### Certificates
Please use certificates and keys stored in cert directory only for testing purposes.

### Start services
To be able to use this services you need to store your telegram bot token in the environment variable named BOT_TOKEN.
You can do this by executing following line of code in the terminal:

    $ export BOT_TOKEN='<your_bot_token>'
    
Then you will be able to start service through the command

    $ bin/watch 
    
### Emulator
This service will work only if telegram webhooks is already setup
and telegram already know were to send messages. If not you can use 
service emulator to emulate telegram webhooks through the long polling 
getUpdates() method. To do so you need to run command:

    $ bin/emulate