
import os
import requests
import json

API_KEY = os.getenv("BPS_API_KEY")

if not API_KEY:
    raise ValueError("BPS_API_KEY belum tersedia")

# Mengambil daftar subjek statistik BPS
url = (
    "https://webapi.bps.go.id/v1/api/"
    "list/model/subject/lang/ind/key/"
    + API_KEY
    + "/"
)

response = requests.get(url, timeout=30)
response.raise_for_status()

result = response.json()

print("STATUS:", result.get("status"))
print("\nDAFTAR SUBJEK BPS:\n")

print(json.dumps(
    result,
    indent=2,
    ensure_ascii=False
)[:10000])