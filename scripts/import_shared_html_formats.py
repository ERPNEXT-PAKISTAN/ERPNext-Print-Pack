#!/usr/bin/env python3
"""Import user-shared HTML templates as Print Pack formats (batch; push when user confirms)."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from erpnext_print_pack.doctype_profiles import PROFILES  # noqa: E402
from erpnext_print_pack.gradient_modern_engine import (  # noqa: E402
	LAYOUT_KEY as GRADIENT_KEY,
	LAYOUT_META as GRADIENT_META,
	format_name as gradient_format_name,
	format_slug as gradient_format_slug,
	render_gradient_modern,
)
from erpnext_print_pack.modern_colorful_engine import (  # noqa: E402
	LAYOUT_KEY as MODERN_COLOR_KEY,
	LAYOUT_META as MODERN_COLOR_META,
	format_name as modern_color_format_name,
	format_slug as modern_color_format_slug,
	render_modern_colorful,
)
from erpnext_print_pack.modular_box_engine import (  # noqa: E402
	LAYOUT_KEY as MODULAR_KEY,
	LAYOUT_META as MODULAR_META,
	format_name as modular_format_name,
	format_slug as modular_format_slug,
	render_modular_box,
)
from erpnext_print_pack.premium_boxed_engine import (  # noqa: E402
	LAYOUT_KEY as PREMIUM_KEY,
	LAYOUT_META as PREMIUM_META,
	format_name as premium_format_name,
	format_slug as premium_format_slug,
	render_premium_boxed,
)
from erpnext_print_pack.payment_receipt_manrope_engine import (  # noqa: E402
	LAYOUT_KEY as PAYMENT_RECEIPT_KEY,
	LAYOUT_META as PAYMENT_RECEIPT_META,
	format_name as payment_receipt_format_name,
	format_slug as payment_receipt_format_slug,
	render_payment_receipt_manrope,
)
from erpnext_print_pack.zatca_manrope_engine import (  # noqa: E402
	LAYOUT_KEY as ZATCA_MANROPE_KEY,
	LAYOUT_META as ZATCA_MANROPE_META,
	format_name as zatca_manrope_format_name,
	format_slug as zatca_manrope_format_slug,
	render_zatca_manrope,
)
from erpnext_print_pack.bilingual_tax_invoice_engine import (  # noqa: E402
	LAYOUT_KEY as BILINGUAL_KEY,
	LAYOUT_META as BILINGUAL_META,
	format_name as bilingual_format_name,
	format_slug as bilingual_format_slug,
	render_bilingual_tax_invoice,
)
from erpnext_print_pack.ksa_zatca_fatoora_engine import (  # noqa: E402
	LAYOUT_KEY as KSA_KEY,
	LAYOUT_META as KSA_META,
	format_name as ksa_format_name,
	format_slug as ksa_format_slug,
	render_ksa_zatca_fatoora,
)
from erpnext_print_pack.layout_engine import COMMERCIAL_CATEGORIES  # noqa: E402
from erpnext_print_pack.metadata_loader import rebuild_manifest_from_folders  # noqa: E402

FORMATS = ROOT / "erpnext_print_pack" / "print_pack" / "print_format"

SHARED_LAYOUTS: list[dict] = [
	{
		"key": KSA_KEY,
		"meta": KSA_META,
		"format_name": ksa_format_name,
		"format_slug": ksa_format_slug,
		"render": render_ksa_zatca_fatoora,
		"doctypes": {
			"Sales Invoice",
			"Delivery Note",
			"Quotation",
			"Sales Order",
			"POS Invoice",
			"Purchase Invoice",
		},
	},
	{
		"key": ZATCA_MANROPE_KEY,
		"meta": ZATCA_MANROPE_META,
		"format_name": zatca_manrope_format_name,
		"format_slug": zatca_manrope_format_slug,
		"render": render_zatca_manrope,
		"doctypes": {
			"Sales Invoice",
			"Delivery Note",
			"Quotation",
			"Sales Order",
			"POS Invoice",
			"Purchase Invoice",
		},
	},
	{
		"key": GRADIENT_KEY,
		"meta": GRADIENT_META,
		"format_name": gradient_format_name,
		"format_slug": gradient_format_slug,
		"render": render_gradient_modern,
		"doctypes": None,
	},
	{
		"key": MODERN_COLOR_KEY,
		"meta": MODERN_COLOR_META,
		"format_name": modern_color_format_name,
		"format_slug": modern_color_format_slug,
		"render": render_modern_colorful,
		"doctypes": None,
	},
	{
		"key": MODULAR_KEY,
		"meta": MODULAR_META,
		"format_name": modular_format_name,
		"format_slug": modular_format_slug,
		"render": render_modular_box,
		"doctypes": None,
	},
	{
		"key": PREMIUM_KEY,
		"meta": PREMIUM_META,
		"format_name": premium_format_name,
		"format_slug": premium_format_slug,
		"render": render_premium_boxed,
		"doctypes": None,
	},
	{
		"key": BILINGUAL_KEY,
		"meta": BILINGUAL_META,
		"format_name": bilingual_format_name,
		"format_slug": bilingual_format_slug,
		"render": render_bilingual_tax_invoice,
		"doctypes": {
			"Sales Invoice",
			"Delivery Note",
			"Quotation",
			"Sales Order",
			"POS Invoice",
			"Purchase Invoice",
		},
	},
	{
		"key": PAYMENT_RECEIPT_KEY,
		"meta": PAYMENT_RECEIPT_META,
		"format_name": payment_receipt_format_name,
		"format_slug": payment_receipt_format_slug,
		"render": render_payment_receipt_manrope,
		"doctypes": {"Payment Entry"},
	},
]


def checksum(content: str) -> str:
	return hashlib.sha256(content.encode("utf-8")).hexdigest()


def write_format(profile, html: str, layout: dict) -> None:
	meta_info = layout["meta"]
	slug = layout["format_slug"](profile)
	name = layout["format_name"](profile)
	fdir = FORMATS / slug
	fdir.mkdir(parents=True, exist_ok=True)
	languages = meta_info.get("languages") or (
		["en", "ar"] if meta_info.get("region") == "SA" else ["en"]
	)
	meta = {
		"name": name,
		"slug": slug,
		"doc_type": profile.doc_type,
		"theme": layout["key"],
		"layout_family": layout["key"],
		"layout_type": meta_info["layout_type"],
		"region": meta_info["region"],
		"category": profile.category,
		"orientation": "portrait",
		"paper_size": "A4",
		"languages": languages,
		"features": ["shared-html", layout["key"]],
		"source_type": "adapted",
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


def generate_layout(layout: dict) -> int:
	render: Callable = layout["render"]
	allowed = layout.get("doctypes")
	count = 0
	for profile in PROFILES.values():
		if profile.category not in COMMERCIAL_CATEGORIES:
			continue
		if allowed is not None and profile.doc_type not in allowed:
			continue
		if allowed is None and not profile.has_items:
			continue
		html = render(profile)
		write_format(profile, html, layout)
		count += 1
	return count


def main():
	results = {}
	for layout in SHARED_LAYOUTS:
		results[layout["key"]] = generate_layout(layout)
	manifest = rebuild_manifest_from_folders()
	results["manifest_total"] = manifest["total_formats"]
	print(json.dumps(results, indent=2))


if __name__ == "__main__":
	main()
