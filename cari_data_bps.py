
import os
import requests
import json

API_KEY = os.getenv("BPS_API_KEY")

if not API_KEY:
    raise ValueError("BPS_API_KEY belum tersedia.")

# Domain 0000 = nasional
url = (
    "https://webapi.bps.go.id/v1/api/"
    "list/model/subject/lang/ind/"
    "domain/0000/"
    "key/" + API_KEY
)

try:
    response = requests.get(url, timeout=30)

    print("HTTP STATUS:", response.status_code)

    if response.status_code != 200:
        print("Pesan dari server BPS:")
        print(response.text[:2000])
    else:
        result = response.json()

        print("Koneksi katalog BPS berhasil!")
        print(json.dumps(
            result,
            indent=2,
            ensure_ascii=False
        )[:10000])

except requests.exceptions.RequestException as error:
    print("Terjadi masalah koneksi:", type(error).__name__)