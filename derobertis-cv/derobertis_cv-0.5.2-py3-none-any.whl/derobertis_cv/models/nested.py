from dataclasses import dataclass, field
from typing import Sequence, Optional

from weakreflist import WeakList


class NestedModel:
    parents: Optional[Sequence['NestedModel']]
    children: WeakList

    def __init__(self):
        if self.parents is not None:
            for parent in self.parents:
                parent.children.append(self)