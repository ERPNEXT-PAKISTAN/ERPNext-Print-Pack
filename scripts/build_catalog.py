#!/usr/bin/env python3
"""Build FORMAT_CATALOG.md from manifest."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "erpnext_print_pack" / "print_pack" / "manifest.json"
OUT = ROOT / "FORMAT_CATALOG.md"


def build_catalog():
	manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
	formats = manifest.get("formats", [])
	lines = [
		"# Format Catalog",
		"",
		f"Generated formats: **{len(formats)}**",
		"",
		"## Summary",
		"",
	]
	by_doctype = Counter(f["doc_type"] for f in formats)
	by_theme = Counter(f["theme"] for f in formats)
	by_status = Counter(f["status"] for f in formats)
	lines.append(f"- Stable: {by_status.get('stable', 0)}")
	lines.append(f"- Draft: {by_status.get('draft', 0)}")
	lines.append(f"- DocTypes: {len(by_doctype)}")
	lines.append(f"- Themes: {len(by_theme)}")
	lines.append("")
	lines.append("## By DocType")
	lines.append("")
	for dt, count in sorted(by_doctype.items()):
		lines.append(f"- {dt}: {count}")
	lines.append("")
	lines.append("## By Theme")
	lines.append("")
	for th, count in sorted(by_theme.items()):
		lines.append(f"- {th}: {count}")
	lines.append("")
	lines.append("## Formats")
	lines.append("")
	lines.append("| Name | DocType | Theme | Status | Features |")
	lines.append("|---|---|---|---|---|")
	for f in sorted(formats, key=lambda x: (x["doc_type"], x["name"])):
		features = ", ".join(f.get("features") or [])
		lines.append(f"| {f['name']} | {f['doc_type']} | {f['theme']} | {f['status']} | {features} |")
	OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
	print(f"Wrote {OUT} ({len(formats)} formats)")


if __name__ == "__main__":
	build_catalog()
