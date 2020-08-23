# Author: Jingping.zhao
# Exception: 0x10 - 0x19

import os
import time

from app import database
from app import application
from framework.database import ClsTableLib
from framework.lib.program import SingletonType
from framework.exception import OrcFrameworkDatabaseException


class OrcTableIDGenerator(metaclass=SingletonType):
    """
    Generate a service ID and recode it in database
    """
    def __init__(self):
        self._cls = ClsTableLib.table("SysSequence")

    def _lock(self, p_flag: str) -> bool:
        """
        :type p_flag: object
        :return:
        """
        result = database.session \
            .query(self._cls) \
            .filter(self._cls.flag == p_flag) \
            .filter(self._cls.lock == False) \
            .update({"lock": True}, synchronize_session=False)
        database.session.commit()

        return result

    def _unlock(self, p_flag: str) -> bool:
        """
        :param p_flag:
        :return:
        """
        result = database.session \
            .query(self._cls) \
            .filter(self._cls.flag == p_flag) \
            .filter(self._cls.lock == True) \
            .update({"lock": False}, synchronize_session=False)
        database.session.commit()

        return result

    def get(self, p_flag: str) -> int:
        """
        :param p_flag:
        :return:
        """
        for i in range(10):
            if not self._lock(p_flag):
                time.sleep(1)
                continue

            sequence = database.session \
                .query(self._cls) \
                .filter(self._cls.flag == p_flag) \
                .first()

            if sequence is None:
                raise OrcFrameworkDatabaseException(0x01, "Create table id failed for flag: %s" % p_flag)

            sequence.sequence += 1
            database.session.commit()
            self._unlock(p_flag)

            return sequence.sequence
        else:
            raise OrcFrameworkDatabaseException(0x1, "Get service id failed.")

    @staticmethod
    def s_get(p_flag: str):
        instance = OrcTableIDGenerator()
        return instance.get(p_flag)


class OrcIdGenerator(metaclass=SingletonType):
    """
    id generator 41 + 17 + 5
    time_distance(9) +
    """

    def __init__(self):
        self._index = 0
        self._now = 0
        self._max_pid = 131072
        self._pid = None

    def set_pid(self, p_pid: int):
        """
        :param p_pid:
        :return:
        """
        self._pid = p_pid
        return self

    def get(self):
        """
        :return:
        """
        d1 = int(time.time() * 1000)
        d2 = self._pid or os.getpid()
        self._index = 0 if d1 != self._now else self._index + 1

        if d2 >= self._max_pid:
            raise OrcFrameworkDatabaseException(0x1, "Pid is too big, %s" % d2)

        if 32 == self._index:
            time.sleep(1)
            d1 = int(time.time() * 1000)
            self._index = 0

        self._now = d1

        return (d1 << 22) + (d2 << 5) + self._index

    @staticmethod
    def s_get(p_pid):
        """
        :return:
        """
        cls = OrcIdGenerator()
        return cls.set_pid(p_pid).get()
