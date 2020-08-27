# Copyright (c) 2020 Watsen Networks.  All Rights Reserved.

_G=':memory:'
_F='mysql'
_E='postgresql'
_D=True
_C='sqlite'
_B='postgres'
_A=None
import os
from copy import copy
import sqlalchemy as sa
from sqlalchemy.engine.url import make_url
from sqlalchemy.exc import OperationalError,ProgrammingError
def database_exists(url,connect_args=_A):
	I=False;E=connect_args;B=url
	def F(engine,sql):A=engine;B=A.execute(sql);C=B.scalar();B.close();A.dispose();return C
	def G(database):
		A=database
		if not os.path.isfile(A)or os.path.getsize(A)<100:return I
		with open(A,'rb')as B:C=B.read(100)
		return C[:16]==b'SQLite format 3\x00'
	B=copy(make_url(B));C=B.database
	if B.drivername.startswith(_B):B.database=_B
	else:B.database=_A
	A=sa.create_engine(B,connect_args=E)
	if A.dialect.name==_E:D="SELECT 1 FROM pg_database WHERE datname='%s'"%C;return bool(F(A,D))
	elif A.dialect.name==_F:D="SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = '%s'"%C;return bool(F(A,D))
	elif A.dialect.name==_C:
		if C:return C==_G or G(C)
		else:return _D
	else:
		A.dispose();A=_A;D='SELECT 1'
		try:B.database=C;A=sa.create_engine(B,connect_args=E);H=A.execute(D);H.close();return _D
		except (ProgrammingError,OperationalError):return I
		finally:
			if A is not _A:A.dispose()
def create_database(url,encoding='utf8',template=_A,connect_args=_A):
	I=encoding;G=template;F=connect_args;B=url;B=copy(make_url(B));C=B.database
	if B.drivername.startswith(_B):B.database=_B
	elif B.drivername.startswith('mssql'):B.database='master'
	elif not B.drivername.startswith(_C):B.database=_A
	if B.drivername=='mssql+pyodbc':
		if F is not _A:H=copy(F)
		else:H={}
		H['autocommit']=_D;A=sa.create_engine(B,connect_args=H)
	elif B.drivername=='postgresql+pg8000':A=sa.create_engine(B,isolation_level='AUTOCOMMIT',connect_args=F)
	else:A=sa.create_engine(B,connect_args=F)
	D=_A
	if A.dialect.name==_E:
		if A.driver=='psycopg2':from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT as J;A.raw_connection().set_isolation_level(J)
		if not G:G='template1'
		E="CREATE DATABASE {0} ENCODING '{1}' TEMPLATE {2}".format(quote(A,C),I,quote(A,G));D=A.execute(E)
	elif A.dialect.name==_F:E="CREATE DATABASE {0} CHARACTER SET = '{1}'".format(quote(A,C),I);D=A.execute(E)
	elif A.dialect.name==_C and C!=_G:
		if C:A.execute('CREATE TABLE DB(id int);');A.execute('DROP TABLE DB;')
	else:E='CREATE DATABASE {0}'.format(quote(A,C));D=A.execute(E)
	if D is not _A:D.close()
	A.dispose()
from sqlalchemy.orm.session import object_session
from sqlalchemy.engine.interfaces import Dialect
from sqlalchemy.orm.exc import UnmappedInstanceError
def quote(mixed,ident):
	A=mixed
	if isinstance(A,Dialect):B=A
	else:B=get_bind(A).dialect
	return B.preparer(B).quote(ident)
def get_bind(obj):
	A=obj
	if hasattr(A,'bind'):B=A.bind
	else:
		try:B=object_session(A).bind
		except UnmappedInstanceError:B=A
	if not hasattr(B,'execute'):raise TypeError('This method accepts only Session, Engine, Connection and declarative model objects.')
	return B