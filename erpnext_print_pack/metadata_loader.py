"""Load print format metadata from format folders and manifest."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parent
FORMAT_ROOT = APP_ROOT / "print_pack" / "print_format"
MANIFEST_PATH = APP_ROOT / "print_pack" / "manifest.json"

REGIONAL_NAME_MARKERS = (
	"Saudi ZATCA",
	"UAE VAT",
	"UAE E-Invoice",
	"ZATCA E-Invoice",
	"ZATCA Tax Invoice",
	"Regional Tax Invoice",
	"Pakistan FBR",
	"Pakistan E-Invoice",
	"FBR Pakistan",
	"India GST",
	"USA Commercial",
	"Gulf Gold",
)
COLORFUL_NAME_MARKERS = (
	"Gradient Vivid",
	"Emerald Fresh",
	"Crimson Shop",
	"Ocean Vibrant",
)
PROFORMA_MARKERS = ("Proforma", "proforma")


@lru_cache(maxsize=1)
def load_all_metadata() -> dict[str, dict]:
	by_name: dict[str, dict] = {}
	if MANIFEST_PATH.exists():
		data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
		for item in data.get("formats", []):
			if item.get("name"):
				by_name[item["name"]] = item
	if FORMAT_ROOT.exists():
		for meta_path in FORMAT_ROOT.glob("*/metadata.json"):
			try:
				item = json.loads(meta_path.read_text(encoding="utf-8"))
			except Exception:
				continue
			name = item.get("name")
			if name:
				by_name[name] = {**by_name.get(name, {}), **item}
	return by_name


def enrich_format_record(fmt: dict) -> dict:
	meta = load_all_metadata().get(fmt.get("name") or "", {})
	fmt["theme"] = meta.get("theme", fmt.get("theme", ""))
	fmt["status"] = meta.get("status", "stable" if not fmt.get("disabled") else "draft")
	fmt["category"] = meta.get("category", "")
	fmt["layout_family"] = meta.get("layout_family", "")
	fmt["layout_type"] = meta.get("layout_type", _infer_layout_type(fmt.get("name") or "", meta))
	fmt["region"] = meta.get("region", _infer_region(fmt.get("name") or "", meta))
	fmt["description"] = meta.get("description", "")
	fmt["is_proforma"] = bool(meta.get("is_proforma")) or any(m in (fmt.get("name") or "") for m in PROFORMA_MARKERS)
	fmt["is_premium"] = bool(fmt["layout_family"]) or fmt["layout_type"] in ("regional", "colorful", "specimen", "proforma") or _is_premium_name(fmt.get("name") or "")
	fmt["is_legacy"] = not fmt["is_premium"] and fmt.get("name") not in ("Sales Invoice Format",)
	return fmt


def _infer_layout_type(name: str, meta: dict) -> str:
	if meta.get("layout_type"):
		return meta["layout_type"]
	if any(m in name for m in PROFORMA_MARKERS):
		return "proforma"
	if any(m in name for m in COLORFUL_NAME_MARKERS):
		return "colorful"
	if any(m in name for m in REGIONAL_NAME_MARKERS):
		return "regional"
	if "Specimen" in name or "E-Invoice" in name:
		return "specimen"
	if "Thermal" in name:
		return "thermal"
	return ""


def _infer_region(name: str, meta: dict) -> str:
	if meta.get("region"):
		return meta["region"]
	if any(x in name for x in ("Saudi", "ZATCA")):
		return "SA"
	if "UAE" in name:
		return "AE"
	if any(x in name for x in ("Pakistan", "FBR Pakistan")):
		return "PK"
	if "India" in name:
		return "IN"
	if "USA" in name:
		return "US"
	if "Gulf" in name:
		return "ME"
	return ""


def _is_premium_name(name: str) -> bool:
	markers = (
		"E-Invoice Specimen",
		"Dark Header Pro",
		"Vertex Classic",
		"Zoho Professional",
		"Tabler Business",
		"SparkSuite",
		"Proforma",
	) + REGIONAL_NAME_MARKERS + COLORFUL_NAME_MARKERS
	return any(m in name for m in markers)


def rebuild_manifest_from_folders() -> dict:
	entries = []
	for meta_path in sorted(FORMAT_ROOT.glob("*/metadata.json")):
		try:
			entries.append(json.loads(meta_path.read_text(encoding="utf-8")))
		except Exception:
			continue
	manifest = {
		"generated_on": str(__import__("datetime").date.today()),
		"total_formats": len(entries),
		"formats": entries,
	}
	MANIFEST_PATH.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
	load_all_metadata.cache_clear()
	return manifest
