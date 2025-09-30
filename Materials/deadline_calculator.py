
from datetime import date, timedelta
from typing import Iterable, Optional, Set, Literal

Direction = Literal["forward", "backward"]
CountKind = Literal["calendar", "business"]
RollRule = Literal["none", "following", "preceding", "modified_following"]

def _to_dateset(holidays: Optional[Iterable[date]]) -> Set[date]:
    return set(holidays) if holidays else set()

def is_weekend(d: date) -> bool:
    return d.weekday() >= 5

def is_business_day(
    d: date,
    skip_weekends: bool = True,
    holidays: Optional[Iterable[date]] = None
) -> bool:
    if skip_weekends and is_weekend(d):
        return False
    if holidays and d in holidays:
        return False
    return True

def roll(
    d: date,
    rule: RollRule,
    holidays: Optional[Iterable[date]] = None,
    skip_weekends: bool = True
) -> date:
    if rule == "none":
        return d

    holidays_set = _to_dateset(holidays)
    if is_business_day(d, skip_weekends, holidays_set):
        return d

    if rule == "following":
        dd = d
        while not is_business_day(dd, skip_weekends, holidays_set):
            dd += timedelta(days=1)
        return dd

    if rule == "preceding":
        dd = d
        while not is_business_day(dd, skip_weekends, holidays_set):
            dd -= timedelta(days=1)
        return dd

    if rule == "modified_following":
        dd = d
        while not is_business_day(dd, skip_weekends, holidays_set):
            dd += timedelta(days=1)
        if dd.month == d.month:
            return dd
        dd = d
        while not is_business_day(dd, skip_weekends, holidays_set):
            dd -= timedelta(days=1)
        return dd

    raise ValueError(f"Unknown roll rule: {rule}")

def _step(direction: Direction) -> int:
    return 1 if direction == "forward" else -1

def add_calendar_days(
    start: date,
    n: int,
    direction: Direction = "forward",
    include_start: bool = False
) -> date:
    if n < 0:
        return add_calendar_days(start, -n, "backward" if direction == "forward" else "forward", include_start)

    if n == 0:
        return start if include_start else (start if direction == "backward" else start)

    step = _step(direction)
    current = start if not include_start else (start - timedelta(days=step))

    return current + timedelta(days=step * n)

def add_business_days(
    start: date,
    n: int,
    direction: Direction = "forward",
    include_start: bool = False,
    skip_weekends: bool = True,
    holidays: Optional[Iterable[date]] = None
) -> date:
    holidays_set = _to_dateset(holidays)

    if n < 0:
        return add_business_days(start, -n, "backward" if direction == "forward" else "forward",
                                 include_start, skip_weekends, holidays_set)

    if n == 0:
        return start

    step = _step(direction)

    current = start
    if include_start:
        while not is_business_day(current, skip_weekends, holidays_set):
            current += timedelta(days=step)
        counted = 1
    else:
        current += timedelta(days=step)
        while not is_business_day(current, skip_weekends, holidays_set):
            current += timedelta(days=step)
        counted = 1

    while counted < n:
        current += timedelta(days=step)
        if is_business_day(current, skip_weekends, holidays_set):
            counted += 1

    return current

def compute_deadline(
    trigger_day: date,
    n: int,
    count_kind: CountKind = "business",
    direction: Direction = "forward",
    include_trigger: bool = False,
    skip_weekends: bool = True,
    holidays: Optional[Iterable[date]] = None,
    roll_rule: RollRule = "following"
) -> date:
    if count_kind == "calendar":
        raw = add_calendar_days(trigger_day, n, direction, include_trigger)
        return roll(raw, roll_rule if roll_rule != "none" else "none", holidays, skip_weekends)
    elif count_kind == "business":
        raw = add_business_days(trigger_day, n, direction, include_trigger, skip_weekends, holidays)
        return roll(raw, roll_rule, holidays, skip_weekends)
    else:
        raise ValueError("count_kind must be 'calendar' or 'business'.")

def x_days_before(
    deadline_day: date,
    x: int,
    count_kind: CountKind = "business",
    skip_weekends: bool = True,
    holidays: Optional[Iterable[date]] = None,
    include_end_as_day1: bool = False,
    roll_rule: RollRule = "preceding"
) -> date:
    if x < 0:
        x = -x
        direction = "forward"
    else:
        direction = "backward"

    if count_kind == "calendar":
        raw = add_calendar_days(deadline_day, x, direction, include_end_as_day1)
        return roll(raw, roll_rule, holidays, skip_weekends)
    else:
        raw = add_business_days(deadline_day, x, direction, include_end_as_day1, skip_weekends, holidays)
        return roll(raw, roll_rule, holidays, skip_weekends)
