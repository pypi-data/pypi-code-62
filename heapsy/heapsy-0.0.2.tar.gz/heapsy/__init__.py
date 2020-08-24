import gc
import sys
from collections import defaultdict


MAX_DEPTH = 5
MAX_ITEMS = 10000
DEFAULT_IGNORE_TYPES = ['HeapList', 'HeapNode', 'HeapDendrogram']
IGNORE_TYPES = []
IGNORE_MODULES = ['builtins']


TOTAL_HEAP_SIZE_METRIC_HELPS = [
    '# HELP heap_size_bytes_total application total heap usage bytes',
    '# TYPE heap_size_bytes_total gauge'
]

OBJ_COUNT_METRIC_HELPS = [
    '# HELP object_count application module object count',
    '# TYPE object_count gauge'
]

HEAP_SIZE_METRIC_HELPS = [
    '# HELP heap_size_bytes application module object heap size bytes',
    '# TYPE heap_size_bytes gauge'
]


class HeapList(list):
    pass


class HeapNode(object):
    name = None
    size = None
    referrers = None
    children = None

    def __init__(self, name, size=0, referrers=[]):
        self.name = name
        self.size = size
        self.referrers = referrers if referrers else HeapList()
        self.children = HeapList()

    @staticmethod
    def decendants(node, depth=0):
        for obj in node.children:
            yield obj
            yield from HeapNode.decendants(obj, depth + 1)


class HeapDendrogram(object):
    root = None
    _footprints = None
    _max_depth = None
    _max_items = None

    def __init__(self, max_depth=MAX_DEPTH, max_items=MAX_ITEMS,
                 ignore_types=IGNORE_TYPES, ignore_modules=IGNORE_MODULES):
        self._max_depth = max_depth
        self._max_items = max_items
        self.ignore_types = set(DEFAULT_IGNORE_TYPES + ignore_types)
        self.ignore_modules = set(ignore_modules)

    def generate(self):
        gc.collect()

        self._footprints = set()
        objects = [
            obj for obj in gc.get_objects()
            if not self._ignorable(obj)
        ]
        self.root = HeapNode('root', 0, objects)
        self.step(self.root)

    def _ignorable(self, obj, referents=None):
        ignorable = any((
            # cyclic reference check
            id(obj) in self._footprints,

            # obj is not ignore_types
            obj.__class__.__name__ in self.ignore_types,

            # obj's module is not in ignore_modules
            type(obj).__module__ in self.ignore_modules,

            # obj's referents is in the ignore_types
            self.ignore_types.intersection((
                r.__class__.__name__ for r in referents
            )) if referents else False
        ))

        return ignorable

    def _stoppable(self, depth):
        return any((
            depth > self._max_depth,
            len(self._footprints) > self._max_items
        ))

    def step(self, node, depth=0):
        if self._stoppable(depth):
            return

        for obj in node.referrers:
            referents = set((type(r) for r in gc.get_referents(obj)))

            if self._ignorable(obj, referents):
                continue

            self._footprints.add(id(obj))

            obj_type = type(obj)
            name = (
                f'{obj_type.__module__}'
                f'.{obj_type.__name__}'
                f'@{id(obj)}'
            )

            size = sys.getsizeof(obj_type)
            referrers = [
                o for o in gc.get_referrers(obj)
                if not self._ignorable(o)
            ]

            nextnode = HeapNode(name, size, referrers)
            node.children.append(nextnode)

            if self._stoppable(depth + 1):
                return

            self.step(nextnode, depth + 1)

        return len(node.children)

    def total_objects(self):
        return len(self._footprints)

    def decendants(self):
        yield from HeapNode.decendants(self.root, 0)

    def as_prometheus_metric(self):
        obj_heapsizes = defaultdict(int)
        obj_counts = defaultdict(int)

        for d in self.decendants():
            name = d.name.split('@')[0]
            obj_heapsizes[name] += d.size
            obj_counts[name] += 1

        prom_metric = TOTAL_HEAP_SIZE_METRIC_HELPS + [
            f'heap_size_bytes_total {sum(obj_heapsizes.values())}'
        ] + HEAP_SIZE_METRIC_HELPS + [
            f'heap_size_bytes{{module="{name}"}} {size}'
            for name, size in obj_heapsizes.items()
        ] + OBJ_COUNT_METRIC_HELPS + [
            f'object_count{{module="{name}"}} {count}'
            for name, count in obj_counts.items()
        ]

        return '\n'.join(prom_metric)
