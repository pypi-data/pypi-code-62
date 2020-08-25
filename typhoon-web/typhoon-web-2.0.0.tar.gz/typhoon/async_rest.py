"""
typhoon.async_rest module
"""
# pylint: disable=missing-docstring, abstract-method, broad-except, invalid-name, protected-access

import datetime
import json
import logging
import random
import threading
from abc import ABC, abstractmethod
from functools import wraps
import sqlite3

from .rest import RestCallback, RestController, RestResult, route
from .status import CREATED, OK

logger = logging.getLogger(__name__)


class BaseJobManager(ABC):
    def __init__(self, node_name, token_slice_count):
        self.node_name = node_name
        self.token_slice_count = token_slice_count
        self.token_locks = [threading.Lock()] * self.token_slice_count
        self.token_idxs = [0] * self.token_slice_count

    @abstractmethod
    def init_job(self, token: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def finish_job(self, token: str, result) -> None:
        raise NotImplementedError()

    @abstractmethod
    def fail_job(self, token: str, msg: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def get_job_status(self, token: str) -> str:
        raise NotImplementedError()

    @abstractmethod
    def get_job_result(self, token: str) -> str:
        raise NotImplementedError()

    def generate_token(self) -> str:
        """
        generate token

        Returns
        -------
        str
            token
        """
        time_str = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3]
        idx = random.randint(0, self.token_slice_count - 1)
        lock = self.token_locks[idx]

        if lock.acquire(timeout=1):
            token = f'{time_str}_{self.node_name}_{idx:03d}{self.token_idxs[idx]:03d}'
            if self.token_idxs[idx] == self.token_slice_count - 1:
                self.token_idxs[idx] = 0
            else:
                self.token_idxs[idx] += 1
            lock.release()
        else:
            raise RuntimeError('token lock is blocked')
        return token


class SQLiteJobManager(BaseJobManager):

    CREATE = """
        CREATE TABLE IF NOT EXISTS `TB_JOB_STATUS`(
            `job_token` char(100) NOT NULL,
            `job_status` char(8) NOT NULL DEFAULT 'RUNNING',
            `job_result` text NOT NULL DEFAULT '',
            `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        """

    INSERT = "INSERT INTO TB_JOB_STATUS (`job_token`) VALUES ('%s')"

    UPDATE = "UPDATE TB_JOB_STATUS SET job_status='%s', job_result='%s' WHERE job_token='%s'"

    SELECT = "SELECT `job_status` FROM TB_JOB_STATUS WHERE job_token='%s'"

    SELECT_FULL = "SELECT `job_status`, `job_result` FROM TB_JOB_STATUS WHERE job_token='%s'"

    def __init__(self, node_name, token_slice_count, db):
        super().__init__(node_name=node_name, token_slice_count=token_slice_count)
        self.db = db
        self._execute(self.CREATE)

    def init_job(self, token: str) -> None:
        self._execute(self.INSERT % token)

    def finish_job(self, token: str, result) -> None:
        self._execute(self.UPDATE % ('FINISHED', json.dumps(result), token))

    def fail_job(self, token: str, msg: str) -> None:
        self._execute(self.UPDATE % ('FAILED', msg, token))

    def get_job_status(self, token: str) -> str:
        result = self._query(self.SELECT % token)
        assert len(result) == 1, f"invalid token: {token}"
        status = result[0]['job_status']
        return status

    def get_job_result(self, token: str) -> dict:
        result = self._query(self.SELECT_FULL % token)
        assert len(result) == 1, f"invalid token: {token}"

        status = result[0]['job_status']
        ret = {
            'token': token,
            'status': status
        }
        if status == 'RUNNING':
            return ret
        if status == 'FINISHED':
            return {
                **ret,
                'result': json.loads(result[0]['job_result'])
            }
        if status == 'FAILED':
            return {
                **ret,
                'error': result[0]['job_result']
            }
        raise RuntimeError('unknown status: %s' % status)

    def _get_connection(self):
        def dict_factory(cursor, row):
            d = {}
            for idx, col in enumerate(cursor.description):
                d[col[0]] = row[idx]
            return d
        connection = sqlite3.connect(self.db, isolation_level=None)
        connection.row_factory = dict_factory
        return connection

    def _execute(self, sql):
        logger.debug(sql)
        connection = self._get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(sql)
            return cursor.rowcount
        finally:
            connection.close()

    def _query(self, sql):
        logger.debug(sql)
        connection = self._get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            connection.close()


class AsyncRestController(RestController):
    def __init__(self, job_manager_class, **kwargs):
        super().__init__()
        self._job_manager = job_manager_class(**kwargs)

    @route(uri=r'/jobStatus', method='get')
    def get_job_status(self, token):
        result = self._job_manager.get_job_status(token=token)
        return RestResult(
            status=OK,
            content=result
        )

    @route(uri=r'/jobResult', method='get')
    def get_job_result(self, token):
        result = self._job_manager.get_job_result(token=token)
        return RestResult(
            status=OK,
            content=result
        )


def async_route(uri, method='get', auth_required=False, default_keep_alive=0):
    def decorator(func):
        func_name = func.__name__
        interface_name = f'_interface_{func_name}'

        def interface_body(self, *args, **kwargs):
            keep_alive = int(kwargs.pop('keep_alive', default_keep_alive))
            if keep_alive:
                result = func(self, *args, **kwargs)
                return RestResult(status=OK, content=result)
            token = self._job_manager.generate_token()
            return RestResult(
                status=CREATED,
                content=token,
                callback=RestCallback(
                    func_name=func_name,
                    args=args,
                    kwargs={**kwargs, 'token': token}
                )
            )
        interface_body.__name__ = interface_name
        interface_body = route(uri=uri, method=method, auth_required=auth_required)(interface_body)

        setattr(AsyncRestController, interface_name, interface_body)

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            token = kwargs.pop('token', None)
            if token:
                try:
                    self._job_manager.init_job(token)
                    result = func(self, *args, **kwargs)
                    self._job_manager.finish_job(token, result)
                except Exception as e:
                    self._job_manager.fail_job(token, e)
                    logger.error('job falied, token=%s', token, exc_info=True)
            else:
                return func(self, *args, **kwargs)
        return wrapper
    return decorator
