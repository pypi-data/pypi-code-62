from utilities import *
from vrmjobs import *
from datetime import datetime
from uuid import uuid4
import jsonpickle


def test_routine_checking_heartbeat(db_manager: 'TinyDbWrapper', interval: int):
    try:
        all_hostnames = db_manager.get_all_hostnames_by_type(HostType.WORKER)
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


def test_insert_hosts(db_manager: 'TinyDbWrapper', hostname: str, inet_addr: str,
                      ports: ['vrmjobs.PortInfo'], hosttype: 'vrmjobs.HostType'):
    try:
        host = HostInfo(hostname, inet_addr, ports, hosttype)
        result = db_manager.insert_host(host)
        if result:
            print("Insert {} to db successfully.".format(host))

    except InsertError as err:
        print(err)


def test_insert_queryinfo(db_manager: 'TinyDbWrapper'):
    node_disk_filter_info = FilterInfo('disk', [{'field_name': 'mountpoint', 'field_value': '/', 'regex': '='}])
    node_disk_io_filter_info = FilterInfo('disk_io',
                                          [{'field_name': 'device', 'field_value': '^.*sda.*$', 'regex': '=~'}])
    node_net_filter_info = FilterInfo('network_io', [{'field_name': 'device', 'field_value': '^wlp.*$', 'regex': '=~'}])

    cadvisor_cpu_filter_info = FilterInfo('cpu', [{'field_name': 'id', 'field_value': '/docker/.+', 'regex': '=~'}])
    cadvisor_mem_filter_info = FilterInfo('memory', [{'field_name': 'id', 'field_value': '/docker/.+', 'regex': '=~'}])
    cadvisor_disk_filter_info = FilterInfo('disk', [{'field_name': 'id', 'field_value': '/docker/.+', 'regex': '=~'}])
    cadvisor_disk_io_filter_info = FilterInfo('disk_io',
                                              [{'field_name': 'id', 'field_value': '/docker/.+', 'regex': '=~'}])
    cadvisor_network_io_filter_info = FilterInfo('network_io',
                                                 [{'field_name': 'id', 'field_value': '/docker/.+', 'regex': '=~'}])

    worker1_nodeexporter_query_ack = QueryAck(str(uuid4()),
                                              'worker1', 'nodeexporter',
                                              [node_disk_filter_info, node_disk_io_filter_info, node_net_filter_info],
                                              VrmType.QUERY_ACK)

    print('worker1_nodeexporter_query_ack: {} - length {}'.format(jsonpickle.encode(
        worker1_nodeexporter_query_ack),
        str(len(jsonpickle.encode(
            worker1_nodeexporter_query_ack)))))

    worker1_cadvisor_query_ack = QueryAck(str(uuid4()),
                                          'worker1', 'cadvisor',
                                          [cadvisor_cpu_filter_info, cadvisor_mem_filter_info,
                                           cadvisor_disk_filter_info, cadvisor_disk_io_filter_info,
                                           cadvisor_network_io_filter_info],
                                          VrmType.QUERY_ACK)

    print('worker1_cadvisor_query_ack: {} - length {} bytes'.format(jsonpickle.encode(
        worker1_cadvisor_query_ack),
        str(len(jsonpickle.encode(
            worker1_cadvisor_query_ack)))))

    # insert info from QueryAck packet to db
    result = db_manager.insert_queryinfo(worker1_nodeexporter_query_ack.hostname,
                                         worker1_nodeexporter_query_ack.job,
                                         worker1_nodeexporter_query_ack.filters)
    print("Insert worker1_nodeexporter_query_ack successfully") if result \
        else print("Insert worker1_nodeexporter_query_ack failed")

    result = db_manager.insert_queryinfo(worker1_cadvisor_query_ack.hostname,
                                         worker1_cadvisor_query_ack.job,
                                         worker1_cadvisor_query_ack.filters)

    print("Insert worker1_cadvisor_query_ack successfully") if result \
        else print("Insert worker1_cadvisor_query_ack failed")


def main():
    # create db
    db = TinyDbWrapper('test_db.json')
    cadvisor_disk_filter_info = FilterInfo('disk', [{'field_name': 'device', 'field_value': '^.*sda.*$', 'regex': '=~'}])
    cadvisor_disk_io_filter_info = FilterInfo('disk_io',
                                              [{'field_name': 'device', 'field_value': '^.*sda.*$', 'regex': '=~'}])
    cadvisor_network_io_filter_info = FilterInfo('network_io',
                                                 [{'field_name': 'interface', 'field_value': '^.*eth.*$', 'regex': '=~'}])

    # add some extra criteria
    worker1_cadvisor_new_queryack = QueryAck(str(uuid4()),
                                             'worker1', 'cadvisor',
                                             [cadvisor_disk_filter_info, cadvisor_disk_io_filter_info,
                                              cadvisor_network_io_filter_info],
                                             VrmType.QUERY_ACK)
    data = jsonpickle.encode(worker1_cadvisor_new_queryack)
    print('worker1_cadvisor_new_queryack: {} - length: {} bytes'.format(data, str(len(data))))
    result = db.insert_queryinfo(worker1_cadvisor_new_queryack.hostname,
                                 worker1_cadvisor_new_queryack.job,
                                 worker1_cadvisor_new_queryack.filters)

    # get worker1 filter category
    worker1_filter_categories = db.get_filter_category_by_hostname_job('worker1', 'cadvisor')
    for category in worker1_filter_categories:
        worker1_criteria = db.get_criteria_by_hostname_job_category('worker1', 'cadvisor', category)

        print('Cate: {} -> {}'.format(category, worker1_criteria))


if __name__ == '__main__':
    main()
