# Author: Jingping.zhao
# Exception: 0x30 - 0x39

import traceback
from app import application
from framework.exception import OrcFrameworkDatabaseException
from framework.database.table import OrcTable

# Add: pid 没有表示顶层节点
# Delete: 同时删除所有子节点
# Update:
# Query: all 所有
#        parents 路径 -> {id}
#        children 子树 -> {id}
#        sub 只查一级，带 pid, 无 pid 表示第一层


class OrcTree(OrcTable):
    """
    For tree apps
    """
    def __init__(self, p_table):
        OrcTable.__init__(self, p_table)

        self._query_type = ["parents", "children", "sub"]

    def delete(self, p_data):
        """
        :param p_data:
        :return:
        """
        for _id in p_data["id"]:
            self.delete({"id": [item["id"] for item in
                                super(OrcTree, self).query({"pid": _id})]})
        super(OrcTree, self).delete(p_data)

    def query(self, p_data):
        """
        :param p_data:
        :return:
        """
        if "__type__" not in p_data:
            return self.query_all(p_data)

        if p_data["__type__"] in self._query_type:
            func = getattr(self, "query_%s" % p_data["__type__"], None)
            return func(p_data) if func is not None else []

    def query_all(self, p_data):
        """
        :param p_data:
        :return:
        """
        return super(OrcTree, self).query(p_data)

    def query_parents(self, p_data):
        """
        :param p_data:
        :return:
        :rtype: list
        """
        current = super(OrcTree, self).query({"id": p_data["id"]})
        if not current:
            return []

        current = current[0]
        if current["pid"] is None:
            return [current]

        parents = self.query_parents({"id": current["pid"]})
        parents.append(current)

        return parents

    def query_children(self, p_data):
        """
        :param p_data:
        :return:
        """
        current = super(OrcTree, self).query({"id": p_data["id"]})
        for _c in current:
            current.extend(self._children({"id": _c["id"]}))
        return current

    def _children(self, p_data):
        """
        :param p_data:
        :return:
        """
        result = []
        children = self.query_sub(p_data)
        for _child in children:
            result.append(_child)
            result.extend(self._children(_child))
        return children

    def query_sub(self, p_data):
        """
        :param p_data:
        :return:
        """
        try:
            return super(OrcTree, self).query({"pid": p_data["id"]})
        except KeyError:
            application.logger.info(traceback.format_exc())
            application.logger.info("Query failed, condition is %s" % p_data)
            raise OrcFrameworkDatabaseException(0x01, "Query failed")


class OrcOrderTree(OrcTree):
    """
    Tree with order
    """
    def __init__(self, p_table):
        OrcTree.__init__(self, p_table)
        # Todo

    def up(self, p_data):
        """
        :param p_data:
        :type p_data: dict
        :return:
        """
        current = self.query(p_data)
        if not current or 1 != len(current):
            return False

        current = current[0]
        if 0 == current["order"]:
            return True

        pre_obj = self.query({"flag": current["flag"], "order": current["order"] - 1})[0]

        self.update({"id": pre_obj["id"], "order": current["order"]})
        self.update({"id": current["id"], "order": pre_obj["order"]})

        return True

    def down(self, p_data):
        """
        :param p_data:
        :type p_data: dict
        :return:
        """
        current = self.query(p_data)
        if not current or 1 != len(current):
            return False

        current = current[0]

        next_obj = self.query({"flag": current["flag"], "order": current["order"] + 1})
        if not next_obj:
            return True

        self.update({"id": next_obj["id"], "order": current["order"]})
        self.update({"id": current["id"], "order": next_obj["order"]})

        return True


class OrcUniqueTree(OrcTree):
    """
    同层元素 flag 不可重复，可通过 path 查询
    """
    def __init__(self, p_table):
        OrcTree.__init__(self, p_table)

        self._query_type.extend(["path", "by_path"])
        self._unique = ""
        try:
            self._unique = self._table.extra.orc_unique
        except AttributeError:
            raise OrcFrameworkDatabaseException(0X01, "Unique tree info orc_unique is missing in table %s."
                                                % getattr(self._table, "__tablename__"))

    def add(self, p_data):
        """
        :param p_data:
        :return:
        """
        try:
            _pid = None if ("pid" not in p_data or not p_data["pid"]) else p_data["pid"]
            p_data["pid"] = _pid

            result = super(OrcUniqueTree, self).query({"pid": _pid, self._unique: p_data[self._unique]})
            if result:
                raise OrcFrameworkDatabaseException(0x00, "Flag %s is already exist" % p_data[self._unique])

            return super(OrcUniqueTree, self).add(p_data)
        except KeyError:
            application.logger.info(traceback.format_exc())
            raise OrcFrameworkDatabaseException(0x00, "Data %s is wrong, flag is essential." % p_data)

    def update(self, p_data):
        """
        :param p_data:
        :return:
        """
        item = super(OrcUniqueTree, self).query({"id": p_data["id"]})
        if not item:
            raise OrcFrameworkDatabaseException(0x00, "Item %s is not found." % p_data["id"])

        item = item[0]
        result = super(OrcUniqueTree, self).query({"pid": item["pid"], self._unique: p_data[self._unique]})

        if result:
            raise OrcFrameworkDatabaseException(0x00, "Flag %s is duplicated." % p_data[self._unique])

        return super(OrcUniqueTree, self).update(p_data)

    def query_by_path(self, p_data):
        """
        :param p_data:
        :return:
        """
        try:
            pid = None
            item = {}
            for _flag in p_data["path"].split("."):
                item = super(OrcUniqueTree, self).query({"pid": pid, self._unique: _flag})

                if not item:
                    application.logger.info(traceback.format_exc())
                    raise OrcFrameworkDatabaseException(0x00, "Flag %s is not found under %s." % (_flag, pid))
                pid = item[0]["id"]

            return item
        except KeyError:
            application.logger.info(traceback.format_exc())
            application.logger.info("Path %s is not found" % p_data)
            return None

    def query_path(self, p_data):
        """
        :param p_data:
        :return:
        """
        result = self.query_parents(p_data)
        return ['.'.join([item[self._unique] for item in result])]
