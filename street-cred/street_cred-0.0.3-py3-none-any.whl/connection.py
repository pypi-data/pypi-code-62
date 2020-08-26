import os
import warnings

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

Base = declarative_base()

engine = None
Session = None


def _xconnection_str():
    locations = [
        'SQL_ALCHEMY_CONN',
        'STREET_CRED__SQL_ALCHEMY_CONN',
        'AIRFLOW__CORE__SQL_ALCHEMY_CONN',
    ]
    for var in locations:
        s = os.getenv(var)
        if s:
            return s
    warnings.warn('Could not find connection string in env vars.')
    return 'sqlite://'


def configure_orm():
    global engine
    global Session

    connection_str = _xconnection_str()
    engine_args = {}
    if 'sqlite' not in connection_str:
        # Engine args not supported by sqlite
        engine_args['pool_size'] = 5
        engine_args['pool_recycle'] = 1800

    engine = create_engine(connection_str, **engine_args)
    Session = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=engine)
    )


configure_orm()
