"""TASK 2 - Biometric attendance files: data model + monthly processing."""
import glob
import os

DATA = "/tmp/co4/att"

# ---- one file per day: "regno,date,status"; some lines damaged -------------
days = {
    "att_2026-10-05.txt": "1911260135A,2026-10-05,P\n1911260140B,2026-10-05,P\n",
    "att_2026-10-06.txt": "1911260135A,2026-10-06,P\n1911260140B,2026-10-06\n",   # damaged: 2 fields
    "att_2026-10-07.txt": "1911260135A,2026-10-07,A\n1911260140B,2026-10-07,L\n",  # damaged: bad status
    "att_2026-10-08.txt": "1911260135A,2026-10-08,A\n1911260140B,2026-10-08,A\n",
}
os.makedirs(DATA, exist_ok=True)
for name, text in days.items():
    with open(os.path.join(DATA, name), "w", encoding="utf-8") as f:
        f.write(text)


def process_month(folder):
    """Accumulate counts in one pass over every daily file."""
    present, total = {}, {}
    rejected = []
    files = sorted(glob.glob(os.path.join(folder, "att_*.txt")))
    for path in files:
        with open(path, encoding="utf-8") as f:          # iteration = one line at a time
            for lineno, line in enumerate(f, start=1):
                parts = line.strip().split(",")
                if len(parts) != 3 or parts[2] not in ("P", "A"):
                    rejected.append((os.path.basename(path), lineno, line.strip()))
                    continue
                reg = parts[0]
                total[reg] = total.get(reg, 0) + 1
                if parts[2] == "P":
                    present[reg] = present.get(reg, 0) + 1
    return present, total, rejected, files


present, total, rejected, files = process_month(DATA)

with open("/tmp/co4/attendance_report.txt", "w", encoding="utf-8") as out, \
     open("/tmp/co4/defaulters.txt", "w", encoding="utf-8") as dfl, \
     open("/tmp/co4/errors.log", "w", encoding="utf-8") as log:
    for reg in sorted(total):
        pct = 100 * present.get(reg, 0) / total[reg]
        out.write(f"{reg},{present.get(reg, 0)}/{total[reg]},{pct:.1f}%\n")
        if pct < 75:
            dfl.write(f"{reg},{pct:.1f}%\n")
    for fname, lineno, text in rejected:
        log.write(f"{fname}:{lineno}: {text}\n")

print(f"files read once each: {[os.path.basename(p) for p in files]}")
print("attendance_report.txt:")
print(open("/tmp/co4/attendance_report.txt").read(), end="")
print("defaulters.txt (<75%):")
print(open("/tmp/co4/defaulters.txt").read(), end="")
print("errors.log:")
print(open("/tmp/co4/errors.log").read(), end="")

# ---- Task 2.4 trace: one small file containing a damaged line ----------------
print("\nTRACE of att_2026-10-06.txt:")
for lineno, line in enumerate(open(os.path.join(DATA, "att_2026-10-06.txt")), 1):
    parts = line.strip().split(",")
    ok = len(parts) == 3 and parts[2] in ("P", "A")
    print(f"  line {lineno}: {line.strip()!r:38} -> {'counted ' + parts[2] if ok else 'REJECTED (damaged)'}")
