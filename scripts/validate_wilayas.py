import json
from schemas.wilaya_schema import Wilaya

with open("datasets/raw/wilayas.json", "r", encoding="utf-8") as f:
    data = json.load(f)

validated = []

for item in data:
    validated.append(Wilaya(**item).dict())

print("Validation successful")
print(validated)