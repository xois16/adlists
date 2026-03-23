#!/usr/bin/env python3
import sys
from pathlib import Path
from datetime import datetime
import requests


URLS = [
    "https://big.oisd.nl",
    "https://nsfw.oisd.nl",
    "https://phishing.army/download/phishing_army_blocklist_extended.txt",
    "https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/fakenews-gambling-porn/hosts",
    "https://adguardteam.github.io/AdGuardSDNSFilter/Filters/filter.txt"
]

OUT = Path("adlists_merged.txt")
TMP_DIR = Path("downloads")
TMP_DIR.mkdir(exist_ok=True)

def fetch(url, timeout=30):
    try:
        r = requests.get(url, timeout=timeout)
        r.raise_for_status()
        return r.content
    except Exception as e:
        return f"FAILED: {url} -> {e}\n".encode()

def main():
    with OUT.open("wb") as out:
        out.write(f"## Merged on {datetime.utcnow().isoformat()}Z\n\n".encode())
        for url in URLS:
            out.write(f"\n#=== START {url} ===\n".encode())
            data = fetch(url)
            out.write(data)
            if not data.endswith(b"\n"):
                out.write(b"\n")
            out.write(f"#=== END {url} ===\n".encode())

if __name__ == "__main__":
    main()
