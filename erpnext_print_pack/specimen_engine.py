"""E-invoice specimen templates for all DocTypes — SA, UAE, Proforma, Thermal."""

from __future__ import annotations

from erpnext_print_pack.doctype_profiles import DocTypeProfile
from erpnext_print_pack.layout_engine import _party_vars
from erpnext_print_pack.print_snippets import DOC_BARCODE_SNIPPET

SPECIMEN_PACKS = {
	"zatca_specimen": {"label": "ZATCA E-Invoice Specimen", "region": "SA", "accent": "#7d579b", "badge": "ZATCA", "badge_sub": "Compliant"},
	"uae_specimen": {"label": "UAE E-Invoice Specimen", "region": "AE", "accent": "#00732f", "badge": "UAE", "badge_sub": "VAT TRN"},
	"proforma_zatca": {"label": "Proforma ZATCA", "region": "SA", "accent": "#7d579b", "badge": "PROFORMA", "badge_sub": "ZATCA", "is_proforma": True},
	"proforma_uae": {"label": "Proforma UAE", "region": "AE", "accent": "#00732f", "badge": "PROFORMA", "badge_sub": "UAE VAT", "is_proforma": True},
	"proforma_modern": {"label": "Proforma Modern", "region": "ALL", "accent": "#6366f1", "badge": "PROFORMA", "badge_sub": "Quote", "is_proforma": True},
	"proforma_classic": {"label": "Proforma Classic", "region": "ALL", "accent": "#1e40af", "badge": "PROFORMA", "badge_sub": "Estimate", "is_proforma": True},
}

THERMAL_PACKS = {
	"zatca_thermal": {"label": "ZATCA Thermal Receipt", "region": "SA", "accent": "#006c35"},
	"uae_thermal": {"label": "UAE Thermal Receipt", "region": "AE", "accent": "#00732f"},
}

# DocTypes that get full specimen layouts (SA/UAE e-invoice style)
SPECIMEN_DOCTYPES = {
	"Sales Invoice",
	"Delivery Note",
	"Payment Entry",
	"Purchase Receipt",
	"Purchase Invoice",
	"Purchase Order",
	"Quotation",
	"Sales Order",
	"POS Invoice",
	"Payment Request",
	"Dunning",
	"Journal Entry",
	"Pick List",
	"Request for Quotation",
	"Supplier Quotation",
	"Material Request",
}

PROFORMA_DOCTYPES = {"Quotation", "Sales Order", "Sales Invoice"}

# DocTypes that get 80mm thermal receipt layouts
THERMAL_DOCTYPES = {
	"POS Invoice",
	"Sales Invoice",
	"Delivery Note",
	"Payment Entry",
	"Purchase Receipt",
}


def format_name(pack_label: str, profile: DocTypeProfile) -> str:
	return f"{pack_label} {profile.title}"


def format_slug(profile: DocTypeProfile, pack_key: str) -> str:
	return f"{profile.slug}_{pack_key}"


