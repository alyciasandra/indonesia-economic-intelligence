import os
import requests

# 1. Membaca API Key
API_KEY = os.getenv("BPS_API_KEY")

if not API_KEY:
    raise ValueError("API Key belum tersedia!")

# 2. Endpoint katalog subjek BPS
url = "https://webapi.bps.go.id/v1/api/list/model/subject/lang/ind/key/" + API_KEY

# 3. Mengirim permintaan
print("Menghubungkan ke BPS...")

try:
    response = requests.get(url, timeout=30)

    print("HTTP STATUS:", response.status_code)

    if response.status_code == 200:
        result = response.json()

        print("\nKoneksi berhasil!")
        print("Status:", result.get("status"))

        records = result.get("data", [])
        subjects = []

        for group in records:
            if isinstance(group, list):
                subjects.extend(group)

        print("\nDAFTAR SUBJEK EKONOMI:")

        keywords = [
            "ekonomi",
            "keuangan",
            "perdagangan",
            "industri",
            "pertanian",
            "tenaga kerja",
            "pengeluaran"
        ]

        found = 0

        for item in subjects:
            title = str(item.get("title", ""))
            subcat = str(item.get("subcat", ""))

            if any(k in (title + " " + subcat).lower()
                   for k in keywords):

                print(
                    "ID:", item.get("sub_id"),
                    "| Subjek:", title,
                    "| Kategori:", subcat
                )
                found += 1

        print("\nJumlah subjek relevan:", found)

    else:
        print("\nPermintaan ditolak oleh server BPS.")
        print("Pesan server:", response.text[:1500])

except requests.exceptions.RequestException as error:
    print("Kesalahan koneksi:", type(error).__name__)