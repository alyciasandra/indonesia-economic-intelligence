
import os
import requests

API_KEY = os.getenv("BPS_API_KEY")

if not API_KEY:
    raise ValueError("API Key belum tersedia.")

url = (
    "https://webapi.bps.go.id/v1/api/"
    "list/model/subject/domain/0000/key/"
    + API_KEY
)

response = requests.get(
    url,
    params={"lang": "ind", "page": 1},
    timeout=30
)

response.raise_for_status()
result = response.json()

records = result.get("data", [])
subjects = records[1] if len(records) > 1 else []

print("DAFTAR SUBJEK TERKAIT EKONOMI BPS")
print("=" * 55)

keywords = [
    "produk domestik bruto",
    "pdb",
    "pertumbuhan ekonomi",
    "inflasi",
    "tenaga kerja",
    "pengangguran",
    "industri"
]

for item in subjects:
    title = str(item.get("title", ""))
    category = str(item.get("subcat", ""))

    if any(k in title.lower() for k in keywords):
        print(
            f"SUBJECT ID: {item.get('sub_id')}"
            f"\nNAMA: {title}"
            f"\nKATEGORI: {category}"
            "\n" + "-" * 40
        )