def render_specimen(profile: DocTypeProfile, pack_key: str, thermal: bool = False) -> str:
	pack = (THERMAL_PACKS if thermal else SPECIMEN_PACKS)[pack_key]
	accent = pack["accent"]
	party = _party_vars(profile)
	date_field = profile.date_field
	title = profile.title
	doc_label = "Proforma Invoice" if pack.get("is_proforma") and profile.doc_type in PROFORMA_DOCTYPES else profile.title

	if thermal:
		return _render_thermal(profile, pack, party, date_field, title)

	items_block = _items_block(profile)
	totals_block = _totals_block(profile)
	in_words = '{% if doc.in_words %}<div class="epp-words words">{{ doc.in_words }}</div>{% endif %}' if profile.has_in_words else ""
	terms = '{% if doc.terms %}<div class="epp-terms terms">{{ doc.terms }}</div>{% endif %}' if profile.has_terms else ""

	return f"""{{# Specimen {pack_key} · {profile.doc_type} #}}
{{% set title = "{title}" %}}
{{% set date_field = "{date_field}" %}}
{{% set doc_label = "{doc_label}" %}}
{party}
<style>
@page {{ size: A4 portrait; margin: 10mm; }}
.sp-root {{ font-family: 'Segoe UI', Arial, sans-serif; font-size: 10px; color: #1f2937; }}
.sp-title {{ font-size: 32px; font-weight: 800; margin: 0 0 8px; }}
.sp-meta {{ color: #6b7280; font-size: 10px; }} .sp-meta b {{ color: #111; }}
.sp-badge {{ width: 92px; height: 92px; border: 3px solid {accent}; border-radius: 50%; text-align: center; margin-left: auto; font-weight: 800; color: {accent}; padding-top: 26px; line-height: 1.2; font-size: 10px; }}
.sp-card {{ background: #f9fafb; border: 1px solid #e5e7eb; border-radius: 10px; padding: 12px 14px; width: 48%; display: inline-block; vertical-align: top; min-height: 80px; }}
.sp-card .lbl {{ color: {accent}; font-weight: 700; margin-bottom: 6px; }}
.sp-qr {{ width: 100px; height: 100px; border: 1px solid #e5e7eb; border-radius: 8px; margin: 0 auto; text-align: center; line-height: 100px; color: #9ca3af; }}
.sp-table {{ width: 100%; border-collapse: collapse; margin: 14px 0; }}
.sp-table th {{ background: {accent}; color: #fff; padding: 8px 6px; text-align: left; font-size: 9px; }}
.sp-table td {{ padding: 7px 6px; border-bottom: 1px solid #e5e7eb; font-size: 9px; }}
.r {{ text-align: right; }}
.sp-bank {{ background: #f9fafb; border-radius: 10px; padding: 12px; border: 1px solid #e5e7eb; }}
.sp-bank .lbl {{ color: {accent}; font-weight: 700; }}
.epp-sig,.sig,.epp-footer,.footer {{ display: none; }}
.print-format .sp-table > tbody > tr > td {{ padding: 7px 6px !important; }}
</style>
<div class="sp-root print-format">
<table style="width:100%;margin-bottom:16px"><tr>
<td style="width:38%"><div class="sp-title">{{{{ doc_label }}}}</div>
<div class="sp-meta">No <b>{{{{ doc.name }}}}</b><br>Date <b>{{{{ frappe.utils.formatdate(doc.get(date_field)) if doc.get(date_field) else "" }}}}</b>
{{% if doc.due_date %}}<br>Due <b>{{{{ frappe.utils.formatdate(doc.due_date) }}}}</b>{{% endif %}}</div></td>
<td style="width:24%;text-align:center"><div class="sp-qr epp-qr qr">{{% set qr = doc.get("ksa_einv_qr") or doc.get("custom_qr_code") or "" %}}{{% if not qr and doc.get("custom_fbr_invoice_no") %}}{{% set _fbr = frappe.call("erpnext_print_pack.print_barcodes.get_qr_and_barcode_data_uri", value=doc.custom_fbr_invoice_no, include_fbr_url=1) %}}{{% if _fbr %}}{{% set qr = _fbr.get("qr") or "" %}}{{% endif %}}{{% endif %}}{{% if qr %}}<img src="{{{{ qr }}}}" style="width:96px;height:96px">{{% else %}}QR{{% endif %}}</div></td>
<td style="width:38%"><div class="sp-badge">{pack["badge"]}<br><span style="font-size:8px">{pack["badge_sub"]}</span></div></td>
</tr></table>
<div style="margin-bottom:12px">
<div class="sp-card"><div class="lbl">From / Billed by</div><strong>{{{{ doc.company or "" }}}}</strong><br><span style="color:#6b7280;font-size:9px">{{{{ doc.company_address_display or "" }}}}</span><br>VAT/TRN: {{{{ doc.company_tax_id or "" }}}}</div>
<div class="sp-card" style="float:right"><div class="lbl">{{{{ party_label }}}}</div><strong>{{{{ party_name }}}}</strong><br><span style="color:#6b7280;font-size:9px">{{{{ party_address }}}}</span></div>
</div>
{items_block}
{totals_block}
<table style="width:100%;margin-top:12px"><tr>
<td style="width:50%"><div class="sp-bank"><div class="lbl">Bank / Payment</div>{{{{ doc.get("custom_bank_name") or doc.get("mode_of_payment") or "—" }}}}<br>{{{{ doc.get("custom_iban") or "" }}}}</div></td>
<td class="r" style="width:50%;vertical-align:top"><strong>Total</strong> {{{{ doc.get_formatted("grand_total") if doc.get_formatted is defined else doc.grand_total or doc.paid_amount or doc.total or "" }}}}</td>
</tr></table>
{in_words}{terms}
{DOC_BARCODE_SNIPPET}
</div>
"""


