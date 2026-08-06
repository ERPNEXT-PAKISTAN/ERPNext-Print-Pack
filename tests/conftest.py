"""Collect all format directories for parametrized tests."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORMATS = ROOT / "erpnext_print_pack" / "print_pack" / "print_format"
MANIFEST = ROOT / "erpnext_print_pack" / "print_pack" / "manifest.json"

FORBIDDEN_PATTERNS = [
	"<script",
	"<iframe",
	"<object",
	"<embed",
	"<form",
	"javascript:",
	"onload=",
	"onclick=",
	"onerror=",
]


def iter_formats():
	for fdir in sorted(FORMATS.iterdir()):
		if not fdir.is_dir():
			continue
		meta_path = fdir / "metadata.json"
		if not meta_path.exists():
			continue
		meta = json.loads(meta_path.read_text(encoding="utf-8"))
		html_files = list(fdir.glob("*.html"))
		if not html_files:
			continue
		yield fdir.name, meta, html_files[0]


def load_manifest():
	return json.loads(MANIFEST.read_text(encoding="utf-8"))
