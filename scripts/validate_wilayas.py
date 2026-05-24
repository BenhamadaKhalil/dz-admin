"""
scripts/validate_wilayas.py
─────────────────────────────────────────────────────────────────────────────
Validates datasets/raw/wilayas.json against the Wilaya Pydantic schema.

Exit codes:
  0 — all wilayas valid
  1 — validation errors detected

Usage:
    python scripts/validate_wilayas.py [--report]

Options:
    --report   Write validation_report.json to datasets/ after validation
"""

import json
import sys
import argparse
from pathlib import Path
from typing import Any

# Allow imports from repo root
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from schemas import Wilaya
from pydantic import ValidationError

ROOT = Path(__file__).resolve().parent.parent
RAW_PATH = ROOT / "datasets" / "raw" / "wilayas.json"


def validate_wilayas(report: bool = False) -> dict[str, Any]:
    """Validate the raw wilayas dataset. Returns a result dict."""
    print("Validating wilayas dataset...")

    if not RAW_PATH.exists():
        print(f"ERROR: {RAW_PATH} not found. Did you generate the raw data?", file=sys.stderr)
        sys.exit(1)

    with open(RAW_PATH, encoding="utf-8") as f:
        data = json.load(f)

    errors: list[dict] = []
    valid: list[dict] = []

    for i, record in enumerate(data):
        try:
            w = Wilaya(**record)
            valid.append(w.model_dump())
        except ValidationError as e:
            for err in e.errors():
                errors.append({
                    "index": i,
                    "id": record.get("id", "?"),
                    "code": record.get("code", "?"),
                    "field": ".".join(str(x) for x in err["loc"]),
                    "message": err["msg"],
                    "value": err.get("input"),
                })

    # Cross-record uniqueness checks
    seen_ids: dict[int, int] = {}
    seen_codes: dict[str, int] = {}
    seen_iso: dict[str, int] = {}
    seen_slugs: dict[str, int] = {}
    capital_count = 0

    for w in valid:
        idx = w["id"]

        if w["id"] in seen_ids:
            errors.append({"type": "duplicate", "field": "id", "value": w["id"],
                           "message": f"Duplicate id={w['id']}"})
        seen_ids[w["id"]] = idx

        if w["code"] in seen_codes:
            errors.append({"type": "duplicate", "field": "code", "value": w["code"],
                           "message": f"Duplicate code='{w['code']}'"})
        seen_codes[w["code"]] = idx

        if w["iso_code"] in seen_iso:
            errors.append({"type": "duplicate", "field": "iso_code", "value": w["iso_code"],
                           "message": f"Duplicate iso_code='{w['iso_code']}'"})
        seen_iso[w["iso_code"]] = idx

        if w["slug"] in seen_slugs:
            errors.append({"type": "duplicate", "field": "slug", "value": w["slug"],
                           "message": f"Duplicate slug='{w['slug']}'"})
        seen_slugs[w["slug"]] = idx

        if w["capital"]:
            capital_count += 1

    # Exactly one capital
    if capital_count != 1:
        errors.append({
            "type": "invariant",
            "field": "capital",
            "message": f"Expected exactly 1 national capital, found {capital_count}",
        })

    # All 69 IDs present
    expected_ids = set(range(1, 70))
    found_ids = set(seen_ids.keys())
    missing = expected_ids - found_ids
    if missing:
        errors.append({
            "type": "missing",
            "field": "id",
            "message": f"Missing wilaya IDs: {sorted(missing)}",
        })
    extra = found_ids - expected_ids
    if extra:
        errors.append({
            "type": "extra",
            "field": "id",
            "message": f"Unexpected wilaya IDs: {sorted(extra)}",
        })

    result = {
        "entity": "wilaya",
        "total_records": len(data),
        "valid_count": len(valid),
        "error_count": len(errors),
        "errors": errors,
        "passed": len(errors) == 0,
    }

    # Print summary
    if errors:
        print(f"\n❌ FAILED — {len(errors)} error(s) found in {len(data)} wilaya records:\n")
        for err in errors[:20]:  # Show first 20
            print(f"  [{err.get('code', err.get('type', '?'))}] {err['field']}: {err['message']}")
        if len(errors) > 20:
            print(f"  ... and {len(errors) - 20} more.")
    else:
        print(f"✅ PASSED — {len(valid)}/{len(data)} wilayas valid.")

    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate wilaya dataset")
    parser.add_argument("--report", action="store_true", help="Write JSON report")
    args = parser.parse_args()

    result = validate_wilayas(report=args.report)

    if args.report:
        report_path = ROOT / "datasets" / "wilaya_validation.json"
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"\nReport written to {report_path}")

    sys.exit(0 if result["passed"] else 1)