import argparse
import json
from pathlib import Path

path = Path("config.json")

config = json.loads(path.read_text(encoding="utf-8"))
parser = argparse.ArgumentParser(description="Server configuration")

parser.add_argument("--host", default=config.get("host", "127.0.0.1"))
parser.add_argument("--port", type=int, default=config.get("port", 8080))

args = parser.parse_args()

print(f"Server will run on {args.host}:{args.port}")
print(config["host"])
print(config["port"])
print(config["timeout"])