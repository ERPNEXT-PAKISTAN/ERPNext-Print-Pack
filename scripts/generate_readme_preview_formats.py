#!/usr/bin/env python3
"""Generate README-preview print formats (ZATCA Tax Invoice & Regional Tax Invoice)."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from erpnext_print_pack.doctype_profiles import PROFILES  # noqa: E402
from erpnext_print_pack.layout_engine import COMMERCIAL_CATEGORIES  # noqa: E402
from erpnext_print_pack.metadata_loader import rebuild_manifest_from_folders  # noqa: E402
from erpnext_print_pack.readme_preview_engine import (  # noqa: E402
	PREVIEW_LAYOUTS,
	format_name,
	format_slug,
	render_preview,
)

FORMATS = ROOT / "erpnext_print_pack" / "print_pack" / "print_format"


def checksum(content: str) -> str:
	return hashlib.sha256(content.encode("utf-8")).hexdigest()


def write_format(profile, layout_key: str) -> None:
	slug = format_slug(profile, layout_key)
	name = format_name(profile, layout_key)
	meta_info = PREVIEW_LAYOUTS[layout_key]
	html = render_preview(profile, layout_key)
	fdir = FORMATS / slug
	fdir.mkdir(parents=True, exist_ok=True)
	meta = {
		"name": name,
		"slug": slug,
		"doc_type": profile.doc_type,
		"theme": layout_key,
		"layout_family": layout_key,
		"layout_type": meta_info["layout_type"],
		"region": meta_info["region"],
		"category": profile.category,
		"orientation": "portrait",
		"paper_size": "A4",
		"languages": ["en", "ar"] if layout_key == "readme_zatca_tax" else ["en"],
		"features": ["readme-preview", layout_key, "premium-layout"],
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


def main():
	count = 0
	for profile in PROFILES.values():
		if profile.category not in COMMERCIAL_CATEGORIES:
			continue
		if not profile.has_items:
			continue
		for layout_key in PREVIEW_LAYOUTS:
			write_format(profile, layout_key)
			count += 1
	manifest = rebuild_manifest_from_folders()
	print(json.dumps({"generated": count, "manifest_total": manifest["total_formats"]}, indent=2))


if __name__ == "__main__":
	main()
