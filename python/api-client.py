import requests
import logging
from pathlib import Path

path = Path("./app.log")
logging.basicConfig( level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", handlers=[logging.FileHandler(path, encoding="utf-8"), logging.StreamHandler()])
url = "https://api.github.com/repos/doviad/mise_app"

try:
    response = requests.get(url, timeout=3)
    response.raise_for_status()
    logging.info("GitHub API request successful")
    print(f"Status: {response.status_code}")
    print(f"Response time: {response.elapsed.total_seconds()}s")

    data = response.json()
    print(f"Name: {data['name']}")
    print(f"Description: {data.get('description') or 'no description'}")
    print(f"URL: {data['html_url']}")
except requests.exceptions.Timeout:
    logging.error("Request timed out")
except requests.exceptions.HTTPError as e:
    logging.error(f"HTTP error occurred: {e}")
except requests.exceptions.RequestException as e:
    logging.error(f"An error occurred: {e}")

