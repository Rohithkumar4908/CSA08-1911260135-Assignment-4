"""Organisation (b): one module with all the functions."""


def read_rows(path):
    with open(path, encoding="utf-8") as f:
        return [line.strip().split(",") for line in f if line.strip()]


def percentages(rows):
    present, total = {}, {}
    for reg, date, status in rows:
        total[reg] = total.get(reg, 0) + 1
        if status == "P":
            present[reg] = present.get(reg, 0) + 1
    return {reg: 100 * present.get(reg, 0) / total[reg] for reg in sorted(total)}


def absent_streaks(rows, days=3):
    """Reg numbers absent `days` consecutive dates (feature added later)."""
    by_reg = {}
    for reg, date, status in rows:
        by_reg.setdefault(reg, []).append((date, status))
    flagged = []
    for reg, entries in by_reg.items():
        streak = 0
        for date, status in sorted(entries):
            streak = streak + 1 if status == "A" else 0
            if streak >= days:
                flagged.append(reg)
                break
    return sorted(flagged)
