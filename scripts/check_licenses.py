#!/usr/bin/env python3
"""Check third-party source registry completeness."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "erpnext_print_pack" / "print_pack" / "source_registry.json"
ALLOWED_USAGE = {"copied", "adapted", "inspired", "rejected"}


def check_licenses() -> int:
	if not REGISTRY.exists():
		print("ERROR: source_registry.json missing")
		return 1
	data = json.loads(REGISTRY.read_text(encoding="utf-8"))
	errors = 0
	for entry in data.get("sources", []):
		repo = entry.get("repository", "<unknown>")
		if not entry.get("license"):
			print(f"ERROR: missing license for {repo}")
			errors += 1
		if entry.get("usage") not in ALLOWED_USAGE:
			print(f"ERROR: invalid usage for {repo}: {entry.get('usage')}")
			errors += 1
		if entry.get("usage") in ("copied", "adapted") and not entry.get("files_used"):
			print(f"WARN: copied/adapted source {repo} has empty files_used")
		if entry.get("usage") == "rejected" and entry.get("files_used"):
			print(f"WARN: rejected source {repo} lists files_used")
		if not entry.get("url"):
			print(f"ERROR: missing URL for {repo}")
			errors += 1
	print(f"Checked {len(data.get('sources', []))} sources, errors={errors}")
	return errors


if __name__ == "__main__":
	sys.exit(check_licenses())
