"""Preview generation framework (synthetic sample data only)."""

from __future__ import annotations

import json
from pathlib import Path

PREVIEW_ROOT = Path(__file__).resolve().parents[2] / "previews"


SAMPLE_DOCS = {
	"Sales Invoice": {
		"name": "SINV-PREVIEW-0001",
		"company": "Sample Company",
		"customer_name": "Sample Customer",
		"posting_date": "2026-01-15",
		"currency": "USD",
		"net_total": 1000,
		"grand_total": 1100,
		"in_words": "One Thousand One Hundred only",
	},
}


def generate_preview_html(doc_type: str, html_template: str) -> str:
	"""Render a lightweight preview using synthetic placeholders."""
	sample = SAMPLE_DOCS.get(doc_type, {"name": "PREVIEW-0001", "company": "Sample Company"})
	replacements = {
		"{{ doc.name or \"\" }}": sample.get("name", ""),
		"{{ doc.company or \"\" }}": sample.get("company", ""),
		"{{ doc.customer_name or doc.customer or \"\" }}": sample.get("customer_name", ""),
	}
	out = html_template
	for k, v in replacements.items():
		out = out.replace(k, str(v))
	return out


def write_preview_index():
	PREVIEW_ROOT.mkdir(parents=True, exist_ok=True)
	index = PREVIEW_ROOT / "index.json"
	index.write_text(json.dumps({"note": "Synthetic previews only. No real business data."}, indent=2) + "\n")
