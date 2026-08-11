"""Premium Boxed invoice — shared HTML/CSS (Poppins grid cards, status badge, gold notes)."""

from __future__ import annotations

from erpnext_print_pack.doctype_profiles import DocTypeProfile
from erpnext_print_pack.layout_engine import _party_vars
from erpnext_print_pack.print_snippets import DOC_BARCODE_SNIPPET

LAYOUT_KEY = "premium_boxed"
LAYOUT_LABEL = "Premium Boxed Invoice"
LAYOUT_META = {
	"label": LAYOUT_LABEL,
	"region": "ALL",
	"layout_type": "colorful",
	"description": "Premium boxed grid invoice — Poppins cards, status badge, gold notes, dark totals",
}


def format_name(profile: DocTypeProfile) -> str:
	return f"{LAYOUT_LABEL} {profile.title}"


def format_slug(profile: DocTypeProfile) -> str:
	return f"{profile.slug}_{LAYOUT_KEY}"


def render_premium_boxed(profile: DocTypeProfile) -> str:
	party = _party_vars(profile)

	if profile.has_items:
		items_block = """
{% if doc.items %}
<table>
<thead>
<tr>
<th>Service Description</th>
<th>Qty</th>
<th>Rate</th>
<th class="pb-r">Total</th>
</tr>
</thead>
<tbody>
{% for row in doc.items %}
<tr>
<td>
<p class="pb-item-name">{{ row.item_name or row.item_code or "" }}</p>
{% if row.description and row.description != (row.item_name or row.item_code) %}
<p class="pb-item-service">{{ row.description }}</p>
{% endif %}
</td>
<td>{{ row.qty or "" }}</td>
<td>{{ row.get_formatted("rate", doc) if row.get_formatted is defined else row.rate or "" }}</td>
<td class="pb-r pb-item-total">{{ row.get_formatted("amount", doc) if row.get_formatted is defined else row.amount or "" }}</td>
</tr>
{% endfor %}
</tbody>
</table>
{% endif %}"""
	else:
		items_block = """
<table>
<thead><tr><th>Description</th><th class="pb-r">Total</th></tr></thead>
<tbody><tr><td>{{ doc.name }}</td><td class="pb-r">{{ doc.get_formatted("grand_total") if doc.get_formatted is defined else doc.grand_total or doc.paid_amount or "" }}</td></tr></tbody>
</table>"""

	tax_rows = ""
	if profile.has_taxes:
		tax_rows = """
{% for tax in doc.taxes or [] %}
<div class="pb-calc-row"><span>{{ tax.description or "Tax" }}</span><span>{{ tax.get_formatted("tax_amount") if tax.get_formatted is defined else tax.tax_amount or "" }}</span></div>
{% endfor %}"""
	elif profile.has_items:
		tax_rows = """
{% if doc.total_taxes_and_charges %}
<div class="pb-calc-row"><span>Tax</span><span>{{ doc.get_formatted("total_taxes_and_charges") if doc.get_formatted is defined else doc.total_taxes_and_charges or "" }}</span></div>
{% endif %}"""

	notes_block = ""
	if profile.has_terms:
		notes_block = """
<div class="pb-box pb-notes">
<h3>Notes</h3>
<p>{% if doc.terms %}{{ doc.terms }}{% elif doc.payment_terms_template %}{{ doc.payment_terms_template }}{% else %}Please include the invoice number in your payment reference. Thank you!{% endif %}</p>
</div>"""
	else:
		notes_block = """
<div class="pb-box pb-notes">
<h3>Notes</h3>
<p>Please include the invoice number in your payment reference. Thank you!</p>
</div>"""

	due_line = ""
	if profile.has_due_date:
		due_line = '<p><strong>Due:</strong> {% if doc.due_date %}{{ frappe.utils.formatdate(doc.due_date) }}{% else %}—{% endif %}</p>'

	return f"""{{# Premium Boxed · {profile.doc_type} #}}
{{% set date_field = "{profile.date_field}" %}}
{party}
<style>
@page {{ size: A4 portrait; margin: 10mm; }}
.pb-root {{ font-family: 'Poppins', 'Segoe UI', Arial, sans-serif; color: #1e293b; font-size: 11px; }}
.pb-container {{ display: block; }}
.pb-box {{ background: #fff; padding: 20px 22px; border-radius: 12px; box-shadow: 0 2px 6px rgba(0,0,0,.08); border: 1px solid rgba(0,0,0,.05); margin-bottom: 16px; }}
.pb-header {{ border-left: 8px solid #4f46e5; display: flex; justify-content: space-between; align-items: center; }}
.pb-logo h1 {{ margin: 0; font-size: 22px; color: #4f46e5; text-transform: uppercase; letter-spacing: 1px; font-weight: 700; }}
.pb-logo p {{ margin: 4px 0 0; font-size: 11px; color: #64748b; }}
.pb-badge {{ background: #dcfce7; color: #15803d; padding: 6px 14px; border-radius: 20px; font-weight: 600; font-size: 12px; text-transform: uppercase; }}
.pb-badge.unpaid {{ background: #fef3c7; color: #b45309; }}
.pb-badge.draft {{ background: #e2e8f0; color: #475569; }}
.pb-badge.cancelled {{ background: #fee2e2; color: #b91c1c; }}
.pb-info-row {{ display: flex; gap: 16px; margin-bottom: 16px; }}
.pb-info {{ flex: 1; }}
.pb-info.highlight {{ border-top: 4px solid #f43f5e; }}
.pb-info h3 {{ margin: 0 0 12px; font-size: 11px; text-transform: uppercase; color: #64748b; letter-spacing: 1px; font-weight: 600; }}
.pb-info p {{ margin: 0 0 4px; font-size: 12px; line-height: 1.6; }}
.pb-table-box {{ padding: 0; overflow: hidden; }}
.pb-table-box table {{ width: 100%; border-collapse: collapse; }}
.pb-table-box thead {{ background: #f8fafc; }}
.pb-table-box th {{ text-align: left; padding: 12px 20px; font-size: 11px; color: #64748b; text-transform: uppercase; font-weight: 600; }}
.pb-table-box td {{ padding: 14px 20px; border-bottom: 1px solid #f1f5f9; font-size: 12px; }}
.pb-item-name {{ margin: 0; font-weight: 600; color: #4f46e5; }}
.pb-item-service {{ margin: 4px 0 0; font-size: 11px; color: #64748b; }}
.pb-item-total {{ font-weight: 600; }}
.pb-r {{ text-align: right; }}
.pb-bottom {{ display: flex; gap: 16px; }}
.pb-notes {{ flex: 1; background: #fbbf24; color: #78350f; margin-bottom: 0; }}
.pb-notes h3 {{ color: #78350f; }}
.pb-notes p {{ font-size: 12px; }}
.pb-calc {{ flex: 2; background: #1e293b; color: #fff; margin-bottom: 0; }}
.pb-calc-row {{ display: flex; justify-content: space-between; margin-bottom: 8px; font-size: 12px; }}
.pb-calc-row.pb-total {{ margin-top: 12px; padding-top: 12px; border-top: 1px solid #334155; font-size: 18px; font-weight: 700; color: #fbbf24; }}
.epp-sig,.sig,.epp-footer,.footer {{ display: none; }}
.print-format .pb-table-box table > tbody > tr > td {{ padding: 14px 20px !important; }}
</style>
<div class="pb-root print-format">
<div class="pb-container">
<div class="pb-box pb-header">
<div class="pb-logo">
<h1>{{{{ doc.company or "" }}}}</h1>
<p>{profile.title} #{{{{ doc.name }}}}</p>
</div>
<div class="pb-badge{{% if doc.docstatus == 2 %}} cancelled{{% elif doc.docstatus == 0 %}} draft{{% elif doc.get("outstanding_amount") is not none and (doc.outstanding_amount or 0) <= 0 %}}{{% elif doc.get("status") == "Paid" %}}{{% else %}} unpaid{{% endif %}}">
{{% if doc.docstatus == 2 %}}Cancelled
{{% elif doc.docstatus == 0 %}}Draft
{{% elif doc.get("outstanding_amount") is not none and (doc.outstanding_amount or 0) <= 0 %}}Paid
{{% elif doc.get("status") == "Paid" %}}Paid
{{% else %}}Unpaid{{% endif %}}
</div>
</div>
<div class="pb-info-row">
<div class="pb-box pb-info">
<h3>From</h3>
<p><strong>{{{{ doc.company or "" }}}}</strong></p>
<p>{{{{ doc.company_address_display or "" }}}}</p>
</div>
<div class="pb-box pb-info highlight">
<h3>{{{{ party_label or "Bill To" }}}}</h3>
<p><strong>{{{{ party_name }}}}</strong></p>
<p>{{{{ party_address }}}}</p>
</div>
<div class="pb-box pb-info">
<h3>Timeline</h3>
<p><strong>Issued:</strong> {{{{ frappe.utils.formatdate(doc.get(date_field)) if doc.get(date_field) else "" }}}}</p>
{due_line}
</div>
</div>
<div class="pb-box pb-table-box">
{items_block}
</div>
<div class="pb-bottom">
{notes_block}
<div class="pb-box pb-calc">
<div class="pb-calc-row"><span>Subtotal</span><span>{{{{ doc.get_formatted("net_total") if doc.get_formatted is defined else doc.net_total or "" }}}}</span></div>
{tax_rows}
<div class="pb-calc-row pb-total"><span>Total</span><span>{{{{ doc.get_formatted("grand_total") if doc.get_formatted is defined else doc.grand_total or doc.total or "" }}}}</span></div>
</div>
</div>
</div>
{DOC_BARCODE_SNIPPET}
</div>"""
