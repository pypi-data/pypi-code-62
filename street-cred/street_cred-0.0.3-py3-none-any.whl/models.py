import json
from urllib.parse import parse_qsl, quote, unquote, urlencode, urlparse

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import synonym

from .connection import Base
from .crypto import get_fernet


# Python automatically converts all letters to lowercase in hostname
# See: https://issues.apache.org/jira/browse/AIRFLOW-3615
def parse_netloc_to_hostname(uri_parts):
    hostname = unquote(uri_parts.hostname or '')
    if '/' in hostname:
        hostname = uri_parts.netloc
        if "@" in hostname:
            hostname = hostname.rsplit("@", 1)[1]
        if ":" in hostname:
            hostname = hostname.split(":", 1)[0]
        hostname = unquote(hostname)
    return hostname


class Credentials(Base):
    """Stores information about various credentials.

    This is largely inspired/stolen from the connections table used
    by airflow. This also tries to maintain compatibility with that model
    so that this package can be used by applications to read the airflow
    connections table without having to install the entire airflow
    package.
    """
    __tablename__ = 'connection'

    id = Column(Integer(), primary_key=True)
    conn_id = Column(String(250))
    conn_type = Column(String(500))
    host = Column(String(500))
    schema = Column(String(500))
    login = Column(String(500))
    _password = Column('password', String(5000))
    port = Column(Integer())
    is_encrypted = Column(Boolean, unique=False, default=False)
    is_extra_encrypted = Column(Boolean, unique=False, default=False)
    _extra = Column('extra', String(5000))

    def __init__(
            self, conn_id=None, conn_type=None,
            host=None, login=None, password=None,
            schema=None, port=None, extra=None,
            uri=None):
        self.conn_id = conn_id
        if uri:
            self.parse_from_uri(uri)
        else:
            self.conn_type = conn_type
            self.host = host
            self.login = login
            self.password = password
            self.schema = schema
            self.port = port
            self.extra = extra

    def __repr__(self) -> None:
        return self.conn_id

    def parse_from_uri(self, uri):
        uri_parts = urlparse(uri)
        conn_type = uri_parts.scheme
        if conn_type == 'postgresql':
            conn_type = 'postgres'
        elif '-' in conn_type:
            conn_type = conn_type.replace('-', '_')
        self.conn_type = conn_type
        self.host = parse_netloc_to_hostname(uri_parts)
        quoted_schema = uri_parts.path[1:]
        self.schema = unquote(quoted_schema) if quoted_schema else quoted_schema
        self.login = unquote(uri_parts.username) \
            if uri_parts.username else uri_parts.username
        self.password = unquote(uri_parts.password) \
            if uri_parts.password else uri_parts.password
        self.port = uri_parts.port
        if uri_parts.query:
            self.extra = json.dumps(dict(parse_qsl(uri_parts.query, keep_blank_values=True)))

    def get_uri(self) -> str:
        uri = '{}://'.format(str(self.conn_type).lower().replace('_', '-'))

        authority_block = ''
        if self.login is not None:
            authority_block += quote(self.login, safe='')

        if self.password is not None:
            authority_block += ':' + quote(self.password, safe='')

        if authority_block > '':
            authority_block += '@'

            uri += authority_block

        host_block = ''
        if self.host:
            host_block += quote(self.host, safe='')

        if self.port:
            if host_block > '':
                host_block += ':{}'.format(self.port)
            else:
                host_block += '@:{}'.format(self.port)

        if self.schema:
            host_block += '/{}'.format(quote(self.schema, safe=''))

        uri += host_block

        if self.extra_dejson:
            uri += '?{}'.format(urlencode(self.extra_dejson))

        return uri

    def get_password(self):
        if self._password and self.is_encrypted:
            fernet = get_fernet()
            return fernet.decrypt(bytes(self._password, 'utf-8')).decode()
        return self._password

    def set_password(self, value):
        fernet = get_fernet()
        if fernet:
            value = fernet.encrypt(bytes(value, 'utf-8')).decode()
        self._password = value
        self.is_encrypted = bool(fernet)

    @declared_attr
    def password(cls):
        return synonym('_password',
                       descriptor=property(cls.get_password, cls.set_password))

    def get_extra(self):
        if self._extra and self.is_extra_encrypted:
            fernet = get_fernet()
            return fernet.decrypt(bytes(self._extra, 'utf-8')).decode()
        return self._extra

    def set_extra(self, value):
        fernet = get_fernet()
        if fernet:
            value = fernet.encrypt(bytes(value, 'utf-8')).decode()
        self._extra = value
        self.is_extra_encrypted = bool(fernet)

    @declared_attr
    def extra(cls):
        return synonym('_extra',
                       descriptor=property(cls.get_extra, cls.set_extra))

    def rotate_fernet_key(self):
        fernet = get_fernet()
        if self._password and self.is_encrypted:
            self._password = fernet.rotate(self._password.encode('utf-8')).decode()
        if self._extra and self.is_extra_encrypted:
            self._extra = fernet.rotate(self._extra.encode('utf-8')).decode()

    @property
    def extra_dejson(self):
        """Returns the extra property by deserializing json."""
        if self.extra:
            return json.loads(self.extra)
        return {}
