import base64
from ..config import PRIVATE_PATH, PUBLIC_PATH
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

pub_key = RSA.importKey(open(PUBLIC_PATH).read())
priv_key = RSA.importKey(open(PRIVATE_PATH).read())


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
