#!/usr/bin/env python3
import requests
from datetime import datetime, timezone

URLS_FILE = "urls.txt"
OUT_FILE = "adlists_merged.txt"

with open(URLS_FILE) as f:
    urls = [line.strip() for line in f if line.strip() and not line.startswith("#")]

timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

with open(OUT_FILE, "wb") as out:
    out.write(f"====# Merged on {timestamp}=====\n".encode())
    for url in urls:
        out.write(f"\n#===== START {url} =====\n".encode())
        out.write(f"# {url} - {timestamp}\n".encode())
        try:
            data = requests.get(url, timeout=30).content
            out.write(data)
            if not data.endswith(b"\n"):
                out.write(b"\n")
        except Exception as e:
            out.write(f"#====FAILED: {url} -> {e}====\n".encode())
        out.write(f"#===== END {url} =====\n".encode())
