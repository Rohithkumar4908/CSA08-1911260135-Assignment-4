"""TASK 4 - File and exception forensics: the library returns log."""
import os

os.chdir("/tmp/co4")
for f in ("returns.log", "errors.log"):
    if os.path.exists(f):
        os.remove(f)


# ---------- the original program ----------
def save_returns_buggy(books):
    log = open("returns.log", "w")     # "w" erases the whole log every day
    for b in books:
        log.write(b)                   # no newline: titles run together
    log.close()


def process_buggy(day_file):
    try:
        books = open(day_file).read().split("\n")
        save_returns_buggy(books)
    except FileNotFoundError:
        print("missing")               # printed on screen, never recorded


with open("day1.txt", "w") as f:
    f.write("1984\nDune\n")
with open("day2.txt", "w") as f:
    f.write("Gita\nWings of Fire\n")

print("--- original program over three days ---")
process_buggy("day1.txt")
process_buggy("day2.txt")
process_buggy("day3.txt")              # does not exist
print("returns.log after 3 days:", repr(open("returns.log").read()))
print("defects visible: day 1 lost (truncated by 'w'), titles joined (no newlines),",
      "day 3's error only printed, not logged")

# ---------- repaired program ----------
def save_returns(books):
    with open("returns.log", "a", encoding="utf-8") as log:   # append, not truncate
        for b in books:
            log.write(b + "\n")


def process(day_file):
    try:
        with open(day_file, encoding="utf-8") as f:
            books = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        with open("errors.log", "a", encoding="utf-8") as err:
            err.write(f"missing file: {day_file}\n")
        return
    save_returns(books)


os.remove("returns.log")
print("\n--- repaired program over three days ---")
process("day1.txt")
process("day2.txt")
process("day3.txt")
print("returns.log:", repr(open("returns.log").read()))
print("errors.log :", repr(open("errors.log").read()))
