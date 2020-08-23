from dataclasses import dataclass


@dataclass
class Consts:
    connections_key: str
    connection_heartbeat_template: str
    connection_queues_template: str
    connection_consumers_template: str
    connection_queue_consumers_template: str
    connection_queue_unacked_template: str
    queues_key: str
    queue_ready_template: str
    queue_rejected_template: str
    queue_connections_template: str
    default_batch_timeout: int
    purge_batch_size: int


consts_list = Consts(**{
    'connections_key':                     'rmq::connections',
    'connection_heartbeat_template':       'rmq::connection::{connection}::heartbeat',
    'connection_queues_template':          'rmq::connection::{connection}::queues',
    'connection_consumers_template':       'rmq::connection::{connection}::consumers',
    'connection_queue_consumers_template': 'rmq::connection::{connection}::queue::[{queue}]::consumers',
    'connection_queue_unacked_template':   'rmq::connection::{connection}::queue::[{queue}]::unacked',

    'queues_key':                          'rmq::queues',
    'queue_ready_template':                'rmq::queue::[{queue}]::ready',
    'queue_rejected_template':             'rmq::queue::[{queue}]::rejected',
    'queue_connections_template':          'rmq::queue::[{queue}]::connections',

    'default_batch_timeout':               1000,
    'purge_batch_size':                    100
})
