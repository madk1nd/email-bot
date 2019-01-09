import base64
from Crypto import Random
from Crypto.Cipher import AES
from ..config import SECRET

iv = Random.new().read(AES.block_size)


def encode(message):
    obj = AES.new(SECRET, AES.MODE_CFB, iv)
    return base64.urlsafe_b64encode(obj.encrypt(message))


def decode(cipher):
    obj2 = AES.new(SECRET, AES.MODE_CFB, iv)
    return obj2.decrypt(base64.urlsafe_b64decode(cipher))
