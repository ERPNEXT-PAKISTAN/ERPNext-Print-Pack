"""Shared Jinja helpers available in print templates as print_helpers()."""

from __future__ import annotations

import frappe


def print_helpers():
	return {
		"safe": _safe,
		"money": _money,
		"translated": get_translated_text,
	}


def get_translated_text(source, language="ar"):
	"""Return Translation DocType / gettext value for a language (ar, ur, …).

	Used by bilingual prints so Translation Data (globe icon) works even when
	print language stays English. Returns empty string when no translation exists.
	"""
	source = (source or "").strip()
	if not source:
		return ""
	language = (language or "ar").strip()
	try:
		translated = frappe.db.get_value(
			"Translation",
			{"source_text": source, "language": language},
			"translated_text",
		)
		if translated:
			return translated
		result = frappe._(source, lang=language)
		if result and result != source:
			return result
	except Exception:
		frappe.log_error(title="erpnext_print_pack translation lookup failed")
	return ""


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


def get_qr_data_uri(value: str = ""):
	"""Jinja-safe QR image (avoids frappe.call/request dependency)."""
	try:
		from erpnext_print_pack.print_barcodes import get_qr_and_barcode_data_uri as _impl

		payload = _impl(value=value) or {}
		return payload.get("qr") or ""
	except Exception:
		frappe.log_error(title="erpnext_print_pack qr render failed")
		return ""


def get_item_tax_percent(item_tax_rate, default=0):
	"""First tax % from item_tax_rate (dict or JSON string). Safe for print Jinja."""
	import json

	if item_tax_rate in (None, "", {}, []):
		return default
	data = item_tax_rate
	if isinstance(data, str):
		try:
			data = json.loads(data)
		except Exception:
			return default
	if isinstance(data, dict):
		for value in data.values():
			try:
				if value is not None and float(value):
					return float(value)
			except (TypeError, ValueError):
				continue
		return default
	try:
		return float(data)
	except (TypeError, ValueError):
		return default


def _safe(value, default=""):
	return default if value is None else value


def _money(value, precision=2):
	try:
		return f"{float(value or 0):,.{precision}f}"
	except (TypeError, ValueError):
		return "0.00"
