"""TASK 5 - the same utility organised four ways: run all four."""
import subprocess
import sys
import time

ORGS = [
    ("(a) one script", [sys.executable, "/tmp/co4/t5/org_a.py"]),
    ("(b) module + main", [sys.executable, "/tmp/co4/t5/org_b/main.py"]),
    ("(c) three modules", [sys.executable, "/tmp/co4/t5/org_c/main.py"]),
    ("(d) package attendance/", [sys.executable, "/tmp/co4/t5/org_d/main.py"]),
]

outputs = []
for name, cmd in ORGS:
    out = subprocess.run(cmd, capture_output=True, text=True, cwd=cmd[1].rsplit("/", 1)[0])
    outputs.append(out.stdout.strip())
    print(f"{name:26} ->")
    print("   " + out.stdout.strip().replace("\n", "\n   "))

print("\nall four outputs identical:", len(set(outputs)) == 1)

# import cost: package modules are loaded once and cached in sys.modules
t0 = time.perf_counter()
for _ in range(1000):
    import importlib
    import attendance  # noqa
t1 = time.perf_counter()
print(f"re-importing a cached package 1000x: {t1 - t0:.5f}s (sys.modules cache)")
