import os
import requests

API_KEY = os.getenv("BPS_API_KEY")

if not API_KEY:
    raise ValueError("API Key belum tersedia.")

# Subject 11: PDB Lapangan Usaha
SUBJECT_ID = 11

url = (
    "https://webapi.bps.go.id/v1/api/"
    "list/model/var/domain/0000/subject/"
    + str(SUBJECT_ID)
    + "/key/" + API_KEY
)

print("Mencari variabel PDB BPS...")

try:
    page = 1
    total_pages = 1
    all_variables = []

    while page <= total_pages:

        response = requests.get(
            url,
            params={"lang": "ind", "page": page},
            timeout=30
        )

        print("Halaman", page, "| HTTP", response.status_code)
        response.raise_for_status()

        result = response.json()
        data = result.get("data", [])

        if len(data) < 2:
            break

        total_pages = int(data[0].get("pages", 1))
        all_variables.extend(data[1])

        page += 1

    print("\nDAFTAR VARIABEL PDB")
    print("=" * 60)

    for item in all_variables:
        print(
            "ID:", item.get("var_id"),
            "| Nama:", item.get("title")
        )

    print("\nTotal variabel:", len(all_variables))

except requests.exceptions.RequestException as error:
    print("Koneksi gagal:", type(error).__name__)