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


def get_item_prices(item_code: str, limit: int = 20):
	"""Active Item Price rows for printouts."""
	item_code = (item_code or "").strip()
	if not item_code or not frappe.db.exists("DocType", "Item Price"):
		return []
	return frappe.get_all(
		"Item Price",
		filters={"item_code": item_code},
		fields=["price_list", "price_list_rate", "currency", "uom", "valid_from", "valid_upto"],
		order_by="price_list asc, valid_from desc",
		limit_page_length=int(limit),
	)


def get_doc_barcode_data_uri(
	value: str = "",
	module_width: float | None = None,
	module_height: float | None = None,
	compact: int | bool = 0,
):
	"""Jinja-safe document barcode helper (avoids frappe.call/request dependency)."""
	try:
		from erpnext_print_pack.print_barcodes import get_doc_barcode_data_uri as _impl

		return (
			_impl(
				value=value,
				module_width=module_width,
				module_height=module_height,
				compact=compact,
			)
			or ""
		)
	except Exception:
		frappe.log_error(title="erpnext_print_pack barcode render failed")
		return ""


def _safe(value, default=""):
	return default if value is None else value


def _money(value, precision=2):
	try:
		return f"{float(value or 0):,.{precision}f}"
	except (TypeError, ValueError):
		return "0.00"
