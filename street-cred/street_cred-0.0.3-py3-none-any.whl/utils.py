import random

from .models import Credentials
from .connection import Session


def get_connections(conn_id):
    session = Session()
    db = (
        session.query(Credentials)
        .filter(Credentials.conn_id == conn_id)
        .all()
    )
    if not db:
        raise Exception("The conn_id `{0}` isn't defined".format(conn_id))
    session.expunge_all()
    session.close()
    return db


def get_credentials(key: str) -> Credentials:
    return random.choice(get_connections(key))
