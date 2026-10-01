import subprocess

result = subprocess.run(
	["df","-h","/"],
	capture_output=True,
	text=True,
	check=True
)

lines = result.stdout.strip().splitlines()

parts = lines[1].split()

usage = int(parts[4].replace("%", ""))

def check_disk_usage(usage):
    if usage >= 80:
        return f"[WARNING] Disk usage is: {usage}%"
    else:
        return f"[INFO] Disk usage is: {usage}%"

print(check_disk_usage(usage))
