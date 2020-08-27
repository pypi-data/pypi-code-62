"""
justnow.parser
~~~~~~~~~~~~~~

"""

from __future__ import annotations

import calendar
import datetime
import itertools
from dataclasses import dataclass
from importlib import resources
from typing import Generator, NamedTuple, Optional, Set, Tuple, Union

from lark import Lark
from lark.lexer import Token
from lark.tree import Tree

INFINITY = float("inf")


WEEKDAY_MAPPING = {
    "mon": 0,
    "tue": 1,
    "wed": 2,
    "thu": 3,
    "fri": 4,
    "sat": 5,
    "sun": 6,
    "Mon": 0,
    "Tue": 1,
    "Wed": 2,
    "Thu": 3,
    "Fri": 4,
    "Sat": 5,
    "Sun": 6,
    "monday": 0,
    "tuesday": 1,
    "wednesday": 2,
    "thursday": 3,
    "friday": 4,
    "saturday": 5,
    "sunday": 6,
}


NAMED_EVENTS = {
    "@minutely": "*-*-* *:*:00",
    "@hourly": "*-*-* *:00:00",
    "@daily": "*-*-* 00:00:00",
    "@monthly": "*-*-01 00:00:00",
    "@weekly": "Mon *-*-* 00:00:00",
    "@yearly": "*-01-01 00:00:00",
    "@quarterly": "*-01,04,07,10-01 00:00:00",
    "@semiannually": "*-01,07-01 00:00:00",
    "@annually": "*-01-01 00:00:00",
}


DEFAULT_WEEKDAY_EVENT = "mon..sun"
DEFAULT_DATE_EVENT = "*-*-*"
DEFAULT_TIME_EVENT = "00:00:00"
DEFAULT_SPECIFICATION = (
    f"{DEFAULT_WEEKDAY_EVENT} {DEFAULT_DATE_EVENT} {DEFAULT_TIME_EVENT}"
)


Number = Union[int, float]
EventSet = Set[Number]


class TimeEvent(NamedTuple):
    """Custom time event container."""

    years: EventSet
    months: EventSet
    days: EventSet
    hours: EventSet
    minutes: EventSet
    seconds: EventSet
    weekdays: Set[int]


def get_specification_ast(event: str) -> Tree:
    """Parses an time event string."""

    grammer = resources.read_text("justnow", "justnow.lark")
    parser = Lark(grammer)

    if event in NAMED_EVENTS:
        ast = parser.parse(NAMED_EVENTS[event])
    else:
        ast = parser.parse(event)

    return next(ast.find_data("specification"), None)


def get_elapse_datetime(
    event: str, reference_date: datetime.datetime
) -> Optional[datetime.datetime]:
    """Generates the next elapse datetime for the provided event string."""

    parser = EventParser(event=event, reference_date=reference_date)
    return next(parser, None)


@dataclass
class EventParser:
    """Parsers an event string and generates elapse dates.

    Note the EventParser is potentially infinite iterator. Therefore
    one should be sure before attempting to convert an instance to a
    sequence.

    To limit the number of items generated use the get_next_n method.
    """

    event: str
    reference_date: datetime.datetime

    def __post_init__(self) -> None:
        """Parse the event string."""

        self._specification_ast = get_specification_ast(event=self.event)
        self._time_event = parse_time_event(specification_ast=self._specification_ast)
        self._date_gen = get_next_elapse_datetime(
            years=self._time_event.years,
            months=self._time_event.months,
            days=self._time_event.days,
            hours=self._time_event.hours,
            minutes=self._time_event.minutes,
            seconds=self._time_event.seconds,
            weekdays=self._time_event.weekdays,
            reference_date=self.reference_date,
        )

    def __iter__(self) -> Generator[datetime.datetime, None, None]:
        return self._date_gen

    def __next__(self) -> datetime.datetime:
        return next(self._date_gen)

    def get_next_n(self, *, limit: int) -> Generator[datetime.datetime, None, None]:
        """Generate the nth next datetimes."""

        for i in range(limit):
            yield next(self._date_gen)


def parse_datepart_token(token: Token) -> Number:
    """Helper function to parse date part tokens."""

    if token == "*":
        return INFINITY
    else:
        return int(token)


