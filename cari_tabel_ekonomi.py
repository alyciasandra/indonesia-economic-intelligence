import os
import requests

API_KEY = os.getenv("BPS_API_KEY")

if not API_KEY:
    raise ValueError("API Key belum tersedia.")

base_url = (
    "https://webapi.bps.go.id/v1/api/"
    "list/model/subject/domain/0000/key/"
    + API_KEY
)

keywords = [
    "ekonomi",
    "produk domestik",
    "pdb",
    "inflasi",
    "tenaga kerja",
    "pengangguran",
    "harga",
    "industri"
]

all_subjects = []

print("MENGAMBIL SELURUH KATALOG BPS...")

try:
    page = 1
    total_pages = 1

    while page <= total_pages:

        response = requests.get(
            base_url,
            params={"lang": "ind", "page": page},
            timeout=30
        )

        print("Halaman:", page,
              "| HTTP:", response.status_code)

        response.raise_for_status()

        result = response.json()
        data = result.get("data", [])

        if len(data) < 2:
            break

        metadata = data[0]
        subjects = data[1]

        total_pages = int(metadata.get("pages", 1))

        all_subjects.extend(subjects)

        page += 1

    print("\nTOTAL SUBJEK:", len(all_subjects))

    print("\nHASIL PENCARIAN EKONOMI")
    print("=" * 55)

    found = 0

    for item in all_subjects:

        title = str(item.get("title", ""))
        category = str(item.get("subcat", ""))

        text = (title + " " + category).lower()

        if any(keyword in text for keyword in keywords):

            print(
                "ID:", item.get("sub_id"),
                "|", title,
                "|", category
            )

            found += 1

    if found == 0:
        print("Tidak ditemukan kecocokan.")
        print("\nSeluruh subjek:")
        for item in all_subjects:
            print(
                item.get("sub_id"),
                "-",
                item.get("title")
            )

    print("\nJumlah hasil relevan:", found)

except requests.exceptions.RequestException as error:
    print("Kesalahan koneksi:", type(error).__name__)

except (ValueError, KeyError, IndexError) as error:
    print("Kesalahan pembacaan data:", error)