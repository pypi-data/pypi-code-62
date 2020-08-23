# Author: Jingping.zhao
# Exception: 0x20 - 0x2F

import json
import traceback
from pymysql.err import MySQLError
from app import database
from app import application
from framework.lib.common import OrcDefaultDict
from framework.database import ClsTableLib
from framework.database.sequence import OrcTableIDGenerator
from framework.database.sequence import OrcIdGenerator
from framework.exception import OrcFrameworkDatabaseException
from sqlalchemy.exc import SQLAlchemyError


class OrcTable(object):
    """
    For table apps
    Exception: 0x20 - 0x28
    """
    _session = database.session

    def __init__(self, p_table):

        object.__init__(self)

        self._table = ClsTableLib.table(p_table)
        self._fields = self._table().to_dict().keys()

    def _param_boundary(self, p_data):
        """
        :param p_data:
        :return:
        """
        for _key, _value in self._table.extra.orc_length.items():
            if _key in p_data and _value < len(p_data[_key]):
                raise OrcFrameworkDatabaseException(0X10, "Field %s is too long, %s." % (_key, p_data))

    def _param_mandatory_exist(self, p_data):
        """
        :return:
        """
        for _key in self._table.extra.orc_mandatory:
            if _key not in p_data:
                raise OrcFrameworkDatabaseException(0X12, "Field %s is missing, %s." % (_key, p_data))

    def _param_mandatory_length(self, p_data):
        """
        :return:
        """
        for _key in self._table.extra.orc_mandatory:
            if _key in p_data and not p_data[_key]:
                raise OrcFrameworkDatabaseException(0X13, "Field %s can't be empty, %s." % (_key, p_data))

    def add(self, p_data):
        """
        新增
        :param p_data:
        :return:
        """
        application.logger.debug("Add item to table %s, data is %s." % (self._table.__tablename__, p_data))

        # Param check
        self._param_boundary(p_data)
        self._param_mandatory_exist(p_data)
        self._param_mandatory_length(p_data)

        # Add
        _data = OrcDefaultDict(p_data)
        _node = self._table()

        try:
            # Set data
            for _field in self._fields:
                _value = _data.value(_field)
                if isinstance(_value, list) or isinstance(_value, dict):
                    _value = json.dumps(_value)

                if 'id' == _field:
                    _node.id = OrcIdGenerator.s_get(OrcTableIDGenerator.s_get(_node.seq_flag))
                else:
                    setattr(_node, _field, _value)

            application.logger.debug("Add item %s" % _node)
            self._session.add(_node)
            self._session.commit()

        except (SQLAlchemyError, MySQLError):
            self._session.rollback()
            application.logger.error(traceback.format_exc())
            raise OrcFrameworkDatabaseException(0x01)

        return _node.to_dict()

    def delete(self, p_data):
        """
        :param p_data:
        :return:
        """
        application.logger.debug("Delete from table %s, id is %s." % (self._table.__tablename__, p_data))

        try:
            ids = p_data["id"]
            if isinstance(ids, list):
                for _id in ids:
                    self._delete(_id)
            else:
                self._delete(ids)
            return True

        except KeyError:
            application.logger.error(traceback.format_exc())
            raise OrcFrameworkDatabaseException(0x05)
        except (SQLAlchemyError, MySQLError):
            self._session.rollback()
            application.logger.error(traceback.format_exc())
            raise OrcFrameworkDatabaseException(0x06)

    def _delete(self, p_id):
        """
        删除
        :param p_id:
        :return:
        """
        self._session.query(self._table).filter(getattr(self._table, 'id') == p_id).delete()
        self._session.commit()

    def update(self, p_data):
        """
        更新
        :param p_data:
        :type p_data: dict
        :return:
        """
        application.logger.debug("Update table %s, condition is %s." % (self._table.__tablename__, p_data))

        # Param check
        self._param_boundary(p_data)
        self._param_mandatory_length(p_data)

        # Update
        try:
            for _key in p_data:
                if "id" == _key:
                    continue

                _item = self._session.query(self._table).filter(getattr(self._table, 'id') == p_data["id"])
                _item.update({_key: (None if "" == p_data[_key] else p_data[_key])})
            self._session.commit()
        except (SQLAlchemyError, MySQLError):
            self._session.rollback()
            application.logger.error(traceback.format_exc())
            raise OrcFrameworkDatabaseException(0x03)

        return True

    def query(self, p_cond):
        """
        查询
        :param p_cond:
        :return:
        """
        application.logger.debug("Query from table %s, condition is %s." % (self._table.__tablename__, p_cond))
        result = self._session.query(self._table)

        page = None if '__page__' not in p_cond else int(p_cond['__page__'])
        number = None if '__number__' not in p_cond else int(p_cond['__number__'])
        order = None if '__order__' not in p_cond else p_cond['__order__']

        for _key in p_cond:
            if _key not in self._fields:
                continue

            try:
                result = self._filter(result, _key, p_cond[_key])
            except KeyError:
                application.logger.error(traceback.format_exc())
                raise OrcFrameworkDatabaseException(0x04)
            except SQLAlchemyError:
                application.logger.error(traceback.format_exc())
                raise OrcFrameworkDatabaseException(0x04)

        if order is not None:
            assert isinstance(order, dict)
            result = result.order_by(*tuple([getattr(getattr(self._table, _field), _mode)()
                                             for _field, _mode in order.items()]))

        try:
            if (page is not None) and (number is not None):
                record_num = result.count()
                result = result.offset((page - 1) * number).limit(number)
                return dict(__number__=record_num, data=[item.to_dict() for item in result.all()])
            else:
                return [item.to_dict() for item in result.all()]
        except (SQLAlchemyError, MySQLError):
            application.logger.error(traceback.format_exc())
            raise OrcFrameworkDatabaseException(0x04, "Query failed, condition is: %s" % p_cond)

    def _filter(self, p_res, p_key, p_value):
        """
        Search method
        :param p_key: field name
        :type p_key: str
        :param p_value: search value
            str: value
            list: (mode, value)
            mode: 'in', like, eq(default)
        :return:
        """
        _mode = 'eq'
        _value = p_value

        try:
            _temp = json.loads(_value) if isinstance(_value, str) else _value

            if isinstance(_temp, (list, tuple)):
                _mode = _temp[0]
                _value = _temp[1]

        except (ValueError, TypeError):
            pass

        if 'eq' == _mode:
            return p_res.filter(getattr(self._table, p_key) == _value)

        elif 'in' == _mode:
            return p_res.filter(getattr(getattr(self._table, p_key), 'in_')(_value))

        elif 'like' == _mode:
            return p_res.filter(getattr(getattr(self._table, p_key), 'like')(_value))

        else:
            return p_res


