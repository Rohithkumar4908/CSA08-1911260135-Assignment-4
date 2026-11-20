"""festreg.writer: master list, event-wise lists, summary and error log."""
import os


def write_outputs(master, errors, outdir):
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "master_list.txt"), "w", encoding="utf-8") as f:
        for r in sorted(master, key=lambda r: r["reg"]):
            f.write(f"{r['reg']},{r['name']},{r['dept']},{r['email']},{';'.join(r['events'])}\n")
    by_event = {}
    for r in master:
        for e in r["events"]:
            by_event.setdefault(e, []).append(r["reg"])
    for event, regs in by_event.items():
        with open(os.path.join(outdir, f"event_{event.replace(' ', '_')}.txt"), "w",
                  encoding="utf-8") as f:
            f.write("\n".join(sorted(regs)) + "\n")
    with open(os.path.join(outdir, "summary.txt"), "w", encoding="utf-8") as f:
        f.write(f"registrations accepted: {len(master)}\n")
        for event, regs in sorted(by_event.items()):
            f.write(f"{event}: {len(regs)} participants\n")
        f.write(f"errors logged: {len(errors)}\n")
    with open(os.path.join(outdir, "errors.log"), "w", encoding="utf-8") as f:
        for line in errors:
            f.write(line + "\n")
    return by_event
