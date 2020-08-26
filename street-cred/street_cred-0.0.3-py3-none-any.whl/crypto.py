import os

from cryptography.fernet import Fernet, MultiFernet

_fernet = None  # type: Optional[FernetProtocol]


def _xfernet_key():
    locations = ['FERNET_KEY',
                 'STREET_CRED__FERNET_KEY',
                 'AIRFLOW__CORE__FERNET_KEY']
    for var in locations:
        s = os.getenv(var)
        if s:
            return s
    return ''


def get_fernet():
    """Get fernet encrypter."""
    global _fernet

    if _fernet:
        return _fernet

    fernet_key = _xfernet_key()
    if fernet_key:
        _fernet = MultiFernet([
            Fernet(fernet_part.encode('utf-8'))
            for fernet_part in fernet_key.split(',')
        ])
    return _fernet
