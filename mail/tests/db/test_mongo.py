import asyncio
import pymongo
from unittest import mock
from unittest.mock import MagicMock
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection, AsyncIOMotorClient

from bson.objectid import ObjectId

import pytest
from asynctest import CoroutineMock

from api.db.mongo import MongoClient


# {
#     '_id': ObjectId('5c364c919303fc1628b07bf2'),
#     'chat': 220753323,
#     'mail': 'yandex',
#     'log': 'test@test.ru',
#     'pass': 'password'
# }
CREATE_INDEX = 'motor.motor_asyncio.AsyncIOMotorCollection.create_index'


@pytest.mark.asyncio
async def test_find_by_id():
    mock_col = MagicMock()
    cor_mock = CoroutineMock()
    cor_mock.return_value = {
        'chat': 220753323,
        'mail': 'yandex',
        'log': b'efolNrbncKXV7W2zBwPoxZH6nu2rQTuM0-GO1RZFZFKtBXlCwogZW8'
               b'XKndb576hMenNXecSWUHCBMCa5gh41cVIqy-uwc0e_R3_Xm5zoLsQI'
               b'pljy_SFNojwjADCLSNU75Q0tNmnND6U569Byj0TzkBibNbWuwxPam7'
               b'sPQiwZncJnfOxqyszDOHWoevXzf5WBfp6uxbwXY6seEEl64cPj53LZ'
               b'rgK4EkcrRkuINhzl8RTDtvt4RMdgwpyRau1bvzqAEMW8NbGsE0aTAF'
               b'fm-pdDNDH8VizbtwZY5t4dUWLAfJeHf9RcWHT37dQSIviJqImQD-QV'
               b'ulQN7BvyTNiRYdzkyA==',
        'pass': b'maHSWleb_MZvgaxBk6H1UNQet0fowTGMuBnxsxnl3IGFkfhWFFOuq'
                b'bxWPFNB3XFkxV_YOwyXOlVhRZGweIoECb3253PZuuFOyFcscF4mwT'
                b'Mw9vHUfN64-f-ogUzAAySKBnekk-lBEQ3TvfIepQK6uQkm0o00w0B'
                b'POBXCnb0pfR_cgMpKRAzkNHEFPLRxQ9cUIK5l1RjXysPQuEYvLY_u'
                b'dOzPouZFtrDplEVnrQRqHy-sadOUKM-CZnI-ODawSPNUEKp7rWxCR'
                b'18qfVXicBWWw3QJO8bF2sUDX5Q1p23u-JDVz6hSEdqqDZbLzNHPgH'
                b'vI62erOjPqDT30hzPk0-iFdQ=='
    }
    mongo = MongoClient()
    mongo.col = mock_col
    with mock.patch.object(mock_col, 'find_one', new=cor_mock):
        doc = await mongo.find_by_id('5c364c919303fc1628b07bf2')
        assert doc['chat'] == 220753323
        assert doc['log'] == 'test@test.ru'
        assert doc['pass'] == 'password'


@pytest.mark.asyncio
async def test_delete_by():
    mock_col = MagicMock()
    cor_mock = CoroutineMock()
    mongo = MongoClient()
    mongo.col = mock_col
    with mock.patch.object(mock_col, 'delete_many', new=cor_mock) as delete:
        await mongo.delete_by('5c364c919303fc1628b07bf2')
        args, _ = delete.call_args
        delete.assert_called_once()
        assert args[0] == {'_id': ObjectId('5c364c919303fc1628b07bf2')}


@pytest.mark.asyncio
async def test_insert():
    mock_col = MagicMock()
    cor_mock = CoroutineMock()
    mongo = MongoClient()
    mongo.col = mock_col
    with mock.patch.object(mock_col, 'insert_one', new=cor_mock) as insert:
        await mongo.insert(12, 'yandex', 'login', 'password')
        args, _ = insert.call_args
        insert.assert_called_once()
        assert args[0]['chat'] == 12
        assert args[0]['mail'] == 'yandex'
        assert type(args[0]['log']) is bytes
        assert type(args[0]['pass']) is bytes


