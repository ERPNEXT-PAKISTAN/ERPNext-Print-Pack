"""E-invoice specimen templates for all DocTypes — SA, UAE, Proforma, Thermal."""

from __future__ import annotations

from erpnext_print_pack.doctype_profiles import DocTypeProfile
from erpnext_print_pack.layout_engine import _party_vars
from erpnext_print_pack.page_fit_css import PAGE_FIT_CSS
from erpnext_print_pack.print_snippets import DOC_BARCODE_SNIPPET, THERMAL_DOC_BARCODE_SNIPPET

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

	if profile.doc_type == "Payment Entry":
		return _render_payment_specimen(profile, pack, party, date_field, title, doc_label)

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
@page {{ size: A4 portrait; margin: 8mm; }}
.sp-root {{ font-family: 'Segoe UI', Arial, sans-serif; font-size: 10px; color: #1f2937; }}
.sp-title {{ font-size: 28px; font-weight: 800; margin: 0 0 8px; }}
.sp-meta {{ color: #6b7280; font-size: 10px; }} .sp-meta b {{ color: #111; }}
.sp-badge {{ width: 84px; height: 84px; border: 3px solid {accent}; border-radius: 50%; text-align: center; margin-left: auto; font-weight: 800; color: {accent}; padding-top: 22px; line-height: 1.2; font-size: 10px; }}
.sp-card {{ background: #f9fafb; border: 1px solid #e5e7eb; border-radius: 10px; padding: 10px 12px; width: 48%; display: inline-block; vertical-align: top; min-height: 72px; }}
.sp-card .lbl {{ color: {accent}; font-weight: 700; margin-bottom: 6px; }}
.sp-qr {{ width: 96px; height: 96px; border: 1px solid #e5e7eb; border-radius: 8px; margin: 0 auto; text-align: center; line-height: 96px; color: #9ca3af; }}
.sp-table {{ width: 100%; border-collapse: collapse; margin: 12px 0; table-layout: fixed; }}
.sp-table th {{ background: {accent}; color: #fff; padding: 6px 4px; text-align: left; font-size: 8px; }}
.sp-table td {{ padding: 5px 4px; border-bottom: 1px solid #e5e7eb; font-size: 9px; }}
.r {{ text-align: right; }}
.sp-bank {{ background: #f9fafb; border-radius: 10px; padding: 10px; border: 1px solid #e5e7eb; }}
.sp-bank .lbl {{ color: {accent}; font-weight: 700; }}
.epp-sig,.sig,.epp-footer,.footer {{ display: none; }}
{PAGE_FIT_CSS}
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
	from erpnext_print_pack.detail_blocks import detail_table

	return detail_table(profile).replace('class="items"', 'class="items sp-table"')


def _totals_block(profile: DocTypeProfile) -> str:
	from erpnext_print_pack.detail_blocks import totals_block

	# Payment specimen layouts already embed amount prominently.
	if profile.doc_type == "Payment Entry":
		return ""
	return totals_block(profile).replace('class="totals"', 'class="totals sp-table"')


def _payment_amount_expr() -> str:
	return """{% set _pay_amt = doc.paid_amount or doc.received_amount or doc.base_paid_amount or 0 %}{% set _pay_cur = doc.paid_to_account_currency or doc.paid_from_account_currency or doc.company_currency or "" %}{{ frappe.utils.fmt_money(_pay_amt, currency=_pay_cur) if _pay_amt else "" }}"""


def _payment_account_expr() -> str:
	return """{% if doc.payment_type == "Receive" %}{{ doc.paid_to or "" }}{% elif doc.payment_type == "Pay" %}{{ doc.paid_from or "" }}{% else %}{{ doc.paid_from or "" }}{% if doc.paid_from and doc.paid_to %} → {% endif %}{{ doc.paid_to or "" }}{% endif %}"""


def _payment_details_table() -> str:
	amt = _payment_amount_expr()
	acct = _payment_account_expr()
	return f"""
<table class="sp-table">
<tr><th>Payment Type</th><th class="r">Amount</th></tr>
<tr>
  <td><span class="sp-pay-type">{{{{ doc.payment_type or "Payment" }}}}</span><br>
    <strong class="sp-party-name">{{{{ doc.party_name or doc.party or "" }}}}</strong><br>
    <span style="color:#6b7280">Mode: <b>{{{{ doc.mode_of_payment or "—" }}}}</b></span><br>
    <span style="color:#6b7280">Account: <b>{acct}</b></span>
  </td>
  <td class="r"><span class="sp-pay-amt">{amt}</span></td>
</tr>
{{% if doc.references %}}
<tr><td colspan="2" style="font-size:8px;color:#6b7280">References: {{% for ref in doc.references %}}{{{{ ref.reference_doctype }}}} {{{{ ref.reference_name }}}}{{% if not loop.last %}}, {{% endif %}}{{% endfor %}}</td></tr>
{{% endif %}}
</table>"""


def _render_payment_specimen(
	profile: DocTypeProfile, pack: dict, party: str, date_field: str, title: str, doc_label: str
) -> str:
	accent = pack["accent"]
	amt = _payment_amount_expr()
	acct = _payment_account_expr()
	return f"""{{# Payment specimen · Payment Entry #}}
{{% set title = "{title}" %}}
{{% set date_field = "{date_field}" %}}
{{% set doc_label = "{doc_label}" %}}
{party}
<style>
@page {{ size: A4 portrait; margin: 8mm; }}
.sp-root {{ font-family: 'Segoe UI', Arial, sans-serif; font-size: 10px; color: #1f2937; }}
.sp-title {{ font-size: 28px; font-weight: 800; margin: 0 0 8px; }}
.sp-meta {{ color: #6b7280; font-size: 10px; }} .sp-meta b {{ color: #111; }}
.sp-badge {{ width: 84px; height: 84px; border: 3px solid {accent}; border-radius: 50%; text-align: center; margin-left: auto; font-weight: 800; color: {accent}; padding-top: 22px; line-height: 1.2; font-size: 10px; }}
.sp-card {{ background: #f9fafb; border: 1px solid #e5e7eb; border-radius: 10px; padding: 10px 12px; }}
.sp-card .lbl {{ color: {accent}; font-weight: 700; margin-bottom: 6px; }}
.sp-pay-type {{ font-size: 18px; font-weight: 800; color: {accent}; text-transform: uppercase; }}
.sp-party-name {{ font-size: 14px; font-weight: 800; display: block; margin: 8px 0 4px; }}
.sp-pay-amt {{ font-size: 20px; font-weight: 800; color: #111; }}
.sp-table {{ width: 100%; border-collapse: collapse; margin: 12px 0; table-layout: fixed; }}
.sp-table th {{ background: {accent}; color: #fff; padding: 6px 4px; text-align: left; font-size: 8px; }}
.sp-table td {{ padding: 6px 4px; border-bottom: 1px solid #e5e7eb; font-size: 9px; vertical-align: top; }}
.r {{ text-align: right; }}
.epp-sig,.sig,.epp-footer,.footer {{ display: none; }}
{PAGE_FIT_CSS}
</style>
<div class="sp-root print-format">
<table style="width:100%;margin-bottom:16px"><tr>
<td style="width:70%"><div class="sp-title">{{{{ doc_label }}}}</div>
<div class="sp-meta">No <b>{{{{ doc.name }}}}</b> · Date <b>{{{{ frappe.utils.formatdate(doc.get(date_field)) if doc.get(date_field) else "" }}}}</b></div>
<div class="sp-pay-type" style="margin-top:10px">{{{{ doc.payment_type or "Payment" }}}}</div></td>
<td style="width:30%;text-align:right"><div class="sp-badge">{pack["badge"]}<br><span style="font-size:8px">{pack["badge_sub"]}</span></div></td>
</tr></table>
<div class="sp-card" style="margin-bottom:12px">
  <div class="lbl">{{{{ party_label }}}}</div>
  <strong class="sp-party-name">{{{{ party_name }}}}</strong>
  {{% if party_address %}}<br><span style="color:#6b7280;font-size:9px">{{{{ party_address }}}}</span>{{% endif %}}
</div>
{_payment_details_table()}
<table style="width:100%;margin-top:8px"><tr>
<td><span style="color:#6b7280">Mode of Payment</span><br><strong>{{{{ doc.mode_of_payment or "—" }}}}</strong></td>
<td><span style="color:#6b7280">Bank / Cash Account</span><br><strong>{acct}</strong></td>
<td class="r"><span style="color:#6b7280">Amount</span><br><span class="sp-pay-amt">{amt}</span></td>
</tr></table>
{DOC_BARCODE_SNIPPET}
</div>
"""


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
.th-bc {{ text-align: center; margin: 3px auto; max-width: 68mm; width: 100%; overflow: hidden; }}
.th-pay-type {{ font-size: 16px; font-weight: 800; text-align: center; margin: 4px 0; color: {accent}; text-transform: uppercase; }}
.th-party {{ font-size: 13px; font-weight: 800; text-align: center; margin: 4px 0; word-wrap: break-word; }}
.th-mop {{ font-size: 10px; text-align: center; margin: 2px 0; }}
.th-acct {{ font-size: 9px; text-align: center; color: #555; word-wrap: break-word; overflow-wrap: anywhere; }}
.th-pay-amt {{ font-size: 16px; font-weight: 800; text-align: center; margin: 6px 0; }}
.th-bc img, .epp-voucher-barcode img {{ display: block; margin: 0 auto; max-width: 56mm !important; width: 56mm !important; height: 8mm !important; max-height: 8mm !important; object-fit: fill; }}
</style>
<div class="th-root print-format">
<div class="th-co">{{{{ doc.company or "" }}}}</div>
<div class="th-meta">{{{{ title }}}}<br>{{{{ doc.name }}}} · {{{{ frappe.utils.formatdate(doc.get(date_field)) if doc.get(date_field) else "" }}}}</div>
{THERMAL_DOC_BARCODE_SNIPPET}
<div class="th-line"></div>
{{% if doc.doc_type == "Payment Entry" %}}
<div class="th-pay-type">{{{{ doc.payment_type or "Payment" }}}}</div>
<div class="th-party">{{{{ doc.party_name or doc.party or "" }}}}</div>
<div class="th-mop">Mode: <b>{{{{ doc.mode_of_payment or "—" }}}}</b></div>
<div class="th-acct">{_payment_account_expr()}</div>
<div class="th-line"></div>
<div class="th-total">AMOUNT {_payment_amount_expr()}</div>
{{% else %}}
<div style="font-size:10px;word-wrap:break-word;overflow-wrap:anywhere">{{{{ party_label }}}}: {{{{ party_name }}}}</div>
<div class="th-line"></div>
{{% if doc.items %}}{{% for row in doc.items %}}<div class="th-item"><span class="th-item-name">{{{{ row.item_name or row.item_code or "" }}}} x {{{{ row.qty or "" }}}}</span><span class="th-item-amt">{{{{ row.get_formatted("amount", doc) if row.get_formatted is defined else row.amount or "" }}}}</span></div>{{% endfor %}}{{% elif doc.accounts %}}{{% for row in doc.accounts %}}{{% if row.debit_in_account_currency or row.credit_in_account_currency %}}<div class="th-item"><span class="th-item-name">{{{{ row.account or "" }}}}</span><span class="th-item-amt">{{{{ row.debit_in_account_currency or row.credit_in_account_currency or "" }}}}</span></div>{{% endif %}}{{% endfor %}}{{% endif %}}
<div class="th-total">TOTAL {{{{ doc.get_formatted("grand_total") if doc.get_formatted is defined else doc.grand_total or doc.paid_amount or "" }}}}</div>
{{% endif %}}
{{% set _th_qr = "" %}}{{% if doc.get("custom_fbr_invoice_no") %}}{{% set _fbr_th = frappe.call("erpnext_print_pack.print_barcodes.get_qr_and_barcode_data_uri", value=doc.custom_fbr_invoice_no, include_fbr_url=1) %}}{{% if _fbr_th %}}{{% set _th_qr = _fbr_th.get("qr") or "" %}}{{% endif %}}{{% endif %}}
{{% if _th_qr %}}<div class="th-qr epp-qr qr"><img src="{{{{ _th_qr }}}}" style="width:72px;height:72px" alt="FBR QR"></div>{{% else %}}<div class="th-qr epp-qr qr">{pack["region"]} E-Invoice · QR</div>{{% endif %}}
<div style="text-align:center;font-size:9px;margin-top:6px">Thank you</div>
</div>
"""
