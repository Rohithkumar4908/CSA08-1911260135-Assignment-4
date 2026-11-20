"""TASK 3 - Exceptions in the attendance processor."""
import os
import tempfile


class InvalidRecord(Exception):
    """Raised when a line of the attendance file is not in the expected format."""


def parse_line(line):
    """'192311001,2026-10-08,P' -> ('192311001', '2026-10-08', 'P')"""
    parts = line.strip().split(",")
    # TODO 1 completed: exactly 3 fields and status P or A
    if len(parts) != 3:
        raise InvalidRecord(f"expected 3 fields, found {len(parts)}")
    if parts[2] not in ("P", "A"):
        raise InvalidRecord(f"invalid status {parts[2]!r}")
    return parts[0], parts[1], parts[2]


def summarise(path):
    present, absent, errors = 0, 0, []
    # TODO 2 completed: with statement, try/except InvalidRecord per line
    try:
        f = open(path, encoding="utf-8")
    except FileNotFoundError as e:
        raise InvalidRecord(f"cannot open input file: {path}") from e
    else:
        try:
            for lineno, line in enumerate(f, start=1):
                try:
                    reg, date, status = parse_line(line)
                except InvalidRecord as e:
                    errors.append((lineno, str(e)))
                else:
                    if status == "P":
                        present += 1
                    else:
                        absent += 1
        finally:
            f.close()
    return present, absent, errors


data = ("192311001,2026-10-08,P\n192311002,2026-10-08,A\n"
        "192311003,2026-10-08\n192311004,2026-10-08,L\n")
with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False,
                                 encoding="utf-8") as tmp:
    tmp.write(data)
print(summarise(tmp.name))
os.remove(tmp.name)

# ---- missing file: handled through the custom exception with its cause ------
try:
    summarise("attendance_2026-13-99.csv")
except InvalidRecord as e:
    print("handled:", e)
    print("original cause:", repr(e.__cause__))

# ---- Task 3.4 misuse experiment: except Exception: pass hides a typing error --
def summarise_misuse(path):
    present, absent = 0, 0
    with open(path, encoding="utf-8") as f:
        for line in f:
            try:
                reg, date, status = parse_line(line)
                if status == "P":
                    presennt += 1          # typing error: NameError at runtime
                else:
                    absent += 1
            except Exception:
                pass
    return present, absent


with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False,
                                 encoding="utf-8") as tmp:
    tmp.write("192311001,2026-10-08,P\n192311002,2026-10-08,P\n192311003,2026-10-08,A\n")
print("correct count is (2, 1); misuse version returns:", summarise_misuse(tmp.name))
print("-> the NameError from the typo was swallowed by except Exception: pass,",
      "so present days silently vanished and no traceback appeared.")
os.remove(tmp.name)
