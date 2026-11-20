"""Organisation (c): three modules in one folder + main script."""
import reader
import stats
import report


def main():
    rows = reader.read_rows("/tmp/co4/t5/att.csv")
    report.print_percentages(stats.percentages(rows))
    print("absent 3 days in a row:", stats.absent_streaks(rows))


if __name__ == "__main__":
    main()
