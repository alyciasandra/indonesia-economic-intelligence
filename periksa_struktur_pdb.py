import json
from pathlib import Path

file_path = Path("data_raw_pdb/pdb_2021_2025_raw.json")

if not file_path.exists():
    raise FileNotFoundError("File JSON PDB belum ditemukan.")

with file_path.open("r", encoding="utf-8") as file:
    records = json.load(file)

print("JUMLAH PERIODE:", len(records))

for record in records[:2]:

    print("\n" + "=" * 50)
    print("PERIODE:", record.get("period"))

    response = record.get("response", {})

    print("STATUS:", response.get("status"))
    print("KEY RESPONSE:", list(response.keys()))

    data = response.get("data")

    print("\nSTRUKTUR DATA:")

    if isinstance(data, dict):
        print("Keys:", list(data.keys()))

        for key, value in data.items():
            if isinstance(value, list):
                print(key, "| Jumlah:", len(value))
                if value:
                    print("Contoh:", value[0])
            else:
                print(key, ":", str(value)[:300])

    elif isinstance(data, list):
        print("Jumlah elemen:", len(data))
        print(json.dumps(
            data[:2],
            indent=2,
            ensure_ascii=False
        )[:3000])

    else:
        print("Data:", data)