import os
import requests

API_KEY = os.getenv("BPS_API_KEY")

if not API_KEY:
    raise ValueError("API Key belum tersedia.")

url = (
    "https://webapi.bps.go.id/v1/api/"
    "list/model/subject/lang/ind/key/"
    + API_KEY
)

response = requests.get(url, timeout=30)
response.raise_for_status()

result = response.json()

print("STATUS:", result.get("status"))
print("\nSUBJEK STATISTIK TERKAIT EKONOMI\n")

# Mengambil daftar subjek
records = result.get("data", [])

subjects = []

for group in records:
    if isinstance(group, list):
        subjects.extend(group)

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