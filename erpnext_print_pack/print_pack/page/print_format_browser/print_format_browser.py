"""Whitelisted APIs for the Print Format Browser desk page."""

from __future__ import annotations

import frappe
from frappe.utils import cint

from erpnext_print_pack.metadata_loader import enrich_format_record
from erpnext_print_pack.print_format_sync import APP_MODULE


def _default_print_format(doc_type: str) -> str | None:
	default = frappe.db.get_value("DocType", doc_type, "default_print_format")
	if default:
		return default
	return frappe.db.get_value(
		"Property Setter",
		{
			"doc_type": doc_type,
			"property": "default_print_format",
			"doctype_or_field": "DocType",
		},
		"value",
	)


@frappe.whitelist()
def get_doctypes():
	"""DocTypes that have Print Pack formats, with counts."""
	return frappe.db.sql(
		"""
		SELECT
			doc_type,
			SUM(CASE WHEN disabled = 0 THEN 1 ELSE 0 END) AS enabled_count,
			SUM(CASE WHEN disabled = 1 THEN 1 ELSE 0 END) AS disabled_count,
			COUNT(*) AS total_count
		FROM `tabPrint Format`
		WHERE module = %s
		GROUP BY doc_type
		ORDER BY doc_type
		""",
		APP_MODULE,
		as_dict=True,
	)


@frappe.whitelist()
def get_formats(doc_type, show_disabled=1, search=None, layout_filter=None, region=None):
	"""List Print Pack formats for a DocType."""
	filters: dict = {"module": APP_MODULE, "doc_type": doc_type}
	show_disabled = cint(show_disabled)
	if show_disabled == 0:
		filters["disabled"] = 0
	elif show_disabled == 2:
		filters["disabled"] = 1

	formats = frappe.get_all(
		"Print Format",
		filters=filters,
		fields=[
			"name",
			"doc_type",
			"disabled",
			"standard",
			"raw_printing",
			"print_format_type",
		],
		order_by="disabled asc, name asc",
	)

	# Reliable HTML presence check without loading full HTML blobs into Python.
	html_flags = {
		row.name: cint(row.has_html)
		for row in frappe.db.sql(
			"""
			SELECT name, CASE WHEN IFNULL(html, '') != '' THEN 1 ELSE 0 END AS has_html
			FROM `tabPrint Format`
			WHERE module = %s AND doc_type = %s
			""",
			(APP_MODULE, doc_type),
			as_dict=True,
		)
	}

	default_pf = _default_print_format(doc_type)

	for fmt in formats:
		fmt["has_html"] = bool(html_flags.get(fmt.name))
		enrich_format_record(fmt)
		fmt["is_default"] = fmt.name == default_pf

	if layout_filter == "premium":
		formats = [f for f in formats if f.get("is_premium")]
	elif layout_filter == "regional":
		formats = [
			f
			for f in formats
			if f.get("layout_type") in ("regional", "specimen")
			or f.get("region") in ("SA", "AE", "PK", "IN", "US", "ME")
			or any(x in (f.get("name") or "") for x in ("ZATCA", "UAE", "Saudi", "Pakistan FBR", "FBR Pakistan", "India GST", "Gulf Gold", "USA Commercial"))
		]
	elif layout_filter == "colorful":
		formats = [
			f
			for f in formats
			if f.get("layout_type") == "colorful"
			or any(x in (f.get("name") or "") for x in ("Gradient Vivid", "Emerald Fresh", "Crimson Shop", "Ocean Vibrant"))
		]
	elif layout_filter == "proforma":
		formats = [f for f in formats if f.get("is_proforma") or f.get("layout_type") == "proforma"]
	elif layout_filter == "thermal":
		formats = [
			f
			for f in formats
			if f.get("layout_type") == "thermal"
			or "Thermal" in (f.get("name") or "")
			or f.get("theme") == "thermal"
		]
	elif layout_filter == "hide_legacy":
		formats = [f for f in formats if not f.get("is_legacy") or f.get("is_default")]

	if region and region != "ALL":
		region_name_markers = {
			"SA": ("Saudi", "ZATCA"),
			"AE": ("UAE",),
			"PK": ("Pakistan", "FBR", "FBR Pakistan"),
			"IN": ("India", "GST"),
			"US": ("USA", "American"),
			"ME": ("Gulf Gold", "Gulf"),
		}
		markers = region_name_markers.get(region, ())

		def _matches_region(fmt: dict) -> bool:
			if fmt.get("region") == region:
				return True
			name = fmt.get("name") or ""
			return any(m in name for m in markers)

		formats = [f for f in formats if _matches_region(f)]

	if search:
		term = search.lower().strip()
		formats = [
			fmt
			for fmt in formats
			if term in fmt.name.lower()
			or term in (fmt.theme or "").lower()
			or term in (fmt.status or "").lower()
			or term in (fmt.layout_family or "").lower()
			or term in (fmt.region or "").lower()
			or term in (fmt.description or "").lower()
		]

	formats.sort(key=lambda f: (0 if f.get("is_premium") else 1, f.get("name") or ""))
	return formats


@frappe.whitelist()
def get_sample_document(doc_type):
	"""Latest readable document for live preview."""
	if not frappe.has_permission(doc_type, "read"):
		frappe.throw(frappe._("No read permission for {0}").format(doc_type))

	meta = frappe.get_meta(doc_type)
	filters: dict = {}
	if meta.is_submittable:
		filters["docstatus"] = 1

	name = frappe.db.get_value(doc_type, filters, "name", order_by="modified desc")
	if not name:
		name = frappe.db.get_value(doc_type, {}, "name", order_by="modified desc")

	if not name:
		return {"name": None, "message": frappe._("No documents found. Create one to preview.")}

	return {"name": name}


@frappe.whitelist()
def get_document(doc_type, name):
	"""Return document dict for print preview."""
	if not frappe.has_permission(doc_type, "read", name):
		frappe.throw(frappe._("Not permitted"), frappe.PermissionError)
	return frappe.get_doc(doc_type, name).as_dict()


@frappe.whitelist()
def toggle_disabled(name, disabled=0):
	"""Enable or disable a print format.

	If enabling a format with empty HTML, sync HTML from app files first.
	Draft formats without HTML previously blocked Enable ("HTML is required").
	"""
	doc = frappe.get_doc("Print Format", name)
	doc.check_permission("write")
	disabled = cint(disabled)

	if disabled == 0 and not (doc.html or "").strip():
		from erpnext_print_pack.print_format_sync import sync_all

		sync_all(
			print_format_name=name,
			statuses=("stable", "draft"),
			include_draft=True,
			dry_run=False,
			force=True,
		)
		doc.reload()
		if not (doc.html or "").strip():
			frappe.throw(
				frappe._(
					"This format has no HTML in the Print Pack library. "
					"Run Sync HTML (Stable) / include drafts from the browser menu."
				)
			)

	doc.disabled = disabled
	doc.save()
	return {"name": doc.name, "disabled": doc.disabled, "has_html": bool((doc.html or "").strip())}


@frappe.whitelist()
def sync_formats(include_draft=1):
	"""Load HTML from app files into Print Format records (includes drafts by default)."""
	frappe.only_for("System Manager")
	from erpnext_print_pack.print_format_sync import sync_all

	include_draft = cint(include_draft)
	statuses = ("stable", "draft") if include_draft else ("stable",)
	result = sync_all(
		statuses=statuses,
		include_draft=include_draft,
		dry_run=False,
		force=False,
	)
	frappe.clear_cache()
	return result