def parse_weekday_section(specification_ast: Tree) -> Generator[int, None, None]:
    """Parses the weekday section of the time event.

    This function yields the weekday number from the parsed time event.
    """

    allowed_weekdays = list(specification_ast.find_data("allowed_weekdays"))
    if len(allowed_weekdays) == 0:
        default_specification = get_specification_ast(DEFAULT_SPECIFICATION)
        allowed_weekdays = default_specification.find_data("allowed_weekdays")

    for ruleset in allowed_weekdays:
        for tree in ruleset.children:
            if tree.data == "weekday_range":
                start_day_tree, end_day_tree = tree.children
                start_day = str(start_day_tree.children[0])
                end_day = str(end_day_tree.children[0])

                lower_bound, upper_bound = sorted(
                    [WEEKDAY_MAPPING[start_day], WEEKDAY_MAPPING[end_day]]
                )
                yield from range(lower_bound, upper_bound + 1)
            else:
                day = str(tree.children[0])
                yield WEEKDAY_MAPPING[day]


def parse_date_section(specification_ast: Tree) -> Tuple[EventSet, ...]:
    """Extract the year, month and date specified in the time event."""

    date_section = next(specification_ast.find_data("date_section"), None)

    if date_section is None:
        default_specification = get_specification_ast(DEFAULT_SPECIFICATION)
        date_section = next(default_specification.find_data("date_section"))

    year_section, month_section, day_section = date_section.children

    return (
        set([parse_datepart_token(token) for token in year_section.children]),
        set([parse_datepart_token(token) for token in month_section.children]),
        set([parse_datepart_token(token) for token in day_section.children]),
    )


def parse_time_section(specification_ast: Tree) -> Tuple[EventSet, ...]:
    """Extract the hour, minute and seconds specified in the time event."""

    time_section = next(specification_ast.find_data("time_section"), None)

    if time_section is None:
        default_specification = get_specification_ast(DEFAULT_SPECIFICATION)
        time_section = next(default_specification.find_data("time_section"))

    hour_section, minute_section, second_section = time_section.children

    return (
        set([parse_datepart_token(token) for token in hour_section.children]),
        set([parse_datepart_token(token) for token in minute_section.children]),
        set([parse_datepart_token(token) for token in second_section.children]),
    )


def parse_time_event(specification_ast: Tree) -> TimeEvent:
    """Extract time event data from the provided specification AST."""

    years, months, days = parse_date_section(specification_ast)
    hours, minutes, seconds = parse_time_section(specification_ast)
    weekdays = set(parse_weekday_section(specification_ast))

    return TimeEvent(
        years=years,
        months=months,
        days=days,
        hours=hours,
        minutes=minutes,
        seconds=seconds,
        weekdays=weekdays,
    )


def get_next_elapse_datetime(
    years: EventSet,
    months: EventSet,
    days: EventSet,
    hours: EventSet,
    minutes: EventSet,
    seconds: EventSet,
    weekdays: Set[int],
    reference_date: datetime.datetime,
) -> Generator[datetime.datetime, None, None]:
    """Yield the next elapse datetime."""

    if len(years) == 1 and list(years)[0] == INFINITY:
        year_gen = itertools.count(reference_date.year)
    else:
        year_gen = (int(year) for year in sorted(years))

    for search_year in year_gen:
        if search_year < reference_date.year:
            continue

        yield from walk_months(
            year=search_year,
            months=months,
            days=days,
            hours=hours,
            minutes=minutes,
            seconds=seconds,
            weekdays=weekdays,
            reference_date=reference_date,
        )


def walk_months(
    year: int,
    months: EventSet,
    days: EventSet,
    hours: EventSet,
    minutes: EventSet,
    seconds: EventSet,
    weekdays: Set[int],
    reference_date: datetime.datetime,
) -> Generator[datetime.datetime, None, None]:
    """Walk months until a match is found."""

    if len(months) == 1 and list(months)[0] == INFINITY:
        if year == reference_date.year:
            month_gen = iter(range(reference_date.month, 13))
        else:
            month_gen = iter(range(1, 13))
    else:
        month_gen = (int(month) for month in months)

    for search_month in sorted(month_gen):
        yield from walk_days(
            year=year,
            month=search_month,
            days=days,
            hours=hours,
            minutes=minutes,
            seconds=seconds,
            weekdays=weekdays,
            reference_date=reference_date,
        )


