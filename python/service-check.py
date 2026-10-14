import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

checks = {
    "ssh": ("127.0.0.1", 22),
    "http": ("127.0.0.1", 80),
    "test-server": ("127.0.0.1", 8080)
}

def check_tcp(host, port):
    try:
        with socket.create_connection((host, port), timeout=3):
            return True
    except OSError:
        return False

def main():
    ok_count = 0
    error_count = 0
    for name, target in checks.items():
        host, port = target

        if check_tcp(host,port):
            print(f"[OK] {name}: {host}:{port}")
            ok_count += 1
        else:
            print(f"[ERROR] {name}: {host}:{port}")
            error_count += 1

    if error_count == 0:
            status = "OK"
    elif ok_count == 0:
            status = "CRITICAL"
    else:
            status = "WARNING"

    print("\nSummary:")
    print(f"OK: {ok_count}")
    print(f"ERROR: {error_count}")
    print(f"Overall Status: {status}")

if __name__ == "__main__":
    main()