from utilities import *
import vrmjobs
from datetime import datetime
from uuid import uuid4

def test_routine_checking_heartbeat(db_manager: 'TinyDbWrapper', interval: int):
    try:
        all_hostnames = db_manager.get_all_hostnames_by_type(vrmjobs.HostType.WORKER)
        disconnected_hosts = []
        now = datetime.now()
        for hostname in all_hostnames:
            if not db_manager.check_heartbeat(hostname, now, interval):
                disconnected_hosts.append(hostname)

        print(disconnected_hosts)
    except HeartbeatError or GetError as err:
        print(err)


def test_check_heartbeat(db_manager: 'TinyDbWrapper', hostname: str, interval: int):
    try:
        result = db_manager.check_heartbeat(hostname, datetime.now(), interval)

        if result:
            print("Still good.")
        else:
            print("Need to update.")
    except HeartbeatError as err:
        print(err)


def test_update_heartbeat(db_manager: 'TinyDbWrapper', hostname: str):
    try:
        db_manager.update_host_heartbeat(hostname)
        host = db_manager.get_host_by_hostname(hostname)
        print("Latest info: {}".format(host))
    except UpdateError as err:
        print(err)


def test_get_host(db_manager: 'TinyDbWrapper', hostname: str):
    try:
        host = db_manager.get_host_by_hostname(hostname)
        print(host)
    except GetError as err:
        print(err)


def test_insert_hosts(db_manager: 'TinyDbWrapper', hostname: str, inet_addr:str,
                      ports: ['vrmjobs.PortInfo'], hosttype: 'vrmjobs.HostType'):
    try:
        host = vrmjobs.HostInfo(hostname, inet_addr, ports, hosttype)
        result = db_manager.insert_host(host)
        if result:
            print("Insert {} to db successfully.".format(host))

    except InsertError as err:
        print(err)


def main():
    # create db
    db = TinyDbWrapper('test_db.json')

    # test host_query_info's functions
    worker1_cadvisor_diskio_criteria = db.get_criteria_by_hostname_job_category('worker1',
                                                                                'cadvisor',
                                                                                'disk-io')

    print(worker1_cadvisor_diskio_criteria)

    worker1_node_disk_criteria = db.get_criteria_by_hostname_job_category('worker1',
                                                                          'node',
                                                                          'disk')

    print(worker1_node_disk_criteria)


if __name__ == '__main__':
    main()
