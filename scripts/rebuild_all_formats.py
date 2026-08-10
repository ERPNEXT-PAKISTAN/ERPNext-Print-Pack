#!/usr/bin/env python3
"""Regenerate theme/premium/regional/specimen formats and rebuild catalog."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

SCRIPTS = [
	"bootstrap_library.py",
	"generate_premium_layouts.py",
	"generate_regional_layouts.py",
	"generate_specimen_pack.py",
	"generate_item_detail_formats.py",
	"generate_readme_preview_formats.py",
	"backfill_metadata.py",
]


def run(script: str) -> None:
	path = ROOT / "scripts" / script
	print(f"\n=== {script} ===")
	result = subprocess.run([sys.executable, str(path)], cwd=str(ROOT))
	if result.returncode != 0:
		raise SystemExit(f"{script} failed with {result.returncode}")


def main() -> None:
	for script in SCRIPTS:
		run(script)

	from erpnext_print_pack.metadata_loader import rebuild_manifest_from_folders

	print("\n=== rebuild_manifest_from_folders ===")
	manifest = rebuild_manifest_from_folders()
	print({"total_formats": len(manifest.get("formats", []))})

	run("build_catalog.py")
	print("\nAll generators completed.")


if __name__ == "__main__":
	main()
