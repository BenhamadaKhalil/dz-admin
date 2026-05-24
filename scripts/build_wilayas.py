import json
from slugify import slugify

with open("datasets/raw/wilayas.json", "r", encoding="utf-8") as f:
    data = json.load(f)

processed = []

for item in data:
    processed.append({
        "id": item["id"],
        "code": item["code"],

        "name": {
            "ar": item["name_ar"],
            "fr": item["name_fr"],
            "en": item["name_en"]
        },

        "slug": slugify(item["name_en"])
    })

with open("datasets/processed/wilayas.json", "w", encoding="utf-8") as f:
    json.dump(processed, f, ensure_ascii=False, indent=2)

print("Build complete")