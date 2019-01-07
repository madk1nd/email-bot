import asyncio
import aiohttp
from config import TOKEN, IP, PORT


class WebhookEmulator:
    __slots__ = ['loop', 'session', 'token', 'offset']

    def __init__(self, loop, token):
        self.loop = loop
        self.session = None
        self.token = token
        self.offset = None

    async def connect(self):
        self.session = aiohttp.ClientSession()
        print('Connected!')

    async def __call__(self, *args, **kwargs):
        telegram_url = 'https://api.telegram.org/bot{token}/getUpdates'.format(token=self.token)
        await self.connect()

        while True:
            print('check for updates')
            await asyncio.sleep(1)
            params = {'offset': self.offset, 'timeout': 20} if self.offset else {'timeout': 20}
            async with self.session.get(url=telegram_url, params=params) as response:
                updates = await response.json()
                print(updates)
                if updates['result']:
                    await self.send_to_bot(updates)

    async def send_to_bot(self, data):
        email_bot_url = 'https://{ip}:{port}/updates/{token}'.format(
            ip=IP,
            port=PORT,
            token=self.token
        )
        async with self.session.post(url=email_bot_url, ssl=False, json=data) as resp:
            if resp.status == 200:
                self.offset = max(update['update_id'] for update in data['result']) + 1


def main():
    if not TOKEN:
        raise Exception('Can\'t find bot token in environment (BOT_TOKEN) --> Failed to start')
    print("Emulator Started")
    loop = asyncio.get_event_loop()
    emulator = WebhookEmulator(loop, TOKEN)
    try:
        loop.run_until_complete(emulator())
    except KeyboardInterrupt:
        loop.stop()
