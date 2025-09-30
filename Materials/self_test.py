
from datetime import date
from deadline_calculator import compute_deadline, x_days_before, is_business_day

cases = []

# Case 1
cases.append({
    "name": "Calendar +30 days (roll following)",
    "got": compute_deadline(date(2025,10,1), 30, count_kind="calendar", include_trigger=False, roll_rule="following"),
    "expect": date(2025,10,31)
})

# Case 2 (corrected expectation to Nov 24, 2025)
holidays = {date(2025,11,27), date(2025,11,28)}
cases.append({
    "name": "Business +10 days over Thanksgiving",
    "got": compute_deadline(date(2025,11,10), 10, count_kind="business", include_trigger=False, holidays=holidays, roll_rule="following"),
    "expect": date(2025,11,24)
})

# Case 3 (corrected expectation to Nov 18, 2025 per backward counting semantics)
deadline = date(2025,12,1)
cases.append({
    "name": "7 business days before Dec 1, 2025",
    "got": x_days_before(deadline, 7, count_kind="business", holidays=holidays, roll_rule="preceding"),
    "expect": date(2025,11,18)
})

# Case 4
cases.append({
    "name": "Modified following avoids month change",
    "got": compute_deadline(date(2025,8,1), 29, count_kind="calendar", include_trigger=False, roll_rule="modified_following"),
    "expect": date(2025,8,29)
})

# Case 5
cases.append({
    "name": "Include trigger (business)",
    "got": compute_deadline(date(2025,10,6), 5, count_kind="business", include_trigger=True, roll_rule="following"),
    "expect": date(2025,10,10)
})

failures = []
print("Self-test results:")
for c in cases:
    ok = c["got"] == c["expect"]
    print(f"- {c['name']}: got {c['got']} (expect {c['expect']}) {'OK' if ok else 'FAIL'}")
    if not ok:
        failures.append((c["name"], c["got"], c["expect"]))

if failures:
    print("\nFailures:")
    for name, got, expect in failures:
        print(f"* {name}: got {got}, expect {expect}")
    raise SystemExit(1)
else:
    print("\nAll tests passed.")
