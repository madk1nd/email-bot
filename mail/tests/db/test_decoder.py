from api.db.decoder import decode, encode


def test_encoding():
    value = encode('test')
    result = decode(value)
    assert result == 'test'
