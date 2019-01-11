import base64
from ..config import ENC_KEY, ENC_PUB
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

pub_key = RSA.importKey(open(ENC_PUB).read())
priv_key = RSA.importKey(open(ENC_KEY).read())


def encode(message):
    cipher = PKCS1_OAEP.new(pub_key)
    return base64.urlsafe_b64encode(
        cipher.encrypt(message.encode('utf-8'))
    )


def decode(text):
    cipher = PKCS1_OAEP.new(priv_key)
    return cipher.decrypt(
        base64.urlsafe_b64decode(text)
    ).decode('utf-8')