async def agen():
    yield {
        'chat': 220753323,
        'mail': 'yandex',
        'log': b'efolNrbncKXV7W2zBwPoxZH6nu2rQTuM0-GO1RZFZFKtBXlCwogZW8'
               b'XKndb576hMenNXecSWUHCBMCa5gh41cVIqy-uwc0e_R3_Xm5zoLsQI'
               b'pljy_SFNojwjADCLSNU75Q0tNmnND6U569Byj0TzkBibNbWuwxPam7'
               b'sPQiwZncJnfOxqyszDOHWoevXzf5WBfp6uxbwXY6seEEl64cPj53LZ'
               b'rgK4EkcrRkuINhzl8RTDtvt4RMdgwpyRau1bvzqAEMW8NbGsE0aTAF'
               b'fm-pdDNDH8VizbtwZY5t4dUWLAfJeHf9RcWHT37dQSIviJqImQD-QV'
               b'ulQN7BvyTNiRYdzkyA==',
        'pass': b'maHSWleb_MZvgaxBk6H1UNQet0fowTGMuBnxsxnl3IGFkfhWFFOuq'
                b'bxWPFNB3XFkxV_YOwyXOlVhRZGweIoECb3253PZuuFOyFcscF4mwT'
                b'Mw9vHUfN64-f-ogUzAAySKBnekk-lBEQ3TvfIepQK6uQkm0o00w0B'
                b'POBXCnb0pfR_cgMpKRAzkNHEFPLRxQ9cUIK5l1RjXysPQuEYvLY_u'
                b'dOzPouZFtrDplEVnrQRqHy-sadOUKM-CZnI-ODawSPNUEKp7rWxCR'
                b'18qfVXicBWWw3QJO8bF2sUDX5Q1p23u-JDVz6hSEdqqDZbLzNHPgH'
                b'vI62erOjPqDT30hzPk0-iFdQ=='
    }


class Aiter:
    def __init__(self):
        self.stop = False

    def __aiter__(self):
        return self

    async def __anext__(self):
        await asyncio.sleep(0)
        if not self.stop:
            self.stop = True
            return {
                'chat': 220753323,
                'mail': 'yandex',
                'log': b'efolNrbncKXV7W2zBwPoxZH6nu2rQTuM0-GO1RZFZFKtBXlCwogZW8'
                       b'XKndb576hMenNXecSWUHCBMCa5gh41cVIqy-uwc0e_R3_Xm5zoLsQI'
                       b'pljy_SFNojwjADCLSNU75Q0tNmnND6U569Byj0TzkBibNbWuwxPam7'
                       b'sPQiwZncJnfOxqyszDOHWoevXzf5WBfp6uxbwXY6seEEl64cPj53LZ'
                       b'rgK4EkcrRkuINhzl8RTDtvt4RMdgwpyRau1bvzqAEMW8NbGsE0aTAF'
                       b'fm-pdDNDH8VizbtwZY5t4dUWLAfJeHf9RcWHT37dQSIviJqImQD-QV'
                       b'ulQN7BvyTNiRYdzkyA==',
                'pass': b'maHSWleb_MZvgaxBk6H1UNQet0fowTGMuBnxsxnl3IGFkfhWFFOuq'
                        b'bxWPFNB3XFkxV_YOwyXOlVhRZGweIoECb3253PZuuFOyFcscF4mwT'
                        b'Mw9vHUfN64-f-ogUzAAySKBnekk-lBEQ3TvfIepQK6uQkm0o00w0B'
                        b'POBXCnb0pfR_cgMpKRAzkNHEFPLRxQ9cUIK5l1RjXysPQuEYvLY_u'
                        b'dOzPouZFtrDplEVnrQRqHy-sadOUKM-CZnI-ODawSPNUEKp7rWxCR'
                        b'18qfVXicBWWw3QJO8bF2sUDX5Q1p23u-JDVz6hSEdqqDZbLzNHPgH'
                        b'vI62erOjPqDT30hzPk0-iFdQ=='
            }
        else:
            raise StopAsyncIteration


@pytest.mark.asyncio
async def test_find_by():
    mock_col = MagicMock()
    mock_col.find.return_value = Aiter()
    mongo = MongoClient()
    mongo.col = mock_col
    docs = await mongo.find_by(12)
    assert docs[0]['chat'] == 220753323
    assert docs[0]['mail'] == 'yandex'
    assert docs[0]['log'] == 'test@test.ru'
    assert docs[0]['pass'] == 'password'


@pytest.mark.asyncio
async def test_on_startup():
    mongo = MongoClient()
    with mock.patch(CREATE_INDEX, new=CoroutineMock()) as create_index:
        await mongo.on_startup()
        create_index.assert_called_once_with([('chat', pymongo.HASHED)])
        assert type(mongo.client) is AsyncIOMotorClient
        assert type(mongo.db) is AsyncIOMotorDatabase
        assert type(mongo.col) is AsyncIOMotorCollection
