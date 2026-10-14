import json
from pathlib import Path
import os
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s",
handlers = [ logging.FileHandler("cfg-reader.log", encoding="utf-8"), logging.StreamHandler()])
path = Path("config.json")

if path.exists():
    config = json.loads(path.read_text(encoding="utf-8"))

    host = os.getenv("HOST", config["host"])
    port = int(os.getenv("PORT", config["port"]))
    timeout = int(os.getenv("TIMEOUT", config["timeout"]))

    logging.info(f"Server will run on {host}:{port}. Timeout is set to {timeout} seconds.")
else:
    logging.error("Configuration file 'config.json' not found.")
    exit(1)