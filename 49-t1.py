"""TASK 1 - Diagnose and repair the hostel mess-bill script."""
import os
import time


# ---------- the original script, kept for evidence ----------
def original(path):
    f = open(path)
    data = f.read()
    total = 0
    report = ""
    for line in data.split("\n"):
        try:
            parts = line.split(",")
            total = total + int(parts[2])
            report = report + parts[1] + " " + parts[2] + "\n"
        except:
            pass
    print(report)
    print("Total", total)


# ---------- repaired design (Task 1.2) ----------
def total_bill(filename):
    """One pass, line by line; bad lines are collected, never hidden."""
    total = 0.0
    report_lines = []
    rejected = []
    with open(filename, encoding="utf-8") as f:
        for lineno, line in enumerate(f, start=1):
            parts = line.strip().split(",")
            try:
                if len(parts) != 3:
                    raise ValueError(f"expected 3 fields, found {len(parts)}")
                amount = float(parts[2])          # paise survive: 1250.50
            except ValueError as e:
                rejected.append((lineno, line.strip(), str(e)))
                continue
            total += amount
            report_lines.append(f"{parts[1].strip():12} {amount:>8.2f}")
    return total, report_lines, rejected


sample = ("1911260135A,Rohith,1250.50\n"
          "1911260140B,Asha,980\n"
          "1911260141C,Bala\n"               # damaged: only 2 fields
          "1911260142D,Charu,abc\n"          # damaged: amount not a number
          "1911260143E,Deepak,1100.25\n")

with open("/tmp/co4/mess_oct.txt", "w", encoding="utf-8") as f:
    f.write(sample)

print("--- original script on the same file ---")
original("/tmp/co4/mess_oct.txt")   # silently drops paise row AND both damaged rows; file left open

print("--- repaired version ---")
total, report, rejected = total_bill("/tmp/co4/mess_oct.txt")
print("\n".join(report))
print(f"Total {total:.2f}")
print("rejected lines:", rejected)

# ---------- scale check: 50,000 lines ----------
with open("/tmp/co4/mess_big.txt", "w", encoding="utf-8") as f:
    for i in range(50000):
        f.write(f"R{i:07d},Student{i},{1000 + i % 500}.50\n")

t0 = time.perf_counter(); total_bill("/tmp/co4/mess_big.txt"); t1 = time.perf_counter()
size = os.path.getsize("/tmp/co4/mess_big.txt")
print(f"\n50,000 lines ({size:,} bytes): repaired version {t1 - t0:.3f}s, memory ~ one line at a time")
