import pymongo
from motor.motor_asyncio import AsyncIOMotorClient
from bson.objectid import ObjectId
from ..config import MONGO_URL, SECRET
from simplecrypt import encrypt, decrypt
import time


class MongoClient:
    __slots__ = (
        'client', 'db', 'col'
    )

    def __init__(self):
        self.client = None
        self.db = None
        self.col = None

    async def on_startup(self):
        self.client = AsyncIOMotorClient(MONGO_URL)
        self.db = self.client['email']
        self.col = self.db['users']
        await self.col.create_index([('chat', pymongo.HASHED)])

    async def insert(self, chat, mail, log, pas):
        t = int(round(time.time() * 1000))
        s = encrypt(SECRET, log)
        print(s)
        end = int(round(time.time() * 1000))
        print(end - t)
        await self.col.insert_one({
            'chat': chat,
            'mail': mail,
            'log': encrypt(SECRET, log),
            'pass': encrypt(SECRET, pas)
        })

    async def find_by(self, chat):
        q = self.col.find({
            'chat': chat,
        })
        return [self.map(doc) async for doc in q]

    async def find_by_id(self, object_id):
        doc = await self.col.find_one({
            '_id': ObjectId(object_id),
        })
        return self.map(doc)

    async def delete_by(self, object_id):
        await self.col.delete_many({'_id': ObjectId(object_id)})

    @staticmethod
    def map(doc):
        doc['log'] = decrypt(SECRET, doc['log'])
        doc['pass'] = decrypt(SECRET, doc['pass'])
        return doc
