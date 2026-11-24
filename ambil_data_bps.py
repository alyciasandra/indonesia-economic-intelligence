import os
import requests
import json
from pathlib import Path

# ==========================================
# 1. KONFIGURASI API BPS
# ==========================================

API_KEY = os.getenv("BPS_API_KEY")

if not API_KEY:
    raise ValueError(
        "API KEY belum ditemukan. "
        "Silakan atur environment variable BPS_API_KEY."
    )

# ==========================================
# 2. ENDPOINT DAFTAR WILAYAH BPS
# ==========================================

url = (
    "https://webapi.bps.go.id/v1/api/"
    "domain/type/prov/key/" + API_KEY
)

# ==========================================
# 3. MENGAMBIL DATA
# ==========================================

print("Menghubungkan ke BPS WebAPI...")

try:
    response = requests.get(url, timeout=30)

    print("HTTP Status:", response.status_code)

    response.raise_for_status()

    data = response.json()

    # ======================================
    # 4. MEMERIKSA RESPONS
    # ======================================

    if data.get("status") != "OK":
        raise ValueError("Respons API BPS tidak menunjukkan status OK.")

    print("\nKoneksi API BPS berhasil!")
    print("Status:", data.get("status"))
    print("Ketersediaan:", data.get("data-availability"))

    # ======================================
    # 5. MENYIMPAN DATA JSON
    # ======================================

    output_file = Path("data_wilayah_bps.json")

    with output_file.open("w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("\nData berhasil disimpan:", output_file)

    # ======================================
    # 6. MENAMPILKAN DAFTAR WILAYAH
    # ======================================

    print("\nDAFTAR PROVINSI INDONESIA:")

    records = data.get("data", [])

    if len(records) > 1 and isinstance(records[1], list):
        provinces = records[1]

        for province in provinces:
            print(
                province.get("domain_id"),
                "-",
                province.get("domain_name")
            )

        print("\nJumlah data wilayah:", len(provinces))
    else:
        print("Struktur data wilayah perlu diperiksa.")

except requests.exceptions.HTTPError:
    print("Server BPS menolak permintaan.")
    print("Periksa API Key dan parameter permintaan.")

except requests.exceptions.RequestException as error:
    print("Kesalahan koneksi:", type(error).__name__)

except (ValueError, KeyError) as error:
    print("Kesalahan pengolahan data:", error)