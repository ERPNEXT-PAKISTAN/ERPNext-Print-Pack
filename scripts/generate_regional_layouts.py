#!/usr/bin/env python3
"""Generate regional & colorful layouts for sales/purchasing DocTypes."""

from __future__ import annotations

import hashlib
import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from erpnext_print_pack.doctype_profiles import PROFILES  # noqa: E402
from erpnext_print_pack.layout_engine import COMMERCIAL_CATEGORIES, format_display_name, format_slug  # noqa: E402
from erpnext_print_pack.regional_layouts import (  # noqa: E402
	COLORFUL_LAYOUT_KEYS,
	REGIONAL_CATEGORIES,
	REGIONAL_LAYOUT_REGISTRY,
	render_layout_regional,
)

FORMATS = ROOT / "erpnext_print_pack" / "print_pack" / "print_format"
MANIFEST = ROOT / "erpnext_print_pack" / "print_pack" / "manifest.json"

# re-export colorful keys from regional module

def checksum(content: str) -> str:
	return hashlib.sha256(content.encode("utf-8")).hexdigest()


def write_format(profile, layout_key: str) -> dict:
	meta_info = REGIONAL_LAYOUT_REGISTRY[layout_key]
	name = f"{meta_info['label']} {profile.title}"
	slug = format_slug(profile, layout_key)
	fdir = FORMATS / slug
	fdir.mkdir(parents=True, exist_ok=True)
	html = render_layout_regional(profile, layout_key)
	meta = {
		"name": name,
		"slug": slug,
		"doc_type": profile.doc_type,
		"theme": layout_key,
		"layout_family": layout_key,
		"layout_type": "colorful" if layout_key in COLORFUL_LAYOUT_KEYS else "regional",
		"region": meta_info.get("region", "ALL"),
		"sector": "all",
		"category": profile.category,
		"orientation": "portrait",
		"paper_size": "A4",
		"languages": ["en", "ar"] if layout_key in ("saudi_zatca", "gulf_gold", "uae_vat") else ["en"],
		"features": ["premium-layout", layout_key, meta_info.get("layout_type", "regional")],
		"source_type": "original",
		"source_license": "MIT",
		"status": "stable",
		"checksum": checksum(html),
		"description": meta_info["description"],
	}
	pf = {
		"doctype": "Print Format",
		"name": name,
		"doc_type": profile.doc_type,
		"module": "Print Pack",
		"custom_format": 1,
		"print_format_type": "Jinja",
		"standard": "No",
		"disabled": 0,
		"default_print_language": "en",
		"margin_top": 10.0,
		"margin_bottom": 10.0,
		"margin_left": 10.0,
		"margin_right": 10.0,
		"page_number": "Hide",
		"css": "",
	}
	(fdir / f"{slug}.html").write_text(html, encoding="utf-8")
	(fdir / f"{slug}.json").write_text(json.dumps(pf, indent=1) + "\n", encoding="utf-8")
	(fdir / "metadata.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
	return meta


def main():
	entries = []
	for profile in PROFILES.values():
		if profile.category not in COMMERCIAL_CATEGORIES:
			continue
		for layout_key in REGIONAL_LAYOUT_REGISTRY:
			# Regional tax layouts only on sales/purchasing
			if layout_key not in COLORFUL_LAYOUT_KEYS and profile.category not in REGIONAL_CATEGORIES:
				continue
			entries.append(write_format(profile, layout_key))
	print(json.dumps({"generated": len(entries)}, indent=2))


if __name__ == "__main__":
	main()
