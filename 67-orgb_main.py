"""Organisation (b): main script importing the module."""
import attendance_utils as att


def main():
    rows = att.read_rows("/tmp/co4/t5/att.csv")
    for reg, pct in att.percentages(rows).items():
        print(f"{reg}: {pct:.1f}%")
    print("absent 3 days in a row:", att.absent_streaks(rows))


if __name__ == "__main__":
    main()