class OrcOrderTable(OrcTable):
    """
    Table with order
    """
    def __init__(self, p_table):
        OrcTable.__init__(self, p_table)

        self._key = []
        self._order = self._table.extra.orc_order

        if not self._order:
            raise OrcFrameworkDatabaseException(0X01, "Order table info orc_key or orc_order is missing for table %s."
                                                % getattr(self._table, "__tablename__"))

    def _order_cond(self, p_data):
        """
        :param p_data:
        :return:
        """
        return {_key: p_data[_key] for _key in self._table.extra.orc_keys if _key in p_data}

    def add(self, p_data):
        """
        Calculate order
        :param p_data:
        :return:
        """
        cond = self._order_cond(p_data)
        p_data[self._order] = len(super(OrcOrderTable, self).query(cond)) + 1
        return super(OrcOrderTable, self).add(p_data)

    def delete(self, p_data):
        """
        Reorder
        :param p_data:
        :return:
        """
        try:
            _ids = p_data["id"] if isinstance(p_data["id"], list) else [p_data["id"]]
        except KeyError:
            raise OrcFrameworkDatabaseException(0x1, "No id found in delete command.")

        data = super(OrcOrderTable, self).query({"id": ("in", _ids)})
        result = super(OrcOrderTable, self).delete(p_data)
        # Todo 需要优化
        if result:
            for _data in data:
                self._reorder(_data)

        return True

    def _reorder(self, p_cond: dict):
        """
        :param p_cond: flag/pid removed order
        :return:
        """
        next_cond = p_cond.copy()
        next_cond[self._order] += 1
        next_item = self.query(p_cond)
        if next_item:
            self._change_order(next_item[0].id, p_cond[self._order])
            self._reorder(next_item[0].to_dict())

    def update(self, p_data):
        """
        Remove order
        :param p_data:
        :return:
        """
        if self._order in p_data:
            del p_data[self._order]

        return super(OrcOrderTable, self).update(p_data)

    def up(self, p_data):
        """
        :param p_data:
        :return:
        """
        cur_item = self.query(p_data)

        # More than 1 item to be up.
        if 1 != len(cur_item):
            return False
        cur_item = cur_item[0]
        assert isinstance(cur_item, dict)

        # Previous item
        cond = self._order_cond(cur_item)
        cond[self._order] = cur_item[self._order] - 1
        pre_item = self.query(cond)
        if 1 != len(pre_item):
            return True
        pre_item = pre_item[0]
        assert isinstance(pre_item, dict)

        self._change_order(pre_item["id"], cur_item[self._order])
        self._change_order(cur_item["id"], pre_item[self._order])

    def down(self, p_data):
        """
        :param p_data:
        :return:
        """
        cur_item = self.query(p_data)

        # More than 1 item to be up.
        if 1 != len(cur_item):
            return False
        cur_item = cur_item[0]
        assert isinstance(cur_item, dict)

        # Next item
        cond = self._order_cond(cur_item)
        cond[self._order] = cur_item[self._order] + 1
        next_item = self.query(cond)
        if 1 != len(next_item):
            return True
        next_item = next_item[0]
        assert isinstance(next_item, dict)

        self._change_order(next_item["id"], cur_item[self._order])
        self._change_order(cur_item["id"], next_item[self._order])

    def _change_order(self, p_id, p_order):
        """
        :param p_id:
        :param p_order:
        :return:
        """
        super(OrcOrderTable, self).update({"id": p_id, self._order: p_order})
