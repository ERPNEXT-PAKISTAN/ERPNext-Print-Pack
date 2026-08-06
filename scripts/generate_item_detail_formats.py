#!/usr/bin/env python3
"""Generate Item Detail Report print formats."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from erpnext_print_pack.doctype_profiles import PROFILES  # noqa: E402
from erpnext_print_pack.item_detail_engine import render_item_detail  # noqa: E402
from erpnext_print_pack.metadata_loader import rebuild_manifest_from_folders  # noqa: E402

FORMATS = ROOT / "erpnext_print_pack" / "print_pack" / "print_format"

VARIANTS = [
	("item_detail_classic", "Item Detail Report", "#6366f1"),
	("item_detail_professional", "Item Detail Professional", "#1e40af"),
]


def checksum(content: str) -> str:
	return hashlib.sha256(content.encode("utf-8")).hexdigest()


def main():
	profile = PROFILES["item_detail"]
	count = 0
	for slug, label, accent in VARIANTS:
		html = render_item_detail(accent=accent, title=label)
		name = "Item Detail Report" if slug == "item_detail_classic" else label
		fdir = FORMATS / slug
		fdir.mkdir(parents=True, exist_ok=True)
		meta = {
			"name": name,
			"slug": slug,
			"doc_type": "Item",
			"theme": slug,
			"layout_family": slug,
			"layout_type": "premium",
			"region": "ALL",
			"category": "stock",
			"orientation": "portrait",
			"paper_size": "A4",
			"languages": ["en"],
			"features": ["item-detail", "image", "barcode", "purchase-history"],
			"source_type": "original",
			"source_license": "MIT",
			"status": "stable",
			"checksum": checksum(html),
			"description": label,
		}
		pf = {
			"doctype": "Print Format",
			"name": name,
			"doc_type": "Item",
			"module": "Print Pack",
			"custom_format": 1,
			"print_format_type": "Jinja",
			"standard": "No",
			"disabled": 0,
			"default_print_language": "en",
			"margin_top": 8.0,
			"margin_bottom": 8.0,
			"margin_left": 10.0,
			"margin_right": 10.0,
			"page_number": "Hide",
			"css": "",
		}
		(fdir / f"{slug}.html").write_text(html, encoding="utf-8")
		(fdir / f"{slug}.json").write_text(json.dumps(pf, indent=1) + "\n", encoding="utf-8")
		(fdir / "metadata.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
		count += 1

	manifest = rebuild_manifest_from_folders()
	print(json.dumps({"generated": count, "manifest_total": manifest["total_formats"]}, indent=2))


if __name__ == "__main__":
	main()
