from cryptography.fernet import Fernet
import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def genkey():
    return base64.urlsafe_b64encode(os.urandom(32))
def encrypt(data_to_encrypt_must_be_encoded, key):
    fernet = Fernet(key)
    return fernet.encrypt(data_to_encrypt_must_be_encoded)
def decrypt(data_to_decrypt, key):
    fernet = Fernet(key)
    encoded = fernet.decrypt(data_to_decrypt)
    return encoded.decode()
def encryptdecoded(data_to_encrypt, key):
    fernet = Fernet(key)
    encoded = data_to_encrypt.encode()
    return fernet.encrypt(encoded)
def genkeypassword(password, salt):
    passw = password.encode()
    kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
    backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(passw))
def saltgen():
    return os.urandom(16)
