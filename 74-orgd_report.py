"""attendance.report: writing reports."""


def print_percentages(pcts):
    for reg, pct in pcts.items():
        print(f"{reg}: {pct:.1f}%")
