import pymongo
from motor.motor_asyncio import AsyncIOMotorClient
from bson.objectid import ObjectId
from ..config import MONGO_URL
from ..db.decoder import encode, decode


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
        await self.col.insert_one({
            'chat': chat,
            'mail': mail,
            'log': encode(log),
            'pass': encode(pas)
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
        doc['log'] = decode(doc['log'])
        doc['pass'] = decode(doc['pass'])
        return doc
