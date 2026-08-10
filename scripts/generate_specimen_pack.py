#!/usr/bin/env python3
"""Generate SA/UAE specimens, proforma, and thermal formats across DocTypes."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from erpnext_print_pack.doctype_profiles import PROFILES  # noqa: E402
from erpnext_print_pack.metadata_loader import rebuild_manifest_from_folders  # noqa: E402
from erpnext_print_pack.specimen_engine import (  # noqa: E402
	PROFORMA_DOCTYPES,
	SPECIMEN_DOCTYPES,
	SPECIMEN_PACKS,
	THERMAL_DOCTYPES,
	THERMAL_PACKS,
	format_name,
	format_slug,
	render_specimen,
)

FORMATS = ROOT / "erpnext_print_pack" / "print_pack" / "print_format"


def checksum(content: str) -> str:
	return hashlib.sha256(content.encode("utf-8")).hexdigest()


def write_format(profile, pack_key: str, pack: dict, html: str, thermal: bool = False) -> None:
	slug = format_slug(profile, pack_key)
	name = format_name(pack["label"], profile)
	fdir = FORMATS / slug
	fdir.mkdir(parents=True, exist_ok=True)
	layout_type = "thermal" if thermal else ("proforma" if pack.get("is_proforma") else "specimen")
	meta = {
		"name": name,
		"slug": slug,
		"doc_type": profile.doc_type,
		"theme": pack_key,
		"layout_family": pack_key,
		"layout_type": layout_type,
		"region": pack.get("region", "ALL"),
		"is_proforma": bool(pack.get("is_proforma")),
		"category": profile.category,
		"orientation": "portrait",
		"paper_size": "80mm" if thermal else "A4",
		"languages": ["en", "ar"] if pack.get("region") in ("SA", "AE") else ["en"],
		"features": ["specimen", pack_key, layout_type],
		"source_type": "original",
		"source_license": "MIT",
		"attribution_required": False,
		"erpnext_versions": ["15", "16"],
		"status": "stable",
		"checksum": checksum(html),
		"description": pack["label"],
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
		"margin_top": 4.0 if thermal else 8.0,
		"margin_bottom": 4.0 if thermal else 8.0,
		"margin_left": 4.0 if thermal else 10.0,
		"margin_right": 4.0 if thermal else 10.0,
		"page_number": "Hide",
		"css": "",
	}
	(fdir / f"{slug}.html").write_text(html, encoding="utf-8")
	(fdir / f"{slug}.json").write_text(json.dumps(pf, indent=1) + "\n", encoding="utf-8")
	(fdir / "metadata.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")


def main():
	count = 0
	for profile in PROFILES.values():
		# SA/UAE full specimens
		if profile.doc_type in SPECIMEN_DOCTYPES:
			for key in ("zatca_specimen", "uae_specimen"):
				html = render_specimen(profile, key)
				write_format(profile, key, SPECIMEN_PACKS[key], html)
				count += 1
		# Proforma styles
		if profile.doc_type in PROFORMA_DOCTYPES:
			for key in ("proforma_zatca", "proforma_uae", "proforma_modern", "proforma_classic"):
				html = render_specimen(profile, key)
				write_format(profile, key, SPECIMEN_PACKS[key], html)
				count += 1
		# Thermal POS / receipts / payment slips
		if profile.doc_type in THERMAL_DOCTYPES:
			for key in ("zatca_thermal", "uae_thermal"):
				html = render_specimen(profile, key, thermal=True)
				write_format(profile, key, THERMAL_PACKS[key], html, thermal=True)
				count += 1

	manifest = rebuild_manifest_from_folders()
	print(json.dumps({"generated": count, "manifest_total": manifest["total_formats"]}, indent=2))


if __name__ == "__main__":
	main()
