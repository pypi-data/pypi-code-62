import hashlib
from .security_exception import SecurityException


def blake2b(plaintext):
    try:
        return hashlib.blake2b(plaintext.encode()).hexdigest()
    except Exception as e:
        raise SecurityException(str(e))


def blake2s(plaintext):
    try:
        return hashlib.blake2s(plaintext.encode()).hexdigest()
    except Exception as e:
        raise SecurityException(str(e))


def md5_hash(plaintext):
    try:
        return hashlib.md5(plaintext.encode()).hexdigest()
    except Exception as e:
        raise SecurityException(str(e))


def sha1_hash(plaintext):
    try:
        return hashlib.sha1(plaintext.encode()).hexdigest()
    except Exception as e:
        raise SecurityException(str(e))


def sha256_hash(plaintext):
    try:
        return hashlib.sha256(plaintext.encode()).hexdigest()
    except Exception as e:
        raise SecurityException(str(e))


def sha512_hash(plaintext):
    try:
        return hashlib.sha512(plaintext.encode()).hexdigest()
    except Exception as e:
        raise SecurityException(str(e))