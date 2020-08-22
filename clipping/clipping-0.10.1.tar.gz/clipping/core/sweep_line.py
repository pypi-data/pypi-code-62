from functools import partial
from typing import (Callable,
                    Generic,
                    Optional,
                    cast)

from dendroid import red_black
from dendroid.hints import Sortable
from reprit.base import generate_repr
from robust.angular import (Orientation,
                            orientation)

from .event import (BinaryEvent,
                    Event,
                    NaryEvent)


class SweepLine(Generic[Event]):
    __slots__ = '_tree',

    def __init__(self, key: Callable[[Event], Sortable]) -> None:
        self._tree = red_black.tree(key=key)

    __repr__ = generate_repr(__init__)

    def __contains__(self, event: Event) -> bool:
        return event in self._tree

    def add(self, event: Event) -> None:
        self._tree.add(event)

    def remove(self, event: Event) -> None:
        self._tree.remove(event)

    def above(self, event: Event) -> Optional[Event]:
        try:
            return self._tree.next(event)
        except ValueError:
            return None

    def below(self, event: Event) -> Optional[Event]:
        try:
            return self._tree.prev(event)
        except ValueError:
            return None


class BinarySweepLineKey:
    __slots__ = 'event',

    def __init__(self, event: BinaryEvent) -> None:
        self.event = event

    __repr__ = generate_repr(__init__)

    def __lt__(self, other: 'BinarySweepLineKey') -> bool:
        """
        Checks if the segment (or at least the point) associated with event
        is lower than other's.
        """
        event, other_event = self.event, other.event
        if event is other_event:
            return False
        start, other_start = event.start, other_event.start
        end, other_end = event.end, other_event.end
        other_start_orientation = orientation(end, start, other_start)
        other_end_orientation = orientation(end, start, other_end)
        if other_start_orientation is other_end_orientation:
            start_x, start_y = start
            other_start_x, other_start_y = other_start
            if other_start_orientation is not Orientation.COLLINEAR:
                # other segment fully lies on one side
                return other_start_orientation is Orientation.COUNTERCLOCKWISE
            # segments are collinear
            elif event.from_left is not other_event.from_left:
                return event.from_left
            elif start_x == other_start_x:
                end_x, end_y = end
                other_end_x, other_end_y = other_end
                if start_y != other_start_y:
                    # segments are vertical
                    return start_y < other_start_y
                # segments have same start
                elif end_y != other_end_y:
                    return end_y < other_end_y
                else:
                    # segments are horizontal
                    return end_x < other_end_x
            elif start_y != other_start_y:
                return start_y < other_start_y
            else:
                # segments are horizontal
                return start_x < other_start_x
        start_orientation = orientation(other_end, other_start, start)
        end_orientation = orientation(other_end, other_start, end)
        if start_orientation is end_orientation:
            return start_orientation is Orientation.CLOCKWISE
        elif other_start_orientation is Orientation.COLLINEAR:
            return other_end_orientation is Orientation.COUNTERCLOCKWISE
        elif start_orientation is Orientation.COLLINEAR:
            return end_orientation is Orientation.CLOCKWISE
        elif end_orientation is Orientation.COLLINEAR:
            return start_orientation is Orientation.CLOCKWISE
        else:
            return other_start_orientation is Orientation.COUNTERCLOCKWISE


class NarySweepLineKey:
    __slots__ = 'event',

    def __init__(self, event: NaryEvent) -> None:
        self.event = event

    __repr__ = generate_repr(__init__)

    def __lt__(self, other: 'NarySweepLineKey') -> bool:
        """
        Checks if the segment (or at least the point) associated with event
        is lower than other's.
        """
        event, other_event = self.event, other.event
        if event is other_event:
            return False
        start, other_start = event.start, other_event.start
        end, other_end = event.end, other_event.end
        other_start_orientation = orientation(end, start, other_start)
        other_end_orientation = orientation(end, start, other_end)
        if other_start_orientation is other_end_orientation:
            start_x, start_y = start
            other_start_x, other_start_y = other_start
            if other_start_orientation is not Orientation.COLLINEAR:
                # other segment fully lies on one side
                return other_start_orientation is Orientation.COUNTERCLOCKWISE
            # segments are collinear
            elif start_x == other_start_x:
                end_x, end_y = end
                other_end_x, other_end_y = other_end
                if start_y != other_start_y:
                    # segments are vertical
                    return start_y < other_start_y
                # segments have same start
                elif end_y != other_end_y:
                    return end_y < other_end_y
                else:
                    # segments are horizontal
                    return end_x < other_end_x
            elif start_y != other_start_y:
                return start_y < other_start_y
            else:
                # segments are horizontal
                return start_x < other_start_x
        start_orientation = orientation(other_end, other_start, start)
        end_orientation = orientation(other_end, other_start, end)
        if start_orientation is end_orientation:
            return start_orientation is Orientation.CLOCKWISE
        elif other_start_orientation is Orientation.COLLINEAR:
            return other_end_orientation is Orientation.COUNTERCLOCKWISE
        elif start_orientation is Orientation.COLLINEAR:
            return end_orientation is Orientation.CLOCKWISE
        elif end_orientation is Orientation.COLLINEAR:
            return start_orientation is Orientation.CLOCKWISE
        else:
            return other_start_orientation is Orientation.COUNTERCLOCKWISE


BinarySweepLine = cast(Callable[[], SweepLine[BinaryEvent]],
                       partial(SweepLine, BinarySweepLineKey))
NarySweepLine = cast(Callable[[], SweepLine[NaryEvent]],
                     partial(SweepLine, NarySweepLineKey))
