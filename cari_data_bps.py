
import os
import requests

API_KEY = os.getenv("BPS_API_KEY")

if not API_KEY:
    raise ValueError("API Key belum tersedia.")

# Endpoint katalog subjek BPS untuk wilayah nasional
base_url = "https://webapi.bps.go.id/v1/api/list/model/subject/domain/0000/key/"

url = base_url + API_KEY

print("Menghubungkan ke katalog BPS...")

try:
    response = requests.get(
        url,
        params={"lang": "ind", "page": 1},
        timeout=30
    )

    print("HTTP STATUS:", response.status_code)

    if response.status_code != 200:
        print("Pesan server:", response.text[:2000])
    else:
        result = response.json()

        print("\nKoneksi katalog berhasil!")
        print("Status:", result.get("status"))

        data = result.get("data", [])
        subjects = data[1] if len(data) > 1 else []

        keywords = [
            "ekonomi",
            "keuangan",
            "perdagangan",
            "industri",
            "pertanian",
            "tenaga kerja",
            "pengeluaran"
        ]

        print("\nSUBJEK TERKAIT EKONOMI:")

        for item in subjects:
            title = str(item.get("title", ""))
            subcat = str(item.get("subcat", ""))

            if any(word in (title + " " + subcat).lower()
                   for word in keywords):
                print(
                    f"ID: {item.get('sub_id')} | "
                    f"{title} | {subcat}"
                )

except requests.exceptions.RequestException as error:
    print("Kesalahan koneksi:", type(error).__name__)
