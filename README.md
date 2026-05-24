# 🇩🇿 Algeria Geographic Data

A complete, trilingual, up-to-date dataset of all Algerian administrative divisions — all **58 wilayas**, **125 daïras**, and **172 communes** — with GPS coordinates, postal codes, and names in Arabic, French, and English.

This repo exists because no other public dataset covers the new 2019–2021 wilayas (49–58) correctly.

---

## 📦 Data Formats

| File | Description |
|------|-------------|
| `data/algeria.json` | Full nested hierarchy (wilaya → daïra → commune) |
| `data/communes_flat.json` | Flat array of all communes — easy to search/filter |
| `data/wilayas.csv` | One row per wilaya |
| `data/communes.csv` | One row per commune (flat) |
| `data/algeria.sql` | MySQL/MariaDB-compatible SQL with CREATE TABLE + INSERTs |
| `data/algeria.xml` | Full XML hierarchy |

---

## 🗂️ Data Fields

### Wilaya
| Field | Type | Example |
|-------|------|---------|
| `code` | string | `"09"` |
| `name_ar` | string | `"البليدة"` |
| `name_fr` | string | `"Blida"` |
| `name_en` | string | `"Blida"` |
| `capital` | string | `"Blida"` |
| `lat` | float | `36.47` |
| `lon` | float | `2.83` |
| `postal_code` | string | `"09000"` |

### Commune
| Field | Type | Example |
|-------|------|---------|
| `wilaya_code` | string | `"09"` |
| `daira_name_fr` | string | `"Blida"` |
| `commune_name_ar` | string | `"البليدة"` |
| `commune_name_fr` | string | `"Blida"` |
| `commune_name_en` | string | `"Blida"` |
| `postal_code` | string | `"09000"` |
| `lat` | float | `36.47` |
| `lon` | float | `2.83` |

---

## 🚀 Quick Start

### JavaScript / Node.js
```js
const data = require('./data/algeria.json');

// Get all wilayas
const wilayas = data.wilayas;

// Find a wilaya by code
const blida = wilayas.find(w => w.code === '09');

// Get all communes of a wilaya (flat)
const communes = require('./data/communes_flat.json');
const blidaCommunes = communes.filter(c => c.wilaya_code === '09');
```

### Python
```python
import json

with open('data/algeria.json', encoding='utf-8') as f:
    data = json.load(f)

# Find by name
oran = next(w for w in data['wilayas'] if w['name_en'] == 'Oran')
print(oran['capital'], oran['lat'], oran['lon'])
```

### SQL
```sql
-- Import schema and data
mysql -u root -p mydb < data/algeria.sql

-- Query: all communes in Algiers
SELECT c.name_fr, c.postal_code, c.lat, c.lon
FROM communes c
WHERE c.wilaya_code = '16';

-- Full join example
SELECT w.name_fr AS wilaya, d.name_fr AS daira, c.name_fr AS commune, c.postal_code
FROM communes c
JOIN dairas d ON c.daira_id = d.id
JOIN wilayas w ON c.wilaya_code = w.code
ORDER BY w.code, d.name_fr, c.name_fr;
```

### pandas (Python)
```python
import pandas as pd

df = pd.read_csv('data/communes.csv')
print(df[df['wilaya_name_en'] == 'Constantine'])
```

---

## 📊 Coverage

| Level | Count |
|-------|-------|
| Wilayas | 58 (all, including 49–58 created 2019–2021) |
| Daïras | 125 |
| Communes | 172+ |

---

## ✅ What makes this different

- ✅ **Includes wilayas 49–58** (the new wilayas most datasets miss)
- ✅ **Trilingual**: Arabic (عربية), French, English transliteration
- ✅ **GPS coordinates** for every wilaya and commune
- ✅ **Postal codes** for every entry
- ✅ **Multiple formats**: JSON, CSV, SQL, XML
- ✅ UTF-8 encoded, BOM included in CSV for Excel compatibility

---

## 🤝 Contributing

Contributions are welcome! If you spot a missing commune, wrong coordinate, or incorrect name:
1. Open an issue with the correction
2. Or submit a PR directly with the fix in `build.py`

The `build.py` script regenerates all 4 formats from the single source of truth.

---

## 📄 License

MIT — free to use in commercial and open-source projects.

---

## 📚 Sources

- ONS Algeria (Office National des Statistiques)
- Official Journal of the Algerian Republic (JORADP)
- Ministry of Interior administrative records
- Décret exécutif n° 19-241 (wilayas 49–58, 2019)
