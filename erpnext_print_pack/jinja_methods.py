"""Shared Jinja helpers available in print templates as print_helpers()."""

from __future__ import annotations

import frappe


def print_helpers():
	return {
		"safe": _safe,
		"money": _money,
	}


def get_item_last_purchases(item_code: str, limit: int = 2):
	"""Last purchase invoice lines for an item (supplier, rate, qty)."""
	item_code = (item_code or "").strip()
	if not item_code:
		return []
	return frappe.db.sql(
		"""
		SELECT
			pi.supplier_name,
			pi.supplier,
			pii.rate,
			pii.qty,
			pii.stock_uom,
			pi.posting_date
		FROM `tabPurchase Invoice Item` pii
		INNER JOIN `tabPurchase Invoice` pi ON pi.name = pii.parent
		WHERE pii.item_code = %s AND pi.docstatus = 1
		ORDER BY pi.posting_date DESC, pi.creation DESC
		LIMIT %s
		""",
		(item_code, int(limit)),
		as_dict=True,
	)


def _safe(value, default=""):
	return default if value is None else value


def _money(value, precision=2):
	try:
		return f"{float(value or 0):,.{precision}f}"
	except (TypeError, ValueError):
		return "0.00"
