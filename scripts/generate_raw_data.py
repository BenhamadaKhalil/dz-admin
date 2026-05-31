"""
scripts/generate_raw_data.py
─────────────────────────────────────────────────────────────────────────────
ONE-TIME migration script: transforms the legacy datasets/raw/wilayas.json (58 wilayas,
flat name_ar/fr/en schema) into the canonical nested-name format and writes:

  datasets/raw/dairas.json
  datasets/raw/communes.json

Also appends stub daira/commune records for the 11 new wilayas (59–69) created
under Loi 26-06 with the best available geographic data.

Run from the repo root:
    python scripts/generate_raw_data.py

IMPORTANT: Do NOT manually edit the output files. Re-run this script if the
source data changes, then validate with:
    python scripts/validate_all.py
"""

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "datasets" / "raw" / "wilayas.json"
OUT_DAIRAS = ROOT / "datasets" / "raw" / "dairas.json"
OUT_COMMUNES = ROOT / "datasets" / "raw" / "communes.json"


# ── Helpers ──────────────────────────────────────────────────────────────────

def slugify(text: str) -> str:
    """Convert any string to a URL-safe ASCII slug."""
    import unicodedata
    # Normalize unicode → ASCII approximation
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = text.strip("-")
    return text or "unknown"


def pad(n: int, width: int) -> str:
    return str(n).zfill(width)



def generate_datasets() -> None:
    print("=" * 60)
    print("dz-admin: generating canonical dairas.json + communes.json")
    print("=" * 60)

    # Load legacy source
    if not SOURCE.exists():
        print(f"ERROR: Source file not found: {SOURCE}", file=sys.stderr)
        sys.exit(1)

    with open(SOURCE, encoding="utf-8") as f:
        source_data = json.load(f)

    legacy_wilayas = source_data["wilayas"]

    dairas: list[dict] = []
    communes: list[dict] = []
    daira_id = 1
    commune_id = 1

    # ── Process legacy wilayas ────────────────────────────────────────────
    print(f"\nProcessing {len(legacy_wilayas)} legacy wilayas from datasets/raw/wilayas.json...")

    for wl in legacy_wilayas:
        wl_code = wl["code"]  # "01" … "58"
        wl_id = int(wl_code)

        for d_seq, d in enumerate(wl.get("dairas", []), start=1):
            d_code = f"{wl_code}{pad(d_seq, 2)}"
            d_slug = slugify(d["name_en"])

            daira_rec = {
                "id": daira_id,
                "code": d_code,
                "wilaya_id": wl_id,
                "wilaya_code": wl_code,
                "name": {
                    "ar": d["name_ar"],
                    "fr": d["name_fr"],
                    "en": d["name_en"],
                },
                "slug": f"{slugify(wl['name_en'])}-{d_slug}",
            }
            dairas.append(daira_rec)

            current_daira_id = daira_id
            daira_id += 1

            for c_seq, c in enumerate(d.get("communes", []), start=1):
                c_code = f"{d_code}{pad(c_seq, 2)}"
                c_slug = slugify(c["name_en"])

                coords = None
                if c.get("lat") is not None and c.get("lon") is not None:
                    coords = {"lat": c["lat"], "lng": c["lon"]}

                commune_rec = {
                    "id": commune_id,
                    "code": c_code,
                    "daira_id": current_daira_id,
                    "daira_code": d_code,
                    "wilaya_id": wl_id,
                    "wilaya_code": wl_code,
                    "name": {
                        "ar": c["name_ar"],
                        "fr": c["name_fr"],
                        "en": c["name_en"],
                    },
                    "slug": f"{slugify(wl['name_en'])}-{d_slug}-{c_slug}",
                    "postal_code": c.get("postal_code", f"{wl_code}000"),
                    "coordinates": coords,
                }
                communes.append(commune_rec)
                commune_id += 1

    print(f"  Legacy wilayas 01–58: {daira_id - 1} daïras, {commune_id - 1} communes generated.")

    # ── Process 11 new wilayas (59–69) ───────────────────────────────────────
    print(f"\nProcessing {len(NEW_WILAYAS)} new wilayas (Loi 26-06)...")

    for wl_data in NEW_WILAYAS:
        wl_code = wl_data["code"]
        wl_id = wl_data["id"]
        wl_en = wl_data["dairas"][0]["name"]["en"]

        for d_seq, d in enumerate(wl_data["dairas"], start=1):
            d_code = f"{wl_code}{pad(d_seq, 2)}"
            d_slug = slugify(d["name"]["en"])

            daira_rec = {
                "id": daira_id,
                "code": d_code,
                "wilaya_id": wl_id,
                "wilaya_code": wl_code,
                "name": d["name"],
                "slug": f"{slugify(wl_en)}-{d_slug}",
            }
            dairas.append(daira_rec)

            current_daira_id = daira_id
            daira_id += 1

            for c_seq, c in enumerate(d["communes"], start=1):
                c_code = f"{d_code}{pad(c_seq, 2)}"
                c_slug = slugify(c["name"]["en"])

                coords = None
                if c.get("lat") is not None:
                    coords = {"lat": c["lat"], "lng": c["lng"]}

                commune_rec = {
                    "id": commune_id,
                    "code": c_code,
                    "daira_id": current_daira_id,
                    "daira_code": d_code,
                    "wilaya_id": wl_id,
                    "wilaya_code": wl_code,
                    "name": c["name"],
                    "slug": f"{slugify(wl_en)}-{d_slug}-{c_slug}",
                    "postal_code": c.get("postal_code", f"{wl_code}000"),
                    "coordinates": coords,
                }
                communes.append(commune_rec)
                commune_id += 1

    total_dairas = daira_id - 1
    total_communes = commune_id - 1
    print(f"  New wilayas 59–69 added.")
    print(f"\nTotals:")
    print(f"  Daïras:   {total_dairas}")
    print(f"  Communes: {total_communes}")

    # ── Write output ──────────────────────────────────────────────────────────
    OUT_DAIRAS.parent.mkdir(parents=True, exist_ok=True)

    with open(OUT_DAIRAS, "w", encoding="utf-8") as f:
        json.dump(dairas, f, ensure_ascii=False, indent=2)
    print(f"\n✓ Written: {OUT_DAIRAS}")

    with open(OUT_COMMUNES, "w", encoding="utf-8") as f:
        json.dump(communes, f, ensure_ascii=False, indent=2)
    print(f"✓ Written: {OUT_COMMUNES}")

    # ── Dataset metadata ──────────────────────────────────────────────────────
    metadata = {
        "version": "2.0.0",
        "description": "Algeria administrative divisions — 69 wilayas, daïras, communes",
        "legislation": "Updated for Loi 26-06 (69 wilayas)",
        "languages": ["ar", "fr", "en"],
        "counts": {
            "wilayas": 69,
            "wilayas_complete": 58,
            "wilayas_partial": 11,
            "dairas": total_dairas,
            "communes": total_communes,
        },
        "schema_version": "2.0",
        "source": "ONS Algeria / official administrative records / Loi 26-06",
        "last_updated": "2026-05-24",
        "maintainers": ["dz-admin contributors"],
        "license": "Open Data Commons Attribution License (ODC-By)",
    }

    meta_path = ROOT / "datasets" / "metadata.json"
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    print(f"✓ Written: {meta_path}")

    print("\n✅ Generation complete. Run 'python scripts/validate_all.py' to verify.")


if __name__ == "__main__":
    generate_datasets()
