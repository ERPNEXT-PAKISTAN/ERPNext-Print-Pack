"""Modular Box invoice — shared HTML/CSS (grid card boxes, indigo/rose accents)."""

from __future__ import annotations

from erpnext_print_pack.doctype_profiles import DocTypeProfile
from erpnext_print_pack.layout_engine import _party_vars
from erpnext_print_pack.print_snippets import DOC_BARCODE_SNIPPET

LAYOUT_KEY = "modular_box"
LAYOUT_LABEL = "Modular Box Invoice"
LAYOUT_META = {
	"label": LAYOUT_LABEL,
	"region": "ALL",
	"layout_type": "colorful",
	"description": "Modular box grid invoice — Poppins-style cards, indigo header stripe, dark total bar",
}


def format_name(profile: DocTypeProfile) -> str:
	return f"{LAYOUT_LABEL} {profile.title}"


def format_slug(profile: DocTypeProfile) -> str:
	return f"{profile.slug}_{LAYOUT_KEY}"


def render_modular_box(profile: DocTypeProfile) -> str:
	party = _party_vars(profile)
	doc_heading = profile.title.upper()

	if profile.has_items:
		items_block = """
{% if doc.items %}
<table>
<thead><tr><th>Item</th><th>Qty</th><th class="r">Rate</th><th class="r">Total</th></tr></thead>
<tbody>
{% for row in doc.items %}
<tr>
<td>{{ row.item_name or row.item_code or row.description or "" }}</td>
<td>{{ row.qty or "" }}</td>
<td class="r">{{ row.get_formatted("rate", doc) if row.get_formatted is defined else row.rate or "" }}</td>
<td class="r">{{ row.get_formatted("amount", doc) if row.get_formatted is defined else row.amount or "" }}</td>
</tr>
{% endfor %}
</tbody>
</table>
{% endif %}"""
	else:
		items_block = """
<table>
<thead><tr><th>Description</th><th class="r">Total</th></tr></thead>
<tbody><tr><td>{{ doc.name }}</td><td class="r">{{ doc.get_formatted("grand_total") if doc.get_formatted is defined else doc.grand_total or doc.paid_amount or "" }}</td></tr></tbody>
</table>"""

	date_label = "Due Date" if profile.has_due_date else "Date"
	date_value = (
		'{% if doc.due_date %}{{ frappe.utils.formatdate(doc.due_date) }}{% else %}{{ frappe.utils.formatdate(doc.get(date_field)) if doc.get(date_field) else "" }}{% endif %}'
		if profile.has_due_date
		else f'{{{{ frappe.utils.formatdate(doc.get("{profile.date_field}")) if doc.get("{profile.date_field}") else "" }}}}'
	)

	in_words = ""
	if profile.has_in_words:
		in_words = '{% if doc.in_words %}<div class="mb-words">{{ doc.in_words }}</div>{% endif %}'

	return f"""{{# Modular Box · {profile.doc_type} #}}
{{% set date_field = "{profile.date_field}" %}}
{party}
<style>
@page {{ size: A4 portrait; margin: 10mm; }}
.mb-root {{ font-family: 'Poppins', 'Segoe UI', Arial, sans-serif; color: #1e293b; font-size: 11px; }}
.mb-container {{ display: block; }}
.mb-box {{ background: #fff; padding: 16px 18px; border-radius: 12px; box-shadow: 0 2px 6px rgba(0,0,0,.06); margin-bottom: 14px; }}
.mb-header {{ border-left: 8px solid #4f46e5; display: flex; justify-content: space-between; align-items: center; }}
.mb-header h1 {{ margin: 0; font-size: 22px; font-weight: 600; color: #1e293b; }}
.mb-header .doc {{ text-align: right; font-size: 11px; line-height: 1.5; }}
.mb-header .doc b {{ font-size: 14px; display: block; color: #4f46e5; }}
.mb-row {{ display: flex; gap: 14px; margin-bottom: 14px; }}
.mb-client {{ flex: 2; border-top: 4px solid #f43f5e; }}
.mb-info {{ flex: 1; }}
.mb-row h3 {{ margin: 0 0 8px; font-size: 11px; text-transform: uppercase; color: #64748b; font-weight: 600; }}
.mb-row p {{ margin: 0; line-height: 1.5; }}
.mb-table-box {{ padding: 0; overflow: hidden; }}
.mb-table-box table {{ width: 100%; border-collapse: collapse; }}
.mb-table-box th {{ background: #f8fafc; padding: 12px 14px; text-align: left; color: #64748b; font-size: 11px; text-transform: uppercase; }}
.mb-table-box td {{ padding: 12px 14px; border-bottom: 1px solid #f1f5f9; }}
.mb-table-box .r {{ text-align: right; }}
.mb-total {{ background: #1e293b; color: #fff; }}
.mb-total-inner {{ display: flex; justify-content: space-between; align-items: center; font-weight: 600; font-size: 13px; text-transform: uppercase; letter-spacing: .5px; }}
.mb-price {{ font-weight: 600; color: #fbbf24; font-size: 20px; }}
.mb-words {{ margin-top: 8px; font-size: 10px; color: #64748b; font-style: italic; text-align: right; }}
.r {{ text-align: right; }}
.epp-sig,.sig,.epp-footer,.footer {{ display: none; }}
.print-format .mb-table-box table > tbody > tr > td {{ padding: 12px 14px !important; }}
</style>
<div class="mb-root print-format">
<div class="mb-container">
<div class="mb-box mb-header">
<h1>{{{{ doc.company or "" }}}}</h1>
<div class="doc"><b>{doc_heading}</b>#{{{{ doc.name }}}}</div>
</div>
<div class="mb-row">
<div class="mb-box mb-client">
<h3>{{{{ party_label or "Bill To" }}}}</h3>
<p><b>{{{{ party_name }}}}</b><br>{{{{ party_address }}}}</p>
</div>
<div class="mb-box mb-info">
<h3>{date_label}</h3>
<p>{date_value}</p>
</div>
</div>
<div class="mb-box mb-table-box">
{items_block}
</div>
<div class="mb-box mb-total">
<div class="mb-total-inner">
<span>Grand Total</span>
<span class="mb-price">{{{{ doc.get_formatted("grand_total") if doc.get_formatted is defined else doc.grand_total or doc.total or doc.paid_amount or "" }}}}</span>
</div>
{in_words}
</div>
</div>
{DOC_BARCODE_SNIPPET}
</div>"""
