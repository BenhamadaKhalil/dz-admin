# dz-admin 🇩🇿

**dz-admin** is a modern, comprehensive, and strongly-typed dataset and API for Algerian administrative divisions. Updated to reflect **Loi 26-06**, this repository contains authoritative data for all **69 Wilayas**, as well as their Daïras and Communes.

Whether you need a quick JSON file for a frontend project, a SQL dump to initialize your database, or Pydantic models for your Python backend, `dz-admin` has you covered.

---

## 🌟 Features

- **Up-to-date (2026/2027)**: Fully supports all 69 wilayas, including the newly formed ones (Wilayas 59–69).
- **Multilingual Support**: Arabic (`ar`), French (`fr`), and English (`en`) localized names for every administrative unit.
- **Multiple Export Formats**: The dataset is pre-generated in JSON, CSV, SQL, XML, and YAML formats.
- **Strongly Typed**: Python schemas are built using Pydantic for robust data validation.
- **Rich Metadata**: Includes ISO 3166-2 codes, postal codes, geographical coordinates (lat/lng), area (km²), population data, and region categorization.
- **TypeScript SDK**: A dedicated SDK is available in the `packages/typescript` directory for frontend/Node.js integration.

---

## 📁 Repository Structure

```text
dz-admin/
├── datasets/
│   ├── raw/             # Authoritative source data (wilayas.json, dairas.json, communes.json)
│   └── processed/       # Generated data in multiple formats ready for production
│       ├── json/        # JSON exports
│       ├── csv/         # CSV exports
│       ├── sql/         # SQL database seeds
│       ├── xml/         # XML exports
│       └── yaml/        # YAML exports
├── schemas/             # Pydantic schema models (wilaya_schema.py, daira_schema.py, commune_schema.py)
├── scripts/             # Python automation and export scripts
│   ├── export_wilayas.py     # Generates the processed formats from raw data
│   ├── validate_wilayas.py   # Validates the dataset against Pydantic schemas
│   └── generate_raw_data.py  # Data migration tool for generating raw datasets
├── packages/            # SDKs for various languages (e.g., TypeScript)
├── apps/                # Related APIs and demo applications
└── tests/               # Test suites
```

---

## 🚀 How to Use the Datasets

If you just need the data, simply head over to `datasets/processed/` and grab the format that best suits your project:
- **Web Developers**: Use `datasets/processed/json/wilayas.json`.
- **Database Admins**: Run `datasets/processed/sql/wilayas.sql` to instantly seed your database.
- **Data Scientists**: Import `datasets/processed/csv/wilayas.csv`.

---

## 🛠️ Working with the Codebase

If you wish to modify the data or generate the files yourself, `dz-admin` provides Python scripts to manage the workflow.

### 1. Requirements

Ensure you have Python 3.10+ installed and install the required dependencies:
```bash
pip install pydantic pyyaml
```

### 2. The Data Pipeline

The central authoritative data lives in `datasets/raw/`. 

To ensure the integrity of the data, `dz-admin` relies on strictly typed Pydantic models (located in the `schemas/` directory).

#### Validate the data
If you make changes to `datasets/raw/wilayas.json`, you must validate it:
```bash
python scripts/validate_wilayas.py
```
*(You can also use the `--report` flag to output a detailed JSON validation report).*

#### Export the formats
Once the data is validated, you can regenerate the processed files (JSON, CSV, SQL, XML, YAML) inside the `datasets/processed/` folder:
```bash
python scripts/export_wilayas.py
```

---

## 🏗️ Pydantic Schemas Overview

The underlying data model ensures absolute correctness. For instance, the Wilaya schema validates:
- `id` is between 1 and 69.
- `iso_code` rigorously matches the `DZ-XX` standard.
- Exactly one wilaya is marked as the national capital.
- Only safe, lowercased `slugs` are permitted.

```python
from schemas import Wilaya

# Example usage of the schema
algiers = Wilaya(
    id=16,
    code="16",
    iso_code="DZ-16",
    name={"ar": "الجزائر", "fr": "Alger", "en": "Algiers"},
    slug="algiers",
    region="North-Center",
    capital=True,
    capital_city="Algiers",
    postal_code="16000",
    coordinates={"lat": 36.7538, "lng": 3.0588},
    data_status="complete"
)
```

---

## 📜 License

This project is licensed under the **Open Data Commons Attribution License (ODC-By)**. See the `LICENSE` file for details.