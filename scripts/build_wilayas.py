import json

with open("datasets/raw/wilayas.json", "r", encoding="utf-8") as f:
    data = json.load(f)

with open("datasets/processed/wilayas.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Wilaya build complete")