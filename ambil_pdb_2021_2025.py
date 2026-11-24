import os
import requests
import json
import re
from pathlib import Path

# ==========================================
# 1. KONFIGURASI
# ==========================================

API_KEY = os.getenv("BPS_API_KEY")
VARIABLE_ID = 104
DOMAIN = "0000"

if not API_KEY:
    raise ValueError("API Key BPS belum tersedia.")

BASE_URL = "https://webapi.bps.go.id/v1/api/list"

# ==========================================
# 2. MENCARI SELURUH PERIODE PDB
# ==========================================

print("MENGAMBIL DAFTAR PERIODE PDB...")

period_url = (
    BASE_URL
    + "/model/th/domain/"
    + DOMAIN
    + "/var/"
    + str(VARIABLE_ID)
    + "/key/"
    + API_KEY
)

periods = []
page = 1
total_pages = 1

while page <= total_pages:

    response = requests.get(
        period_url,
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

# ==========================================
# 3. MEMILIH PERIODE 2021-2025
# ==========================================

selected_periods = []

for item in periods:

    label = str(item.get("th", ""))
    match = re.search(r"20\d{2}", label)

    if match:
        year = int(match.group())

        if 2021 <= year <= 2025:
            selected_periods.append(item)

print("Jumlah periode terpilih:", len(selected_periods))

# ==========================================
# 4. MENGAMBIL DATA AKTUAL
# ==========================================

all_data = []

for period in selected_periods:

    period_id = period.get("th_id")
    period_name = period.get("th")

    data_url = (
        BASE_URL
        + "/model/data/domain/"
        + DOMAIN
        + "/var/"
        + str(VARIABLE_ID)
        + "/th/"
        + str(period_id)
        + "/key/"
        + API_KEY
    )

    response = requests.get(
        data_url,
        params={"lang": "ind"},
        timeout=30
    )

    response.raise_for_status()

    result = response.json()

    all_data.append({
        "period_id": period_id,
        "period": period_name,
        "response": result
    })

    print("Berhasil:", period_name)

# ==========================================
# 5. MENYIMPAN DATA RAW JSON
# ==========================================

output_dir = Path("data_raw_pdb")
output_dir.mkdir(parents=True, exist_ok=True)

output_file = output_dir / "pdb_2021_2025_raw.json"

with output_file.open("w", encoding="utf-8") as file:
    json.dump(
        all_data,
        file,
        indent=4,
        ensure_ascii=False
    )

print("\n================================")
print("PENGAMBILAN DATA SELESAI")
print("Jumlah periode:", len(all_data))
print("File:", output_file)
print("================================")

if all_data:
    print("\nSTRUKTUR RESPONS DATA PERTAMA:")
    print(json.dumps(
        all_data[0]["response"],
        indent=2,
        ensure_ascii=False
    )[:4000])