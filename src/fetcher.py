import os
import time
import requests

USER_AGENT = "FlyRankInternshipA9/1.0 (+https://github.com/Mj-Abraham/Scrapped-FlyRank-Assignment)"
TIMEOUT = 10  # seconds
DELAY = 0.5   # seconds between real requests


def fetch(url: str, cache_path: str, retries: int = 1) -> str:
    """Fetch a URL, using a local cache if available. Returns HTML text.
    Retries only on timeouts / 5xx server errors. Never retries 404 or 403."""

    if os.path.exists(cache_path):
        with open(cache_path, "r", encoding="utf-8") as f:
            html = f.read()
        print(f"CACHE HIT  {url}  ({len(html)} bytes)")
        return html

    for attempt in range(retries + 1):
        time.sleep(DELAY)
        try:
            resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=TIMEOUT)
        except requests.Timeout:
            if attempt < retries:
                print(f"TIMEOUT    {url}  (retrying)")
                continue
            raise RuntimeError(f"Timeout fetching {url}")
        except requests.RequestException as e:
            raise RuntimeError(f"Request failed for {url}: {e}")

        if resp.status_code == 200:
            os.makedirs(os.path.dirname(cache_path), exist_ok=True)
            with open(cache_path, "w", encoding="utf-8") as f:
                f.write(resp.text)
            print(f"FETCH      {url}  ({len(resp.text)} bytes)")
            return resp.text
        elif resp.status_code >= 500 and attempt < retries:
            print(f"SERVER ERR {url}  ({resp.status_code}, retrying)")
            continue
        else:
            raise RuntimeError(f"Failed fetch: {url} returned {resp.status_code}")