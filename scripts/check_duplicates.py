import json

with open("datasets/raw/wilayas.json", "r", encoding="utf-8") as f:
    data = json.load(f)

codes = set()

for item in data:
    if item["code"] in codes:
        raise ValueError(f"Duplicate code: {item['code']}")

    codes.add(item["code"])

print("No duplicates found")