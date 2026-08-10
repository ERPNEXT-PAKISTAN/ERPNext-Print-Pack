#!/usr/bin/env python3
"""Generate premium Google-style layouts for all commercial DocTypes."""

from __future__ import annotations

import hashlib
import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from erpnext_print_pack.doctype_profiles import PROFILES  # noqa: E402
from erpnext_print_pack.layout_engine import (  # noqa: E402
	COMMERCIAL_CATEGORIES,
	LAYOUT_REGISTRY,
	format_display_name,
	format_slug,
	render_layout,
)

FORMATS = ROOT / "erpnext_print_pack" / "print_pack" / "print_format"
MANIFEST = ROOT / "erpnext_print_pack" / "print_pack" / "manifest.json"
PRESERVE = {"sales_invoice_bilingual_tax"}


def checksum(content: str) -> str:
	return hashlib.sha256(content.encode("utf-8")).hexdigest()


def write_format(profile, layout_key: str, status: str = "stable") -> dict | None:
	slug = format_slug(profile, layout_key)
	if slug in PRESERVE:
		return None
	name = format_display_name(profile, layout_key)
	fdir = FORMATS / slug
	fdir.mkdir(parents=True, exist_ok=True)
	html = render_layout(profile, layout_key)
	layout_meta = LAYOUT_REGISTRY[layout_key]

	meta = {
		"name": name,
		"slug": slug,
		"doc_type": profile.doc_type,
		"theme": layout_key,
		"layout_family": layout_key,
		"sector": "all",
		"category": profile.category,
		"orientation": "portrait",
		"paper_size": "A4",
		"languages": ["en"],
		"features": ["premium-layout", layout_key, "field-rich"],
		"source_type": "original",
		"source_license": "MIT",
		"attribution_required": False,
		"erpnext_versions": ["15", "16"],
		"status": status,
		"checksum": checksum(html),
		"description": layout_meta["description"],
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


def rebuild_manifest(entries: list[dict]):
	existing = []
	if MANIFEST.exists():
		data = json.loads(MANIFEST.read_text(encoding="utf-8"))
		existing = data.get("formats", [])
	# Keep legacy theme formats; replace prior premium layout entries
	layout_suffixes = tuple(f"_{k}" for k in LAYOUT_REGISTRY)
	kept = [f for f in existing if not (f.get("slug") or "").endswith(layout_suffixes)]
	merged = kept + entries
	manifest = {
		"generated_on": str(date.today()),
		"premium_layouts": len(entries),
		"total_formats": len(merged),
		"layout_families": list(LAYOUT_REGISTRY.keys()),
		"formats": merged,
	}
	MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
	return manifest


def main():
	entries = []
	count = 0
	for profile in PROFILES.values():
		if profile.category not in COMMERCIAL_CATEGORIES:
			continue
		for layout_key in LAYOUT_REGISTRY:
			meta = write_format(profile, layout_key, status="stable")
			if meta:
				entries.append(meta)
				count += 1
	manifest = rebuild_manifest(entries)
	print(json.dumps({"generated": count, "layout_families": len(LAYOUT_REGISTRY), "manifest_total": manifest["total_formats"]}, indent=2))


if __name__ == "__main__":
	main()
