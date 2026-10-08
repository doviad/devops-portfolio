import subprocess
import sys

try:
    target = sys.argv[1]
    cpu_threshold = float(sys.argv[2]) if len(sys.argv) > 2 else 0.0
    mem_threshold = float(sys.argv[3]) if len(sys.argv) > 3 else 0.0
    sort_by = sys.argv[4] if len(sys.argv) > 4 else "cpu"
    limit = int(sys.argv[5]) if len(sys.argv) > 5 else None

except (IndexError, ValueError):
    print("Usage: python process-check.py <process_name> [cpu_threshold] [mem_threshold] [sort_by(cpu|mem)] [limit]")
    sys.exit(1)

if sort_by not in ["cpu", "mem"]:
    print("Invalid sort_by value. Use 'cpu' or 'mem'.")
    sys.exit(1)

if limit is not None and limit <= 0:
    print("Limit must be a positive integer.")
    sys.exit(1)

def get_processes():
    result = subprocess.run(["ps", "-eo", "pid,comm,%cpu,%mem"], capture_output=True, text=True, check=True)

    lines = result.stdout.strip().splitlines()

    processes = lines[1:] 

    return processes

processes = get_processes()

def find_processes(processes, target, cpu_threshold, mem_threshold):    
    found = []

    for process in processes:
        parts = process.split()

        pid = int(parts[0])
        command = " ".join(parts[1:-2])
        cpu = float(parts[-2])
        mem = float(parts[-1])

        if target in command and cpu > cpu_threshold and mem > mem_threshold:
            found.append((pid, command, cpu, mem))

    return found

found = find_processes(processes, target, cpu_threshold, mem_threshold)
if sort_by == "cpu":
    found.sort(key=lambda process: process[2], reverse=True)
elif sort_by == "mem":
    found.sort(key=lambda process: process[3], reverse=True)

found_count = len(found)

if found:
    if limit is not None:
        found = found[:limit]
    for pid, command, cpu, mem in found:
        print(f"PID: {pid}, Command: {command}, CPU: {cpu}%, Memory: {mem}%")

    print(f"Found {found_count} processes matching '{target}' with CPU usage above {cpu_threshold}% and Memory usage above {mem_threshold}%")
else:
    print(f"No processes matching '{target}' found with CPU usage above {cpu_threshold}% and Memory usage above {mem_threshold}%")