import os
import requests

API_KEY = os.getenv("BPS_API_KEY")

if not API_KEY:
    raise ValueError("API Key belum tersedia.")

# Semua variabel PDB yang ditemukan sebelumnya
VARIABLES = {
    8: "PDB Menurut Lapangan Usaha",
    9: "Laju Pertumbuhan PDB",
    65: "PDB Seri 2010",
    104: "Laju Pertumbuhan PDB Seri 2010",
    105: "Laju Implisit PDB",
    106: "Distribusi PDB",
    129: "Indeks Implisit PDB",
    554: "Sumber Pertumbuhan PDB"
}

print("MEMERIKSA PERIODE SELURUH VARIABEL PDB")
print("=" * 65)

for var_id, name in VARIABLES.items():

    url = (
        "https://webapi.bps.go.id/v1/api/"
        "list/model/th/domain/0000/var/"
        + str(var_id)
        + "/key/" + API_KEY
    )

    try:
        page = 1
        total_pages = 1
        periods = []

        while page <= total_pages:

            response = requests.get(
                url,
                params={"lang": "ind", "page": page},
                timeout=30
            )

            response.raise_for_status()

            result = response.json()
            data = result.get("data", [])

            if len(data) < 2:
                break

            total_pages = int(data[0].get("pages", 1))
            periods.extend(data[1])

            page += 1

        years = [
            str(item.get("th"))
            for item in periods
        ]

        print("\nID VARIABEL:", var_id)
        print("NAMA:", name)
        print("JUMLAH PERIODE:", len(periods))

        if years:
            print("PERIODE TERBARU:", years[0])
            print("PERIODE TERLAMA:", years[-1])
        else:
            print("Tidak ada periode tersedia.")

    except Exception as error:
        print("\nID:", var_id, "| Gagal:", type(error).__name__)

print("\nPEMERIKSAAN SELESAI")