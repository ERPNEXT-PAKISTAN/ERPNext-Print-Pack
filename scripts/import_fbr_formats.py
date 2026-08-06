#!/usr/bin/env python3
"""Copy FBR Integration sales invoice print formats into Print Pack with new names."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from erpnext_print_pack.metadata_loader import rebuild_manifest_from_folders  # noqa: E402
from erpnext_print_pack.print_snippets import FBR_DI_LOGO  # noqa: E402

FBR_FIXTURE = ROOT.parent / "fbr_integration" / "fbr_integration" / "fixtures" / "print_format.json"
FORMATS_DIR = ROOT / "erpnext_print_pack" / "print_pack" / "print_format"

SOURCE_MAP = [
	("Sales Invoice Tax", "FBR Pakistan-1 Sales Invoice", "sales_invoice_fbr_pakistan_1"),
	("FBR Sales Invoice", "FBR Pakistan-2 Sales Invoice", "sales_invoice_fbr_pakistan_2"),
	("FBR Letterhead-2", "FBR Pakistan-3 Sales Invoice", "sales_invoice_fbr_pakistan_3"),
]


def checksum(content: str) -> str:
	return hashlib.sha256(content.encode("utf-8")).hexdigest()


def adapt_html(html: str) -> str:
	html = html.replace(
		"fbr_integration.print_barcodes.get_qr_and_barcode_data_uri",
		"erpnext_print_pack.print_barcodes.get_qr_and_barcode_data_uri",
	)
	html = html.replace("/assets/fbr_integration/images/fbr/DI_invoicing.png", FBR_DI_LOGO)
	html = re.sub(r"white-space:\s*nowrap", "white-space:normal;word-wrap:break-word;overflow-wrap:anywhere", html)
	return html


def write_format(source_name: str, display_name: str, slug: str, row: dict) -> None:
	html = adapt_html(row.get("html") or "")
	fdir = FORMATS_DIR / slug
	fdir.mkdir(parents=True, exist_ok=True)
	meta = {
		"name": display_name,
		"slug": slug,
		"doc_type": "Sales Invoice",
		"theme": slug,
		"layout_family": slug,
		"layout_type": "regional",
		"region": "PK",
		"category": "sales",
		"orientation": "portrait",
		"paper_size": "A4",
		"languages": ["en"],
		"features": ["fbr", "pakistan", "sales-tax", "qr", "barcode"],
		"source_type": "adapted",
		"source_license": "MIT",
		"source_app": "fbr_integration",
		"source_format": source_name,
		"status": "stable",
		"checksum": checksum(html),
		"description": f"Pakistan FBR sales tax invoice (adapted from {source_name})",
	}
	pf = {
		"doctype": "Print Format",
		"name": display_name,
		"doc_type": "Sales Invoice",
		"module": "Print Pack",
		"custom_format": 1,
		"print_format_type": "Jinja",
		"standard": "No",
		"disabled": 0,
		"default_print_language": "en",
		"margin_top": row.get("margin_top", 15.0),
		"margin_bottom": row.get("margin_bottom", 15.0),
		"margin_left": row.get("margin_left", 15.0),
		"margin_right": row.get("margin_right", 15.0),
		"page_number": "Hide",
		"css": "",
	}
	(fdir / f"{slug}.html").write_text(html, encoding="utf-8")
	(fdir / f"{slug}.json").write_text(json.dumps(pf, indent=1) + "\n", encoding="utf-8")
	(fdir / "metadata.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")


def main():
	if not FBR_FIXTURE.exists():
		raise SystemExit(f"FBR fixture not found: {FBR_FIXTURE}")
	rows = {r["name"]: r for r in json.loads(FBR_FIXTURE.read_text(encoding="utf-8"))}
	created = 0
	for source_name, display_name, slug in SOURCE_MAP:
		row = rows.get(source_name)
		if not row:
			print(f"skip missing source: {source_name}")
			continue
		write_format(source_name, display_name, slug, row)
		created += 1
	manifest = rebuild_manifest_from_folders()
	print(json.dumps({"imported": created, "manifest_total": manifest["total_formats"]}, indent=2))


if __name__ == "__main__":
	main()
