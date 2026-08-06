"""Frappe / ERPNext version compatibility helpers."""

from __future__ import annotations

import frappe


def get_frappe_version() -> tuple[int, int, int]:
	version = getattr(frappe, "__version__", "0.0.0")
	parts = []
	for part in version.split(".")[:3]:
		try:
			parts.append(int(part))
		except ValueError:
			parts.append(0)
	while len(parts) < 3:
		parts.append(0)
	return tuple(parts)


def get_erpnext_version() -> tuple[int, int, int]:
	try:
		version = frappe.get_attr("erpnext.__version__")
	except Exception:
		return (0, 0, 0)
	parts = []
	for part in str(version).split(".")[:3]:
		try:
			parts.append(int(part))
		except ValueError:
			parts.append(0)
	while len(parts) < 3:
		parts.append(0)
	return tuple(parts)


def is_v15() -> bool:
	major, _, _ = get_frappe_version()
	return major == 15


def is_v16() -> bool:
	major, _, _ = get_frappe_version()
	return major >= 16


def format_date(value) -> str:
	if not value:
		return ""
	if is_v16():
		return frappe.utils.formatdate(value)
	return frappe.utils.format_date(value)


def doc_formatted(doc, fieldname: str) -> str:
	if hasattr(doc, "get_formatted"):
		try:
			return doc.get_formatted(fieldname) or ""
		except Exception:
			pass
	value = doc.get(fieldname) if hasattr(doc, "get") else getattr(doc, fieldname, "")
	if value in (None, ""):
		return ""
	return str(value)
