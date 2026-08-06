#!/usr/bin/env python3
"""Validate print formats with Frappe Jinja engine (site context required)."""

from __future__ import annotations

import json
from pathlib import Path

import frappe

from erpnext_print_pack.print_format_sync import PRINT_FORMAT_ROOT, _load_format, _validate_jinja


def execute(include_draft: bool = False) -> dict:
	frappe.only_for("System Manager")
	stable_failures = []
	draft_failures = []
	validated_stable = 0
	validated_draft = 0

	for format_dir in sorted(PRINT_FORMAT_ROOT.iterdir()):
		if not format_dir.is_dir():
			continue
		try:
			row, metadata, slug, html_path = _load_format(format_dir)
		except Exception as exc:
			stable_failures.append({"name": format_dir.name, "path": str(format_dir), "error": str(exc)})
			continue

		name = row.get("name") or slug
		status = metadata.get("status", "stable")
		if status == "draft" and not include_draft:
			continue

		error = _validate_jinja(row["html"], name)
		if error:
			entry = {"name": name, "path": str(html_path), "error": error}
			if status == "draft":
				draft_failures.append(entry)
			else:
				stable_failures.append(entry)
			continue

		if status == "draft":
			validated_draft += 1
		else:
			validated_stable += 1

	result = {
		"validated_stable": validated_stable,
		"validated_draft": validated_draft,
		"stable_failures": stable_failures,
		"draft_failures": draft_failures,
	}
	print(json.dumps(result, indent=2))
	if stable_failures:
		frappe.throw(f"{len(stable_failures)} stable format(s) failed Jinja validation")
	return result
