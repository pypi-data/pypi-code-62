from typing import List, Tuple, Optional

from distributed import Client
from distributed.scheduler import WorkerState

from mason_dask.utils.worker_spec import WorkerSpec

class ClusterSpec:
    
    def __init__(self, client: Client):
        self.worker_specs: List[WorkerSpec] = []
        if client.cluster and client.cluster.scheduler:
            workers_dict: dict = client.cluster.scheduler.workers
            workers: List[WorkerState] = list({k: workers_dict[k] for k in workers_dict.keys() if isinstance(workers_dict[k], WorkerState)}.values())
            worker_specs: List[Tuple[int, int]] = list(map(lambda w: (w.memory_limit, w.ncores), workers))
            self.worker_specs = list(map(lambda s: WorkerSpec(*s), worker_specs))
        
    def max_partition_size(self) -> int:
        return min(list(map(lambda s: s.memory, self.worker_specs)))
    
    def num_workers(self) -> Optional[int]:
        if len(self.worker_specs) > 0:
            return len(self.worker_specs)
    
