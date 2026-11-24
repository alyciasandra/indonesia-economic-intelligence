import os
import requests

API_KEY = os.getenv("BPS_API_KEY")

if not API_KEY:
    raise ValueError("API Key belum tersedia.")

# ID 9 = Laju Pertumbuhan PDB Menurut Lapangan Usaha
VARIABLE_ID = 9

url = (
    "https://webapi.bps.go.id/v1/api/"
    "list/model/th/domain/0000/var/"
    + str(VARIABLE_ID)
    + "/key/" + API_KEY
)

print("MENCARI PERIODE DATA PDB...")

try:
    response = requests.get(
        url,
        params={"lang": "ind", "page": 1},
        timeout=30
    )

    print("HTTP STATUS:", response.status_code)
    response.raise_for_status()

    result = response.json()

    print("\nSTATUS:", result.get("status"))

    data = result.get("data", [])

    if len(data) >= 2:
        metadata = data[0]
        periods = data[1]

        print("\nDAFTAR PERIODE PDB")
        print("=" * 45)

        for item in periods:
            print(
                "PERIODE ID:", item.get("th_id"),
                "| TAHUN/PERIODE:", item.get("th")
            )

        print("\nTotal halaman:", metadata.get("pages"))
        print("Total periode:", metadata.get("total"))
    else:
        print("Struktur respons perlu diperiksa.")

except requests.exceptions.RequestException as error:
    print("Kesalahan koneksi:", type(error).__name__)