def _items_block(profile: DocTypeProfile) -> str:
	if not profile.has_items:
		if profile.doc_type == "Payment Entry":
			return """<table class="sp-table"><tr><th>Description</th><th class="r">Amount</th></tr>
<tr><td>Payment — {{ doc.party_name or doc.party or "" }} ({{ doc.payment_type or "" }})</td><td class="r">{{ doc.get_formatted("paid_amount") if doc.get_formatted is defined else doc.paid_amount or "" }}</td></tr>
{% if doc.references %}<tr><td colspan="2" style="font-size:8px;color:#6b7280">{% for ref in doc.references %}{{ ref.reference_doctype }} {{ ref.reference_name }}{% if not loop.last %}, {% endif %}{% endfor %}</td></tr>{% endif %}</table>"""
		if profile.doc_type == "Journal Entry":
			return """{% if doc.accounts %}<table class="sp-table"><tr><th>Account</th><th class="r">Debit</th><th class="r">Credit</th></tr>
{% for row in doc.accounts %}<tr><td>{{ row.account or "" }}</td><td class="r">{{ row.get_formatted("debit_in_account_currency") if row.get_formatted is defined else row.debit_in_account_currency or "" }}</td><td class="r">{{ row.get_formatted("credit_in_account_currency") if row.get_formatted is defined else row.credit_in_account_currency or "" }}</td></tr>{% endfor %}
</table>{% endif %}"""
		return ""
	return """
{% if doc.items %}<table class="sp-table"><thead><tr><th>Description</th><th class="r">Qty</th><th class="r">Rate</th><th class="r">Amount</th></tr></thead><tbody>
{% for row in doc.items %}<tr><td>{{ row.item_name or row.item_code or row.description or "" }}</td><td class="r">{{ row.qty or "" }}</td><td class="r">{{ row.get_formatted("rate", doc) if row.get_formatted is defined else row.rate or "" }}</td><td class="r">{{ row.get_formatted("amount", doc) if row.get_formatted is defined else row.amount or "" }}</td></tr>{% endfor %}
</tbody></table>{% endif %}"""


def _totals_block(profile: DocTypeProfile) -> str:
	if not profile.has_items or profile.doc_type == "Payment Entry":
		return ""
	if not profile.has_taxes:
		return """<div class="r" style="margin-top:8px"><strong>Total:</strong> {{ doc.get_formatted("grand_total") if doc.get_formatted is defined else doc.grand_total or "" }}</div>"""
	return """
<div class="r" style="margin-top:8px">
Net: {{ doc.get_formatted("net_total") if doc.get_formatted is defined else doc.net_total or "" }}<br>
{% for tax in doc.taxes or [] %}{{ tax.description or "Tax" }}: {{ tax.get_formatted("tax_amount") if tax.get_formatted is defined else tax.tax_amount or "" }}<br>{% endfor %}
<strong>Grand Total: {{ doc.get_formatted("grand_total") if doc.get_formatted is defined else doc.grand_total or "" }}</strong>
</div>"""


