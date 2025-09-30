
#!/usr/bin/env python3
"""
deadline_cli.py — Command-line wrapper for deadline calculations.

Usage examples:
  # 60 business days from today (exclude today), skipping weekends, no holidays specified
  python deadline_cli.py --days 60

  # 60 business days from a trigger date, with explicit holidays
  python deadline_cli.py --days 60 --trigger 2025-10-01 --holiday 2025-11-27 --holiday 2025-11-28

  # 30 calendar days forward from today, rolling to next business day if needed, with weekends included but holidays skipped
  python deadline_cli.py --days 30 --count-kind calendar --skip-weekends false --holidays-file my_holidays.csv

  # 7 business days backward from a known deadline (works like "x days before") and roll to the preceding business day
  python deadline_cli.py --days 7 --direction backward --roll preceding --trigger 2025-12-01

Holidays file format:
  - JSON: ["2025-01-01","2025-07-04","2025-12-25"]
  - CSV: one ISO date per line, or a headered file with a column named "date" (YYYY-MM-DD).
"""

import argparse
import csv
import json
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Iterable, Set, Optional

# Import the calculator module you saved earlier.
try:
    from deadline_calculator import compute_deadline
except Exception as e:
    print("Error: could not import 'deadline_calculator'. Make sure deadline_calculator.py is on PYTHONPATH or in the same directory.", file=sys.stderr)
    raise

ROLL_CHOICES = ["none", "following", "preceding", "modified_following"]

def parse_iso_date(s: str) -> date:
    if s.lower() == "today":
        return date.today()
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"Invalid date '{s}'. Use YYYY-MM-DD or 'today'.") from exc

def str_to_bool(s: str) -> bool:
    t = s.strip().lower()
    if t in ("1", "true", "t", "yes", "y"):
        return True
    if t in ("0", "false", "f", "no", "n"):
        return False
    raise argparse.ArgumentTypeError(f"Invalid boolean '{s}'. Use true/false.")

def load_holidays_from_file(path: Path) -> Set[date]:
    if not path.exists():
        raise FileNotFoundError(f"Holidays file not found: {path}")
    if path.suffix.lower() == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, list):
            raise ValueError("JSON holidays must be a list of ISO dates (YYYY-MM-DD).")
        return {parse_iso_date(s) for s in data}
    # CSV or other text
    out: Set[date] = set()
    with path.open(newline="", encoding="utf-8") as f:
        sniff = f.read(2048)
        f.seek(0)
        # Heuristics: if it looks like CSV with commas, use csv.DictReader; else treat each line as a date
        if "," in sniff or "date" in sniff.lower():
            reader = csv.DictReader(f)
            if "date" not in (reader.fieldnames or []):
                raise ValueError("CSV holidays need a 'date' column with YYYY-MM-DD values.")
            for row in reader:
                if row.get("date"):
                    out.add(parse_iso_date(row["date"].strip()))
        else:
            # plain list, one date per line
            for line in f:
                s = line.strip()
                if not s:
                    continue
                out.add(parse_iso_date(s))
    return out

def main(argv: Optional[Iterable[str]] = None) -> int:
    p = argparse.ArgumentParser(description="Calculate legal-style deadlines.")
    p.add_argument("--days", type=int, required=True,
                   help="Number of days to add/subtract (use --direction). For 'x days before', combine with --direction backward.")
    p.add_argument("--trigger", type=parse_iso_date, default=date.today(),
                   help="Trigger date (YYYY-MM-DD or 'today'). Default: today.")
    p.add_argument("--count-kind", choices=["calendar", "business"], default="business",
                   help="Counting mode. Default: business.")
    p.add_argument("--direction", choices=["forward", "backward"], default="forward",
                   help="Direction of counting. Default: forward.")
    p.add_argument("--include-trigger", action="store_true",
                   help="If set, count the trigger day as day 1 when adding days.")
    p.add_argument("--roll", choices=ROLL_CHOICES, default="following",
                   help="Rolling rule if the result lands on a non-business day. Default: following.")
    p.add_argument("--skip-weekends", type=str_to_bool, default=True,
                   help="When count-kind=business, whether to skip weekends (true/false). Default: true.")
    p.add_argument("--holiday", action="append", default=[],
                   help="Add a holiday date (YYYY-MM-DD). May be repeated.")
    p.add_argument("--holidays-file", type=Path,
                   help="Path to JSON or CSV holiday list (see header for formats).")
    p.add_argument("--verbose", "-v", action="store_true", help="Print an explanatory summary.")
    args = p.parse_args(argv)

    # Build holidays set
    holidays: Set[date] = set()
    if args.holidays_file:
        holidays |= load_holidays_from_file(args.holidays_file)
    for h in args.holiday:
        holidays.add(parse_iso_date(h))

    # Compute
    result = compute_deadline(
        trigger_day=args.trigger,
        n=args.days,
        count_kind=args.count_kind,        # 'calendar' or 'business'
        direction=args.direction,          # 'forward' or 'backward'
        include_trigger=args.include_trigger,
        skip_weekends=args.skip_weekends,
        holidays=holidays if holidays else None,
        roll_rule=args.roll
    )

    # Output
    print(result.isoformat())
    if args.verbose:
        summary = [
            f"trigger={args.trigger.isoformat()}",
            f"days={args.days}",
            f"direction={args.direction}",
            f"count_kind={args.count_kind}",
            f"include_trigger={args.include_trigger}",
            f"skip_weekends={args.skip_weekends}",
            f"holidays={sorted(d.isoformat() for d in holidays)}",
            f"roll={args.roll}"
        ]
        print("# " + " | ".join(summary))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
