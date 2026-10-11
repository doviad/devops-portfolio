import sys
from datetime import datetime

try:
    target = sys.argv[1].upper()
    log_path = sys.argv[2] if len(sys.argv) > 2 else "app.log"
    keyword = sys.argv[3].upper() if len(sys.argv) > 3 else None
    since = sys.argv[4] if len(sys.argv) > 4 else None
except IndexError:
    print("usage: python log-analyzer.py [INFO | WARNING | ERROR] [log_file_path] [keyword] [since]")
    sys.exit(1)

valid_levels = ["INFO", "WARNING", "ERROR"]
if target not in valid_levels:
    print(f"Invalid log level: {target}. Please use INFO, WARNING, or ERROR.")
    sys.exit(1)

if since not in [None, ""]:
    try:
        since = datetime.strptime(since, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        print("Invalid date format for 'since'. Please use 'YYYY-MM-DD HH:MM:SS'.")
        sys.exit(1)

def analyze_log(target, log_path, keyword, since):
    levels = {
        "INFO": 0,
        "WARNING": 0,
        "ERROR": 0
    }
    try:
        with open(log_path, "r", encoding="utf-8") as file:
            count = 0
            missed_count = 0
            for line in file:
                parts = line.split()
                if len(parts) < 3:
                    missed_count += 1
                    continue  # Skip lines that don't have a valid log level


                level = parts[2].upper()

                if level not in valid_levels:
                    missed_count += 1
                    continue  # Skip lines with invalid log levels

                try:
                    line_time = datetime.strptime(f"{parts[0]} {parts[1]}", "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    missed_count += 1
                    continue  # Skip lines with invalid date format

                levels[level] += 1

                if since is not None and line_time < since: 
                    continue  # Skip lines that are before the 'since' date

                if target == level and (keyword is None or keyword in line.upper()):
                    print(line, end="")
                    count += 1
                
    except FileNotFoundError:
        print(f"Error: {log_path} not found.")
        sys.exit(1)
    print(f"\nTotal {target.lower()}s found: {count}")
    print(f"\nLog statistics:\nINFO: {levels['INFO']}, WARNING: {levels['WARNING']}, ERROR: {levels['ERROR']}\nTotal: {sum(levels.values())}")
    print(f"Skipped malformed lines: {missed_count}")

analyze_log(target, log_path, keyword, since)