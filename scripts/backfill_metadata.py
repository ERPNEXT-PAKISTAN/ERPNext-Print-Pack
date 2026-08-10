#!/usr/bin/env python3
"""Backfill required metadata fields and refresh HTML checksums."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORMATS = ROOT / "erpnext_print_pack" / "print_pack" / "print_format"

DEFAULTS = {
	"attribution_required": False,
	"erpnext_versions": ["15", "16"],
	"source_type": "original",
	"source_license": "MIT",
	"languages": ["en"],
	"features": [],
	"orientation": "portrait",
	"paper_size": "A4",
}


def checksum(content: str) -> str:
	return hashlib.sha256(content.encode("utf-8")).hexdigest()


def main() -> None:
	updated = 0
	for fdir in sorted(FORMATS.iterdir()):
		if not fdir.is_dir():
			continue
		meta_path = fdir / "metadata.json"
		if not meta_path.exists():
			continue
		html_files = list(fdir.glob("*.html"))
		if not html_files:
			continue
		meta = json.loads(meta_path.read_text(encoding="utf-8"))
		html = html_files[0].read_text(encoding="utf-8")
		changed = False
		for key, value in DEFAULTS.items():
			if key not in meta:
				meta[key] = value
				changed = True
		if not meta.get("slug"):
			meta["slug"] = fdir.name
			changed = True
		if not meta.get("theme"):
			meta["theme"] = meta.get("layout_family") or meta.get("slug") or fdir.name
			changed = True
		if not meta.get("category"):
			meta["category"] = "general"
			changed = True
		new_sum = checksum(html)
		if meta.get("checksum") != new_sum:
			meta["checksum"] = new_sum
			changed = True
		if changed:
			meta_path.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
			updated += 1
	print(json.dumps({"updated": updated}, indent=2))


if __name__ == "__main__":
	main()
