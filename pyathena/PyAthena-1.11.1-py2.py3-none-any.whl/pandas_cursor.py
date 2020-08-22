#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging

from pyathena.common import CursorIterator
from pyathena.cursor import BaseCursor
from pyathena.error import OperationalError, ProgrammingError
from pyathena.model import AthenaQueryExecution
from pyathena.result_set import AthenaPandasResultSet, WithResultSet
from pyathena.util import synchronized

_logger = logging.getLogger(__name__)


class PandasCursor(BaseCursor, CursorIterator, WithResultSet):
    def __init__(
        self,
        connection,
        s3_staging_dir,
        schema_name,
        work_group,
        poll_interval,
        encryption_option,
        kms_key,
        converter,
        formatter,
        retry_config,
        kill_on_interrupt=True,
        **kwargs
    ):
        super(PandasCursor, self).__init__(
            connection=connection,
            s3_staging_dir=s3_staging_dir,
            schema_name=schema_name,
            work_group=work_group,
            poll_interval=poll_interval,
            encryption_option=encryption_option,
            kms_key=kms_key,
            converter=converter,
            formatter=formatter,
            retry_config=retry_config,
            kill_on_interrupt=kill_on_interrupt,
            **kwargs
        )

    @property
    def rownumber(self):
        return self._result_set.rownumber if self._result_set else None

    def close(self):
        if self._result_set and not self._result_set.is_closed:
            self._result_set.close()

    @synchronized
    def execute(
        self,
        operation,
        parameters=None,
        work_group=None,
        s3_staging_dir=None,
        cache_size=0,
        keep_default_na=False,
        na_values=None,
        quoting=1,
    ):
        self._reset_state()
        self._query_id = self._execute(
            operation,
            parameters=parameters,
            work_group=work_group,
            s3_staging_dir=s3_staging_dir,
            cache_size=cache_size,
        )
        query_execution = self._poll(self._query_id)
        if query_execution.state == AthenaQueryExecution.STATE_SUCCEEDED:
            self._result_set = AthenaPandasResultSet(
                connection=self._connection,
                converter=self._converter,
                query_execution=query_execution,
                arraysize=self.arraysize,
                retry_config=self._retry_config,
                keep_default_na=keep_default_na,
                na_values=na_values,
                quoting=quoting,
            )
        else:
            raise OperationalError(query_execution.state_change_reason)
        return self

    def executemany(self, operation, seq_of_parameters):
        for parameters in seq_of_parameters:
            self.execute(operation, parameters)
        # Operations that have result sets are not allowed with executemany.
        self._reset_state()

    @synchronized
    def cancel(self):
        if not self._query_id:
            raise ProgrammingError("QueryExecutionId is none or empty.")
        self._cancel(self._query_id)

    @synchronized
    def fetchone(self):
        if not self.has_result_set:
            raise ProgrammingError("No result set.")
        return self._result_set.fetchone()

    @synchronized
    def fetchmany(self, size=None):
        if not self.has_result_set:
            raise ProgrammingError("No result set.")
        return self._result_set.fetchmany(size)

    @synchronized
    def fetchall(self):
        if not self.has_result_set:
            raise ProgrammingError("No result set.")
        return self._result_set.fetchall()

    @synchronized
    def as_pandas(self):
        if not self.has_result_set:
            raise ProgrammingError("No result set.")
        return self._result_set.as_pandas()
