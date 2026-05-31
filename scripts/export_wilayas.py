import json
import csv
import yaml
import xml.etree.ElementTree as ET
from xml.dom import minidom
import sys
from pathlib import Path

# Allow imports from repo root
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from schemas.wilaya_schema import Wilaya
from pydantic import ValidationError

ROOT = Path(__file__).resolve().parent.parent
RAW_PATH = ROOT / "datasets" / "raw" / "wilayas.json"
OUT_DIR = ROOT / "datasets" / "processed"

def export_wilayas():
    print("Loading and validating wilayas...")
    if not RAW_PATH.exists():
        print(f"ERROR: {RAW_PATH} not found.")
        sys.exit(1)

    with open(RAW_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    valid_wilayas = []
    for i, record in enumerate(data):
        try:
            w = Wilaya(**record)
            valid_wilayas.append(w)
        except ValidationError as e:
            print(f"Validation error in record {i}: {e}")
            sys.exit(1)

    print(f"Successfully validated {len(valid_wilayas)} wilayas.")

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # 1. JSON
    json_dir = OUT_DIR / "json"
    json_dir.mkdir(exist_ok=True)
    json_path = json_dir / "wilayas.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump([w.model_dump() for w in valid_wilayas], f, ensure_ascii=False, indent=2)
    print(f"Generated {json_path}")

    # 2. CSV
    csv_dir = OUT_DIR / "csv"
    csv_dir.mkdir(exist_ok=True)
    csv_path = csv_dir / "wilayas.csv"
    with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow([
            "id", "code", "iso_code", "name_ar", "name_fr", "name_en",
            "slug", "region", "capital", "capital_city", "postal_code",
            "lat", "lng", "area_km2", "population", "data_status"
        ])
        for w in valid_wilayas:
            writer.writerow([
                w.id, w.code, w.iso_code,
                w.name.ar, w.name.fr, w.name.en,
                w.slug, w.region.value, w.capital, w.capital_city, w.postal_code,
                w.coordinates.lat, w.coordinates.lng,
                w.area_km2, w.population, w.data_status.value
            ])
    print(f"Generated {csv_path}")

    # 3. SQL
    sql_dir = OUT_DIR / "sql"
    sql_dir.mkdir(exist_ok=True)
    sql_path = sql_dir / "wilayas.sql"
    with open(sql_path, "w", encoding="utf-8") as f:
        f.write("DROP TABLE IF EXISTS wilayas;\n")
        f.write('''CREATE TABLE wilayas (
    id INT PRIMARY KEY,
    code VARCHAR(2) NOT NULL,
    iso_code VARCHAR(10) NOT NULL,
    name_ar VARCHAR(100) NOT NULL,
    name_fr VARCHAR(100) NOT NULL,
    name_en VARCHAR(100) NOT NULL,
    slug VARCHAR(100) NOT NULL,
    region VARCHAR(50) NOT NULL,
    capital BOOLEAN NOT NULL,
    capital_city VARCHAR(100) NOT NULL,
    postal_code VARCHAR(5) NOT NULL,
    lat DECIMAL(9,6) NOT NULL,
    lng DECIMAL(9,6) NOT NULL,
    area_km2 INT,
    population INT,
    data_status VARCHAR(20) NOT NULL
);\n\n''')
        f.write("INSERT INTO wilayas (id, code, iso_code, name_ar, name_fr, name_en, slug, region, capital, capital_city, postal_code, lat, lng, area_km2, population, data_status) VALUES\n")

        values = []
        for w in valid_wilayas:
            name_ar = w.name.ar.replace("'", "''")
            name_fr = w.name.fr.replace("'", "''")
            name_en = w.name.en.replace("'", "''")
            slug = w.slug.replace("'", "''")
            cap_city = w.capital_city.replace("'", "''")
            area = str(w.area_km2) if w.area_km2 is not None else "NULL"
            pop = str(w.population) if w.population is not None else "NULL"
            values.append(f"({w.id}, '{w.code}', '{w.iso_code}', '{name_ar}', '{name_fr}', '{name_en}', '{slug}', '{w.region.value}', {str(w.capital).upper()}, '{cap_city}', '{w.postal_code}', {w.coordinates.lat}, {w.coordinates.lng}, {area}, {pop}, '{w.data_status.value}')")

        f.write(",\n".join(values) + ";\n")
    print(f"Generated {sql_path}")

    # 4. XML
    xml_dir = OUT_DIR / "xml"
    xml_dir.mkdir(exist_ok=True)
    xml_path = xml_dir / "wilayas.xml"
    root = ET.Element("wilayas")
    for w in valid_wilayas:
        wel = ET.SubElement(root, "wilaya")
        ET.SubElement(wel, "id").text = str(w.id)
        ET.SubElement(wel, "code").text = w.code
        ET.SubElement(wel, "iso_code").text = w.iso_code

        name_el = ET.SubElement(wel, "name")
        ET.SubElement(name_el, "ar").text = w.name.ar
        ET.SubElement(name_el, "fr").text = w.name.fr
        ET.SubElement(name_el, "en").text = w.name.en

        ET.SubElement(wel, "slug").text = w.slug
        ET.SubElement(wel, "region").text = w.region.value
        ET.SubElement(wel, "capital").text = str(w.capital).lower()
        ET.SubElement(wel, "capital_city").text = w.capital_city
        ET.SubElement(wel, "postal_code").text = w.postal_code

        coords_el = ET.SubElement(wel, "coordinates")
        ET.SubElement(coords_el, "lat").text = str(w.coordinates.lat)
        ET.SubElement(coords_el, "lng").text = str(w.coordinates.lng)

        if w.area_km2 is not None:
            ET.SubElement(wel, "area_km2").text = str(w.area_km2)
        if w.population is not None:
            ET.SubElement(wel, "population").text = str(w.population)
        ET.SubElement(wel, "data_status").text = w.data_status.value

    xml_str = minidom.parseString(ET.tostring(root, encoding="unicode")).toprettyxml(indent="  ")
    with open(xml_path, "w", encoding="utf-8") as f:
        f.write(xml_str)
    print(f"Generated {xml_path}")

    # 5. YAML
    yaml_dir = OUT_DIR / "yaml"
    yaml_dir.mkdir(exist_ok=True)
    yaml_path = yaml_dir / "wilayas.yaml"
    with open(yaml_path, "w", encoding="utf-8") as f:
        yaml.dump([w.model_dump() for w in valid_wilayas], f, allow_unicode=True, sort_keys=False)
    print(f"Generated {yaml_path}")

    print("All exports completed successfully!")

if __name__ == "__main__":
    export_wilayas()
