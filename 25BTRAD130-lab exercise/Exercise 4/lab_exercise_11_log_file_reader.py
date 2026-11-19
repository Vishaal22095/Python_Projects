
# Lab Exercise 11: Log File Reader Program
# Student Name: VISHAAL MS
# USN: 25BTRAD130


def analyze_logs(log_data):

    # Initialize counters
    counts = {
        "INFO": 0,
        "WARNING": 0,
        "ERROR": 0
    }

    print("\n=== Critical Error Messages ===")

    # Read each line from the log data
    for line in log_data.splitlines():

        for level in counts:

            if f"[{level}]" in line:
                counts[level] += 1

                if level == "ERROR":
                    print("Critical:", line.strip())

    # Display log summary
    print("\n========== LOG SUMMARY ==========")

    for level, count in counts.items():
        print(f"{level:<10}: {count} entries")

    print("=================================")


# Main program
if __name__ == "__main__":

    # Sample application log data
    log_data = """2026-10-29 10:00:00 [INFO] System started.
2026-10-29 10:05:00 [WARNING] High memory usage (84%).
2026-10-29 10:10:00 [ERROR] DB connection timed out.
2026-10-29 10:15:00 [INFO] Backup completed successfully."""

    print("=== Analyzing Application Log File ===")

    # Analyze the log information
    analyze_logs(log_data)

    print("\nLog file analysis completed successfully!")
