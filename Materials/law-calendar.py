class CourtCalendar:
    def __init__(self, name: str):
        self.name = name

    def holidays_for_year(self, year: int) -> Set[date]:
        # Populate from an internal table or a JSON file your team maintains.
        return set()

    def holidays_between(self, start: date, end: date) -> Set[date]:
        years = range(start.year, end.year + 1)
        out = set()
        for y in years:
            out |= self.holidays_for_year(y)
        return {d for d in out if start <= d <= end}