def walk_days(
    year: int,
    month: int,
    days: EventSet,
    hours: EventSet,
    minutes: EventSet,
    seconds: EventSet,
    weekdays: Set[int],
    reference_date: datetime.datetime,
) -> Generator[datetime.datetime, None, None]:
    """Walk days until a match is found."""

    if len(days) == 1 and list(days)[0] == INFINITY:
        last_day_of_month = calendar.monthrange(year, month)[1]

        start_from_reference = [
            year == reference_date.year,
            month == reference_date.month,
        ]

        if all(start_from_reference):
            day_gen = iter(range(reference_date.day, last_day_of_month + 1))
        else:
            day_gen = iter(range(1, last_day_of_month + 1))
    else:
        day_gen = (int(day) for day in sorted(days))

    for search_day in day_gen:
        if all([calendar.isleap(year) is False, month == 2, search_day == 29]):
            continue

        yield from walk_hours(
            year=year,
            month=month,
            day=search_day,
            hours=hours,
            minutes=minutes,
            seconds=seconds,
            weekdays=weekdays,
            reference_date=reference_date,
        )


def walk_hours(
    year: int,
    month: int,
    day: int,
    hours: EventSet,
    minutes: EventSet,
    seconds: EventSet,
    weekdays: Set[int],
    reference_date: datetime.datetime,
) -> Generator[datetime.datetime, None, None]:
    """Walk hours until a match is found."""

    if len(hours) == 1 and list(hours)[0] == INFINITY:
        start_from_reference = [
            year == reference_date.year,
            month == reference_date.month,
            day == reference_date.day,
        ]

        if all(start_from_reference):
            hour_gen = iter(range(reference_date.hour, 23))
        else:
            hour_gen = iter(range(0, 23))
    else:
        hour_gen = (int(hour) for hour in sorted(hours))

    for search_hour in hour_gen:
        yield from walk_minutes(
            year=year,
            month=month,
            day=day,
            hour=search_hour,
            minutes=minutes,
            seconds=seconds,
            weekdays=weekdays,
            reference_date=reference_date,
        )


def walk_minutes(
    year: int,
    month: int,
    day: int,
    hour: int,
    minutes: EventSet,
    seconds: EventSet,
    reference_date: datetime.datetime,
    weekdays: Set[int],
) -> Generator[datetime.datetime, None, None]:
    """Walk minutes until a match is found."""

    if len(minutes) == 1 and list(minutes)[0] == INFINITY:
        start_from_reference = [
            year == reference_date.year,
            month == reference_date.month,
            day == reference_date.day,
            hour == reference_date.hour,
        ]

        if all(start_from_reference):
            minute_gen = iter(range(reference_date.minute, 60))
        else:
            minute_gen = iter(range(0, 60))
    else:
        minute_gen = (int(minute) for minute in sorted(minutes))

    for search_minute in minute_gen:
        yield from walk_seconds(
            year=year,
            month=month,
            day=day,
            hour=hour,
            minute=search_minute,
            seconds=seconds,
            weekdays=weekdays,
            reference_date=reference_date,
        )


def walk_seconds(
    year: int,
    month: int,
    day: int,
    hour: int,
    minute: int,
    seconds: EventSet,
    weekdays: Set[int],
    reference_date: datetime.datetime,
) -> Generator[datetime.datetime, None, None]:
    """Walk seconds until a match is found."""

    if len(seconds) == 1 and list(seconds)[0] == INFINITY:
        start_from_reference = [
            year == reference_date.year,
            month == reference_date.month,
            day == reference_date.day,
            hour == reference_date.hour,
            minute == reference_date.minute,
        ]

        if all(start_from_reference):
            second_gen = iter(range(reference_date.second, 60))
        else:
            second_gen = iter(range(0, 60))
    else:
        second_gen = (int(second) for second in sorted(seconds))

    for search_second in second_gen:
        elapse_date = datetime.datetime(
            year=year,
            month=month,
            day=day,
            hour=hour,
            minute=minute,
            second=search_second,
            tzinfo=reference_date.tzinfo,
        )

        if elapse_date >= reference_date and elapse_date.weekday() in weekdays:
            yield elapse_date