def _render_thermal(profile: DocTypeProfile, pack: dict, party: str, date_field: str, title: str) -> str:
	accent = pack["accent"]
	return f"""{{# Thermal {pack["label"]} · {profile.doc_type} #}}
{{% set title = "{title}" %}}
{{% set date_field = "{date_field}" %}}
{party}
<style>
@page {{ size: 80mm auto; margin: 2mm; }}
.th-root {{ font-family: monospace, Arial; font-size: 11px; width: 72mm; margin: 0 auto; color: #111; }}
.th-co {{ font-size: 14px; font-weight: 800; text-align: center; border-bottom: 2px solid {accent}; padding-bottom: 4px; }}
.th-meta {{ text-align: center; font-size: 10px; margin: 6px 0; }}
.th-line {{ border-top: 1px dashed #999; margin: 6px 0; }}
.th-item {{ display: block; font-size: 10px; margin: 4px 0; overflow: hidden; }}
.th-item-name {{ display: block; word-wrap: break-word; overflow-wrap: anywhere; white-space: normal; max-width: 72mm; line-height: 1.25; padding-right: 2mm; }}
.th-item-amt {{ display: block; text-align: right; font-weight: 600; margin-top: 1px; }}
.th-total {{ background: {accent}; color: #fff; text-align: center; padding: 8px; font-size: 14px; font-weight: 800; margin-top: 8px; }}
.th-qr {{ text-align: center; margin: 6px 0; font-size: 9px; color: {accent}; }}
.th-bc {{ text-align: center; margin: 4px 0; }}
.th-bc img {{ max-width: 64mm; height: 12mm; }}
</style>
<div class="th-root print-format">
<div class="th-co">{{{{ doc.company or "" }}}}</div>
<div class="th-meta">{{{{ title }}}}<br>{{{{ doc.name }}}} · {{{{ frappe.utils.formatdate(doc.get(date_field)) if doc.get(date_field) else "" }}}}</div>
{{% set _th_bc = frappe.call("erpnext_print_pack.print_barcodes.get_doc_barcode_data_uri", value=doc.name) %}}
{{% if _th_bc %}}<div class="th-bc"><img src="{{{{ _th_bc }}}}" alt="{{{{ doc.name }}}}"></div>{{% endif %}}
<div class="th-line"></div>
<div style="font-size:10px;word-wrap:break-word;overflow-wrap:anywhere">{{{{ party_label }}}}: {{{{ party_name }}}}</div>
<div class="th-line"></div>
{{% if doc.items %}}{{% for row in doc.items %}}<div class="th-item"><span class="th-item-name">{{{{ row.item_name or row.item_code or "" }}}} x {{{{ row.qty or "" }}}}</span><span class="th-item-amt">{{{{ row.get_formatted("amount", doc) if row.get_formatted is defined else row.amount or "" }}}}</span></div>{{% endfor %}}
{{% elif doc.doc_type == "Payment Entry" %}}<div class="th-item"><span class="th-item-name">{{{{ doc.payment_type or "Payment" }}}} · {{{{ doc.party_name or doc.party or "" }}}}</span><span class="th-item-amt">{{{{ doc.get_formatted("paid_amount") if doc.get_formatted is defined else doc.paid_amount or "" }}}}</span></div>
{{% elif doc.accounts %}}{{% for row in doc.accounts %}}{{% if row.debit_in_account_currency or row.credit_in_account_currency %}}<div class="th-item"><span class="th-item-name">{{{{ row.account or "" }}}}</span><span class="th-item-amt">{{{{ row.debit_in_account_currency or row.credit_in_account_currency or "" }}}}</span></div>{{% endif %}}{{% endfor %}}{{% endif %}}
<div class="th-total">TOTAL {{{{ doc.get_formatted("grand_total") if doc.get_formatted is defined else doc.grand_total or doc.paid_amount or "" }}}}</div>
{{% set _th_qr = "" %}}{{% if doc.get("custom_fbr_invoice_no") %}}{{% set _fbr_th = frappe.call("erpnext_print_pack.print_barcodes.get_qr_and_barcode_data_uri", value=doc.custom_fbr_invoice_no, include_fbr_url=1) %}}{{% if _fbr_th %}}{{% set _th_qr = _fbr_th.get("qr") or "" %}}{{% endif %}}{{% endif %}}
{{% if _th_qr %}}<div class="th-qr epp-qr qr"><img src="{{{{ _th_qr }}}}" style="width:72px;height:72px" alt="FBR QR"></div>{{% else %}}<div class="th-qr epp-qr qr">{pack["region"]} E-Invoice · QR</div>{{% endif %}}
<div style="text-align:center;font-size:9px;margin-top:6px">Thank you</div>
</div>
"""
