import os
import requests
import json

# Membaca API Key dari environment variable
API_KEY = os.getenv("BPS_API_KEY")

if not API_KEY:
    raise ValueError(
        "API Key belum ditemukan. "
        "Atur environment variable BPS_API_KEY terlebih dahulu."
    )

# Endpoint pengujian: daftar provinsi
url = (
    "https://webapi.bps.go.id/v1/api/"
    "domain/type/prov/key/" + API_KEY
)

try:
    response = requests.get(url, timeout=30)
    response.raise_for_status()

    result = response.json()

    print("Koneksi API BPS berhasil!")
    print(json.dumps(result, indent=2, ensure_ascii=False)[:3000])

except requests.exceptions.RequestException as error:
    print("Terjadi kesalahan saat mengakses API:")
    print(error)

except ValueError as error:
    print("Respons tidak dapat dibaca sebagai JSON:")
    print(error)