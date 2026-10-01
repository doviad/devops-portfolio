import sys
import requests
import subprocess
    
#Алгоритм выполнения команд

def run_command(command):
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Command failed: {' '.join(command)}")
        print(f"[ERROR] Exit code: {e.returncode}")
        print(f"[ERROR] {e.stderr.strip()}")
        return None
        
    except FileNotFoundError:
        print(f"[ERROR] Command not found: {command[0]}")
        return None
 

def check_hostname(): #получаем данные о хосте
    return run_command(["hostname"])
   
def check_disk(): #получаем процент использования диска
    result = run_command(["df","-h","/"])
    
    if result is None:
        return None
    
    lines = result.splitlines()
    parts = lines[1].split()
    
    usage = int(parts[4].replace("%",""))    
    
    return usage
    
def check_memory(): #получаем данные о RAM
    result = run_command(["free"])
    
    if result is None:
        return None
    
    lines = result.splitlines()
    parts = lines[1].split()
    
    total = int(parts[1])
    used = int(parts[2])
    
    usage = (used/total)*100
    
    return usage

def check_ssh(): #проверяем статус ssh
    return run_command(["systemctl","is-active","ssh"])
    
def check_github(): #проверяем API GitHub
    try:
        response = requests.get(
            "https://api.github.com",
            timeout=5
        )
        
        response.raise_for_status()
        return True
    
    except requests.exceptions.RequestException:
        return False

#Статусы

def get_usage_status(usage):
    if usage >= 80:
        return "WARNING"
    return "INFO"

def get_service_status(status):
    if status == "active":
        return "INFO"
    return "WARNING"    

def get_api_status(success):
    if success:
        return "INFO"
    return "ERROR"
    
#Выводы

def cmd_hostname():
    hostname = check_hostname()
    
    if hostname is None:
        return
    
    print(f"Hostname: {hostname}")
    
def cmd_disk():
    usage = check_disk()
    
    if usage is None:
        return 
    
    status = get_usage_status(usage)
    
    print(f"[{status}] Disk usage is {usage}%")
    
def cmd_memory():
    usage = check_memory()
    
    if usage is None:
        return 
    
    status = get_usage_status(usage)
    
    print(f"[{status}] RAM usage is {usage:.0f}%")
    
def cmd_ssh():
    status = check_ssh()
    
    if status is None:
        return 

    sign = get_service_status(status)
    
    print(f"[{sign}] SSH is {status}")
    
def cmd_github():
    success = check_github()
    
    sign = get_api_status(success)
    
    if success:
        print(f"[{sign}] GitHub is available")
    else:
        print(f"[{sign}] GitHub is unavailable")

def cmd_help():
    print("""
Usage:
    server-audit <command>

Commands:
    hostname    Show hostname
    disk        Check disk usage
    memory      Check RAM usage
    ssh         Check SSH status
    github      Check GitHub API
    help        Show this help message
""")

#Список команд
    
commands = {
    "hostname": cmd_hostname,
    "disk": cmd_disk,
    "memory": cmd_memory,
    "ssh": cmd_ssh,
    "github": cmd_github,
    "help": cmd_help
}

try:
    command = sys.argv[1]
    commands[command]()   
except IndexError:
    print("Usage: server-audit help")
    sys.exit(1)
except KeyError:
    print(f"Unknown command: {command}")
    print("Use 'server-audit help' for usage")
    sys.exit(1)