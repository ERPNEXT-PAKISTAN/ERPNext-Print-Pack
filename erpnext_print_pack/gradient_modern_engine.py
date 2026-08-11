"""Gradient Modern invoice — shared HTML/CSS (indigo/purple gradient card)."""

from __future__ import annotations

from erpnext_print_pack.doctype_profiles import DocTypeProfile
from erpnext_print_pack.layout_engine import _party_vars
from erpnext_print_pack.print_snippets import DOC_BARCODE_SNIPPET

LAYOUT_KEY = "gradient_modern"
LAYOUT_LABEL = "Gradient Modern Invoice"
LAYOUT_META = {
	"label": LAYOUT_LABEL,
	"region": "ALL",
	"layout_type": "colorful",
	"description": "Modern gradient card invoice — indigo/purple header, clean Inter-style layout",
}


def format_name(profile: DocTypeProfile) -> str:
	return f"{LAYOUT_LABEL} {profile.title}"


def format_slug(profile: DocTypeProfile) -> str:
	return f"{profile.slug}_{LAYOUT_KEY}"


def render_gradient_modern(profile: DocTypeProfile) -> str:
	party = _party_vars(profile)
	doc_heading = profile.title.upper()

	items_block = ""
	if profile.has_items:
		items_block = """
{% if doc.items %}
<table class="gm-table">
<thead><tr><th>Description</th><th class="r">Qty</th><th class="r">Rate</th><th class="r">Amount</th></tr></thead>
<tbody>
{% for row in doc.items %}
<tr>
<td>{{ row.item_name or row.item_code or row.description or "" }}</td>
<td class="r">{{ row.qty or "" }}</td>
<td class="r">{{ row.get_formatted("rate", doc) if row.get_formatted is defined else row.rate or "" }}</td>
<td class="r">{{ row.get_formatted("amount", doc) if row.get_formatted is defined else row.amount or "" }}</td>
</tr>
{% endfor %}
</tbody>
</table>
{% endif %}"""
	else:
		items_block = """
<table class="gm-table">
<thead><tr><th>Description</th><th class="r">Amount</th></tr></thead>
<tbody><tr><td>{{ doc.name }}</td><td class="r">{{ doc.get_formatted("grand_total") if doc.get_formatted is defined else doc.grand_total or doc.paid_amount or "" }}</td></tr></tbody>
</table>"""

	due_block = ""
	if profile.has_due_date:
		due_block = """
<div><h4>Due Date</h4><p>{% if doc.due_date %}{{ frappe.utils.formatdate(doc.due_date) }}{% else %}—{% endif %}</p></div>"""
	else:
		due_block = f"""
<div><h4>Date</h4><p>{{{{ frappe.utils.formatdate(doc.get("{profile.date_field}")) if doc.get("{profile.date_field}") else "" }}}}</p></div>"""

	tax_lines = ""
	if profile.has_taxes:
		tax_lines = """
{% for tax in doc.taxes or [] %}
<div class="gm-tax-row"><span>{{ tax.description or "Tax" }}</span><span>{{ tax.get_formatted("tax_amount") if tax.get_formatted is defined else tax.tax_amount or "" }}</span></div>
{% endfor %}"""

	in_words = ""
	if profile.has_in_words:
		in_words = '{% if doc.in_words %}<p class="gm-words">{{ doc.in_words }}</p>{% endif %}'

	return f"""{{# Gradient Modern · {profile.doc_type} #}}
{{% set date_field = "{profile.date_field}" %}}
{party}
<style>
@page {{ size: A4 portrait; margin: 10mm; }}
.gm-root {{ font-family: 'Inter', 'Segoe UI', Arial, sans-serif; color: #111827; font-size: 11px; }}
.gm-card {{ background: #fff; border-radius: 16px; overflow: hidden; box-shadow: 0 4px 16px rgba(0,0,0,.08); }}
.gm-header {{ background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%); color: #fff; padding: 28px 32px; display: flex; justify-content: space-between; align-items: flex-start; }}
.gm-header h2 {{ margin: 0 0 4px; font-size: 20px; font-weight: 700; }}
.gm-header p {{ margin: 0; opacity: .9; font-size: 11px; }}
.gm-header h1 {{ margin: 0 0 4px; font-size: 26px; font-weight: 700; letter-spacing: 1px; }}
.gm-header-right {{ text-align: right; }}
.gm-content {{ padding: 28px 32px; }}
.gm-grid {{ display: flex; justify-content: space-between; gap: 40px; margin-bottom: 28px; }}
.gm-grid h4 {{ color: #6366f1; text-transform: uppercase; font-size: 11px; margin: 0 0 8px; letter-spacing: .5px; }}
.gm-grid p {{ margin: 0; line-height: 1.5; }}
.gm-table {{ width: 100%; border-collapse: collapse; }}
.gm-table th {{ text-align: left; padding: 8px 0; border-bottom: 2px solid #eee; color: #6b7280; font-size: 11px; text-transform: uppercase; }}
.gm-table th.r {{ text-align: right; }}
.gm-table td {{ padding: 14px 0; border-bottom: 1px solid #f3f4f6; }}
.gm-table td.r {{ text-align: right; }}
.gm-total {{ margin-top: 24px; text-align: right; }}
.gm-total h4 {{ color: #6366f1; text-transform: uppercase; font-size: 11px; margin: 0 0 6px; }}
.gm-total-amt {{ font-size: 26px; font-weight: 700; color: #6366f1; }}
.gm-tax-row {{ display: flex; justify-content: flex-end; gap: 24px; font-size: 11px; color: #6b7280; margin-top: 4px; }}
.gm-words {{ margin-top: 12px; font-size: 10px; color: #6b7280; font-style: italic; text-align: right; }}
.r {{ text-align: right; }}
.epp-sig,.sig,.epp-footer,.footer {{ display: none; }}
.print-format .gm-table > tbody > tr > td {{ padding: 14px 0 !important; }}
</style>
<div class="gm-root print-format">
<div class="gm-card">
<header class="gm-header">
<div>
<h2>{{{{ doc.company or "" }}}}</h2>
<p>{{{{ doc.company_address_display or "" }}}}</p>
</div>
<div class="gm-header-right">
<h1>{doc_heading}</h1>
<p>#{{{{ doc.name }}}}</p>
</div>
</header>
<div class="gm-content">
<div class="gm-grid">
<div><h4>{{{{ party_label or "Client" }}}}</h4><p><b>{{{{ party_name }}}}</b><br>{{{{ party_address }}}}</p></div>
{due_block}
</div>
{items_block}
{tax_lines}
<div class="gm-total">
<h4>Total Due</h4>
<div class="gm-total-amt">{{{{ doc.get_formatted("grand_total") if doc.get_formatted is defined else doc.grand_total or doc.total or doc.paid_amount or "" }}}}</div>
</div>
{in_words}
</div>
</div>
{DOC_BARCODE_SNIPPET}
</div>"""
