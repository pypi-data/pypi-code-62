from tinydb import TinyDB, Query
from typing import List, Dict
from threading import RLock
from datetime import datetime
from .singleton import SingletonMeta
from .tinydb_exceptions import *
import vrmjobs


class TinyDbWrapper(metaclass=SingletonMeta):
    """
    Wrapper class for TinyDB within VRM system
    """

    def __init__(self, db_path: str) -> None:
        # create db
        self.db = TinyDB(db_path, sort_keys=True, indent=2, separators=(',', ': '))
        # create hosts table
        self.hosts = self.db.table('hosts')
        # create query table
        self.query_info = self.db.table('query_info')
        # create lock
        self.lock = RLock()
        # create timing-format
        self.time_format = '%H:%M:%S %d-%m-%Y'

    def insert_host(self, info: 'vrmjobs.HostInfo') -> bool:
        """
        Insert a new host into db
        :param info: an instance of HostInfo
        :return: True if success, False otherwise
        """
        with self.lock:
            try:
                host = self._check_host_existence(info.hostname)

                if not host:
                    ports = []
                    for p in info.ports:
                        ports.append({"daemon": p.daemon, "port": p.port})

                    self.hosts.insert({"hostname": info.hostname,
                                       "inet_addr": info.inet_addr,
                                       "ports": ports,
                                       "type": info.type.name,
                                       "latest_recv": datetime.now().strftime(self.time_format)})
                    return True
                return False
            except Exception as err:
                raise InsertError('Cannot insert new host {}'.format(str(info)), err)

    def _check_host_existence(self, hostname: str) -> bool:
        """
        Check whether a host with certain hostname is already included in the hosts table
        :param hostname: hostname of the host need to check
        :return: True if included, False otherwise
        """
        with self.lock:
            hosts = self.hosts.all()
            for host in hosts:
                if host['hostname'] == hostname:
                    return True
            return False

    def get_all_hostnames_by_type(self, host_type: 'vrmjobs.HostType') -> []:
        """
        Get all hostnames of a certain type
        :param host_type: type of host we want to filter
        :return: list of hostnames
        """
        hostnames = []
        with self.lock:
            try:
                hosts = self.hosts.all()

                if hosts:
                    for h in hosts:
                        if vrmjobs.HostType.__dict__[h['type']] == host_type:
                            hostnames.append(h['hostname'])
                return hostnames
            except Exception as err:
                raise GetError('Cannot find hostnames with type={}'.format(str(host_type)), err)

    def get_host_by_hostname(self, hostname: str) -> vrmjobs.HostInfo:
        """
        Get info of a host by its hostname
        :param hostname: hostname of a worker/controller/monitor
        :return: HostInfo instance
        """
        with self.lock:
            try:
                host = Query()
                record = self.hosts.search(host.hostname == hostname)

                if record:
                    port_infos = []
                    for info in record[0]["ports"]:
                        port_infos.append(vrmjobs.PortInfo(info["daemon"], info["port"]))

                    return vrmjobs.HostInfo(record[0]["hostname"],
                                            record[0]["inet_addr"],
                                            port_infos,
                                            # https://stackoverflow.com/questions/41407414/convert-string-to-enum-in-python
                                            vrmjobs.HostType.__dict__[record[0]["type"]])
                else:
                    raise Exception('Not found.')
            except Exception as err:
                raise GetError('Cannot find host by hostname={}'.format(hostname), err)

    def get_daemon_by_name(self, hostname: str, daemon: str) -> vrmjobs.PortInfo:
        """
        Get daemon information of a worker/collector/monitor by its hostname
        :param hostname: hostname of a host
        :param daemon: name of daemon
        :return: an instance of PortInfo
        """
        with self.lock:
            try:
                host = Query()
                record = self.hosts.search(host.hostname == hostname)[0]

                if not record:
                    return None

                for info in record["ports"]:
                    if info["daemon"] == daemon:
                        return vrmjobs.PortInfo(info["daemon"],
                                                info["port"])

                return None
            except Exception as err:
                raise GetError('Cannot get daemon name={} of host with hostname={}'.format(daemon, hostname), err)

    def update_host_metrics(self, hostname, metrics: List[Dict]) -> bool:
        """
        Update metrics information of a host with a certain hostname
        :param hostname: hostname of host
        :param metrics: list of PortInfo
        :return: True if succeed, False otherwise
        """
        with self.lock:
            try:
                host = Query()
                self.hosts.upsert({'metrics': metrics},
                                  host.hostname.matches(hostname))

                return True
            except Exception as err:
                raise UpdateError('Cannot update metrics: {} of host with hostname={}'.format(metrics, hostname), err)

    def update_host_heartbeat(self, hostname: str) -> bool:
        """
        Update latest_update information of a host with a certain hostname
        :param hostname: hostname of host
        :return: True if success, UpdateError otherwise
        """
        with self.lock:
            try:
                host = Query()
                self.hosts.update({'latest_recv': datetime.now().strftime(self.time_format)},
                                  host.hostname.matches(hostname))
                return True
            except Exception as err:
                raise UpdateError('Cannot update latest_recv of host with hostname={}'.format(hostname), err)

    def check_heartbeat(self, hostname: str, current_time, max_interval: int) -> bool:
        """
        Check whether latest_update information of a host with a certain hostname is overdue
        :param hostname: hostname of host
        :param current_time: time of the moment of checking
        :param max_interval: maximum seconds allowed between check
        :return:
        """
        with self.lock:
            try:
                host = Query()
                record = self.hosts.search(host.hostname == hostname)[0]

                if record:
                    latest_update = datetime.strptime(record['latest_recv'], self.time_format)
                    difference = current_time - latest_update

                    return int(difference.total_seconds()) <= max_interval

            except Exception as err:
                raise HeartbeatError('Cannot check heartbeat of host with hostname={}'.format(hostname), err)

    def insert_queryinfo(self, sys_type: str, job: str, info: List['vrmjobs.FilterInfo']) -> bool:
        """
        Insert a FilterInfo to db
        :param sys_type: type of the system (simulation/production)
        :param job: name of a prometheus job
        :param info: a list of instance of FilterInfo
        :return: True if success, False otherwise
        """
        with self.lock:
            try:
                type_query_info = self._check_info_existence(sys_type, job)

                # if type_query_info is not existed
                if not type_query_info:
                    filters = []
                    for item in info:
                        filters.append({'category': item.category, 'criteria': item.criteria})

                    self.query_info.insert({'type': sys_type,
                                            'job': job,
                                            'filters': filters})
                    return True
                # in case host_query_info, we add/update the category if needed
                else:
                    query = Query()
                    record = self.query_info.search(query.type == sys_type and query.job == job)
                    old_filters = record[0]['filters']
                    for item_info in info:
                        # if category of new FilterInfo (item_info) is already included in the database
                        if item_info.category in [d['category'] for d in old_filters]:
                            for item_filter in old_filters:
                                if item_info.category == item_filter['category']:
                                    # now we compare each criterion of item_info and item_filter
                                    for crit_info in item_info.criteria:
                                        # add without comparing field_name
                                        item_filter['criteria'].append(crit_info)
                                        # add with comparing field_name (unique check)
                                        # if crit_info['field_name'] not in [d['field_name'] for d in item_filter['criteria']]:
                                        #    item_filter['criteria'].append(crit_info)
                        # else, we add the whole new category and all of its criteria
                        else:
                            old_filters.append({'category': item_info.category, 'criteria': item_info.criteria})

                    self.query_info.update({'filters': old_filters},
                                           query.type.matches(sys_type) and query.job.matches(job))
                    return True

            except Exception as err:
                raise InsertError('Cannot insert FilterInfo of {}-{} to db'.format(sys_type, job), err)

    def _check_info_existence(self, sys_type: str, job: str) -> bool:
        """
        Check whether FilterInfo with certain type & job is already included in the query_info table
        :param sys_type: type of system (simulation/production)
        :param job: name of a prometheus job
        :return: True if included, False otherwise
        """
        with self.lock:
            infos = self.query_info.all()
            for info in infos:
                if info['type'] == sys_type and info['job'] == job:
                    return True
            return False

    def get_criteria_by_type_job_category(self, sys_type: str, job: str, category: str) -> List[Dict[str, str]]:
        """
        Get the list of FilterInfo of a worker using hostname, job, and category values
        :param sys_type: type of system (simulation/production)
        :param job: name of a prometheus job
        :param category: cpu/memory/disk/disk_io/network_io
        :return: List of vrmjobs.FilterInfo's criteria
        """
        with self.lock:
            query_infos = self.query_info.all()
            for info in query_infos:
                if info['type'] == sys_type and info['job'] == job:
                    for item in info['filters']:
                        if item['category'] == category:
                            return item['criteria']
            return []

    def get_categories_by_type_job(self, sys_type: str, job: str) -> List[str]:
        """
        Get the list of all category of FilterInfo of a worker using hostname and job values
        :param sys_type: type of system (simulation/production)
        :param job: name of a prometheus job of the worker
        :return: List of names of FilterInfo's categories
        """
        with self.lock:
            categories = []
            query_infos = self.query_info.all()
            for info in query_infos:
                if info['type'] == sys_type and info['job'] == job:
                    for item in info['filters']:
                        categories.append(item['category'])

            return categories

