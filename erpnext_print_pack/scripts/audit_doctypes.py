#!/usr/bin/env python3
"""Report installed vs missing DocTypes for print formats."""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

import frappe

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "print_pack" / "manifest.json"


def execute() -> dict:
	frappe.only_for("System Manager")
	manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
	by_dt = defaultdict(lambda: {"stable": 0, "draft": 0})
	installed = {}
	missing = {}

	for fmt in manifest.get("formats", []):
		dt = fmt["doc_type"]
		by_dt[dt][fmt["status"]] += 1
		if dt not in installed and dt not in missing:
			if frappe.db.exists("DocType", dt):
				installed[dt] = True
			else:
				missing[dt] = True

	report = {
		"installed_doctypes": sorted(installed.keys()),
		"missing_doctypes": sorted(missing.keys()),
		"formats_by_doctype": dict(by_dt),
	}
	print(json.dumps(report, indent=2))
	return report
