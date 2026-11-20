"""TASK 6 - College fest registration desk: package demonstration."""
import os
import sys

sys.path.insert(0, "/tmp/co4/t6")
from festreg import reader, cleaner, writer

BASE = "/tmp/co4/t6"
IN = os.path.join(BASE, "depts")
os.makedirs(IN, exist_ok=True)

# five departments -> four files (ECE missing on purpose)
files = {
    "cse.txt": "1911260135A,Rohith K,CSE,rohith@gmail.com,Coding;Quiz\n"
               "1911260140B,Asha R,CSE,asha@gmail.com,Dance\n",
    "it.txt":  "1911260141C,Bala V,IT,bala@gmail.com,Quiz;Debate\n"
               "1911260135A,Rohith K,CSE,rohith@gmail.com,Coding;Quiz\n"   # duplicate
               "1911260142D,Charu M,IT,charu@@gmail.com,Singing\n",        # invalid e-mail
    "eee.txt": "1911260143E,Deepak S,EEE,deepak@gmail.com\n",              # damaged: 4 fields
    "mech.txt": "1911260144F,Esha T,MECH,esha@gmail.com,Debate\n",
}
for name, text in files.items():
    with open(os.path.join(IN, name), "w", encoding="utf-8") as f:
        f.write(text)

master, errors, seen = [], [], set()
for dept in ("cse", "it", "eee", "ece", "mech"):
    path = os.path.join(IN, f"{dept}.txt")
    lines = reader.read_department(path)
    if lines is None:
        errors.append(f"{dept}.txt: file not found - skipped")
        continue
    for lineno, raw in lines:
        try:
            rec = cleaner.parse_line(raw)
        except ValueError as e:
            errors.append(f"{dept}.txt:{lineno}: {e}")
            continue
        if rec["reg"] in seen:
            errors.append(f"{dept}.txt:{lineno}: duplicate registration {rec['reg']} - kept first")
            continue
        seen.add(rec["reg"])
        master.append(rec)

by_event = writer.write_outputs(master, errors, os.path.join(BASE, "out"))

print("master list:")
for r in sorted(master, key=lambda r: r["reg"]):
    print(f"  {r['reg']}  {r['name']:11} {r['dept']:5} {r['email']:18} {';'.join(r['events'])}")
print("\nevent files:", {e: len(v) for e, v in sorted(by_event.items())})
print("\nerrors.log:")
for line in errors:
    print(" ", line)
print("\nprogram never stopped: 4 files processed + 1 missing file logged")
