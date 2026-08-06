#!/usr/bin/env python3
"""Validate erpnext_print_pack repository integrity."""

from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "erpnext_print_pack"
FORMATS = APP / "print_pack" / "print_format"
MANIFEST = APP / "print_pack" / "manifest.json"

REQUIRED_META = {
	"name", "slug", "doc_type", "theme", "category", "orientation",
	"paper_size", "languages", "features", "source_type", "source_license",
	"attribution_required", "erpnext_versions", "status",
}


def validate_repository() -> int:
	errors: list[str] = []
	warnings: list[str] = []
	names: list[str] = []
	slugs: list[str] = []

	for fdir in sorted(FORMATS.iterdir()):
		if not fdir.is_dir():
			continue
		slug = fdir.name
		json_files = [p for p in fdir.glob("*.json") if p.name != "metadata.json"]
		html_files = list(fdir.glob("*.html"))
		meta_path = fdir / "metadata.json"

		if not json_files:
			errors.append(f"{slug}: missing print format json")
			continue
		if not html_files:
			errors.append(f"{slug}: missing html")
			continue
		if not meta_path.exists():
			errors.append(f"{slug}: missing metadata.json")
			continue

		try:
			meta = json.loads(meta_path.read_text(encoding="utf-8"))
			pf = json.loads(json_files[0].read_text(encoding="utf-8"))
			html = html_files[0].read_text(encoding="utf-8")
		except Exception as exc:
			errors.append(f"{slug}: invalid json/html - {exc}")
			continue

		missing = REQUIRED_META - set(meta)
		if missing:
			errors.append(f"{slug}: metadata missing {sorted(missing)}")

		name = meta.get("name") or pf.get("name")
		if name:
			names.append(name)
		slugs.append(meta.get("slug") or slug)

		if not html.strip():
			errors.append(f"{slug}: empty html")
		if re.search(r"<script", html, re.I):
			errors.append(f"{slug}: contains script tag")
		if re.search(r"https?://[^\s\"']+\.(css|js)", html, re.I):
			warnings.append(f"{slug}: remote asset reference")
		if meta.get("status") == "stable" and len(html) < 80:
			warnings.append(f"{slug}: suspiciously short stable template")

		for token in ("if", "for"):
			opens = len(re.findall(rf"\{{%-?\s*{token}\b", html))
			closes = len(re.findall(rf"\{{%-?\s*end{token}\b", html))
			if opens != closes:
				errors.append(f"{slug}: unbalanced jinja {token} ({opens}/{closes})")

	name_dupes = [n for n, c in Counter(names).items() if c > 1]
	slug_dupes = [s for s, c in Counter(slugs).items() if c > 1]
	if name_dupes:
		errors.append(f"Duplicate names: {name_dupes[:10]}")
	if slug_dupes:
		errors.append(f"Duplicate slugs: {slug_dupes[:10]}")

	if MANIFEST.exists():
		manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
		folder_count = len([p for p in FORMATS.iterdir() if p.is_dir() and (p / "metadata.json").exists()])
		if len(manifest.get("formats", [])) != folder_count:
			warnings.append(f"Manifest count ({len(manifest.get('formats', []))}) differs from folder count ({folder_count})")

	print(f"Validated {len(slugs)} formats")
	print(f"Errors: {len(errors)}")
	print(f"Warnings: {len(warnings)}")
	for e in errors[:30]:
		print(f"ERROR: {e}")
	for w in warnings[:15]:
		print(f"WARN: {w}")
	return 1 if errors else 0


if __name__ == "__main__":
	sys.exit(validate_repository())
