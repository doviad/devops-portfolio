import socket
import sys

try:
    host = sys.argv[1]
    port = int(sys.argv[2])
except (IndexError, ValueError):
    print("Usage: python tcp-check.py <host> <port>")
    sys.exit(1)

if not 1 <= port <= 65535:
    print("[ERROR] Port must be between 1 and 65535")
    sys.exit(1)

try:
    with socket.create_connection((host, port), timeout=3):
        print(f"[OK] TCP connection to {host}:{port} succeeded")
        
except socket.gaierror:
    print(f"[ERROR] Could not resolve host: {host}")

except ConnectionRefusedError:
    print(f"[ERROR] Connection refused: {host}:{port}")

except TimeoutError:
    print(f"[ERROR] Connection timed out: {host}:{port}")

except OSError as e:
    print(f"[ERROR] Network error: {e}")