"""Print layouts matching README preview designs — ZATCA bilingual & Regional tax invoice."""

from __future__ import annotations

from erpnext_print_pack.doctype_profiles import DocTypeProfile
from erpnext_print_pack.layout_engine import _party_vars
from erpnext_print_pack.print_snippets import DOC_BARCODE_SNIPPET

PREVIEW_LAYOUTS = {
	"readme_zatca_tax": {
		"label": "ZATCA Tax Invoice",
		"region": "SA",
		"layout_type": "specimen",
		"description": "Bilingual ZATCA e-invoice — matches README preview (Arabic/English, QR, VAT blocks)",
	},
	"readme_regional_tax": {
		"label": "Regional Tax Invoice",
		"region": "ALL",
		"layout_type": "regional",
		"description": "Global tax invoice — navy corporate style matching README preview (Bill/Ship, HSN, tax summary)",
	},
}


def format_name(profile: DocTypeProfile, layout_key: str) -> str:
	return f"{PREVIEW_LAYOUTS[layout_key]['label']} {profile.title}"


def format_slug(profile: DocTypeProfile, layout_key: str) -> str:
	return f"{profile.slug}_{layout_key}"


def render_preview(profile: DocTypeProfile, layout_key: str) -> str:
	if layout_key == "readme_zatca_tax":
		return _render_zatca_tax(profile)
	return _render_regional_tax(profile)


def _items_zatca(profile: DocTypeProfile) -> str:
	if not profile.has_items:
		return ""
	return """
{% if doc.items %}
<table class="zt-table">
<thead><tr>
<th>#</th><th>البند / Item</th><th class="r">الكمية<br>Qty</th><th class="r">الوحدة<br>Unit</th>
<th class="r">سعر الوحدة<br>Unit Price</th><th class="r">قبل الضريبة<br>Before Tax</th>
<th class="r">نسبة<br>Tax %</th><th class="r">الضريبة<br>Tax</th><th class="r">الإجمالي<br>Total</th>
</tr></thead>
<tbody>
{% for row in doc.items %}
{% set line_net = row.net_amount if row.net_amount is not none else (row.amount or 0) %}
{% set line_tax = (row.get("tax_amount") or 0) %}
{% set line_total = (line_net or 0) + (line_tax or 0) %}
{% set tax_rate = row.item_tax_rate if row.item_tax_rate is not none else (row.tax_rate if row.tax_rate is defined else "") %}
<tr>
<td>{{ loop.index }}</td>
<td>{{ row.item_name or row.item_code or row.description or "" }}{% if row.get("custom_item_name_ar") %}<br><span class="ar">{{ row.custom_item_name_ar }}</span>{% endif %}</td>
<td class="r">{{ row.qty or "" }}</td>
<td class="r">{{ row.uom or row.stock_uom or "" }}</td>
<td class="r">{{ row.get_formatted("rate", doc) if row.get_formatted is defined else row.rate or "" }}</td>
<td class="r">{{ row.get_formatted("net_amount", doc) if row.get_formatted is defined else line_net or "" }}</td>
<td class="r">{{ tax_rate }}{% if tax_rate %}%{% endif %}</td>
<td class="r">{{ row.get_formatted("tax_amount", doc) if row.get_formatted is defined and row.tax_amount is defined else line_tax or "" }}</td>
<td class="r">{{ row.get_formatted("amount", doc) if row.get_formatted is defined else line_total or "" }}</td>
</tr>
{% endfor %}
</tbody>
</table>
{% endif %}"""


def _items_regional(profile: DocTypeProfile) -> str:
	if not profile.has_items:
		return ""
	return """
{% if doc.items %}
<table class="rt-table">
<thead><tr>
<th>#</th><th>Description</th><th>HSN/SAC</th><th class="r">Qty</th><th>Unit</th>
<th class="r">Unit Price</th><th class="r">Amount</th>
</tr></thead>
<tbody>
{% for row in doc.items %}
<tr>
<td>{{ loop.index }}</td>
<td><strong>{{ row.item_name or row.item_code or row.description or "" }}</strong>{% if row.description and row.description != (row.item_name or row.item_code) %}<br><small>{{ row.description }}</small>{% endif %}</td>
<td>{{ row.gst_hsn_code or row.item_code or "" }}</td>
<td class="r">{{ row.qty or "" }}</td>
<td>{{ row.uom or row.stock_uom or "" }}</td>
<td class="r">{{ row.get_formatted("rate", doc) if row.get_formatted is defined else row.rate or "" }}</td>
<td class="r">{{ row.get_formatted("amount", doc) if row.get_formatted is defined else row.amount or "" }}</td>
</tr>
{% endfor %}
</tbody>
</table>
{% endif %}"""


def _totals_zatca(profile: DocTypeProfile) -> str:
	if not profile.has_items:
		return ""
	return """
<div class="zt-totals-wrap">
<table class="zt-totals">
<tr><td>Total Before Tax / الإجمالي قبل الضريبة</td><td class="r">{{ doc.get_formatted("net_total") if doc.get_formatted is defined else doc.net_total or "" }}</td></tr>
{% for tax in doc.taxes or [] %}
<tr><td>{{ tax.description or "VAT" }} / ضريبة</td><td class="r">{{ tax.get_formatted("tax_amount") if tax.get_formatted is defined else tax.tax_amount or "" }}</td></tr>
{% endfor %}
<tr class="zt-grand"><td>Total Including Tax / الإجمالي شامل الضريبة</td><td class="r">{{ doc.get_formatted("grand_total") if doc.get_formatted is defined else doc.grand_total or "" }}</td></tr>
</table>
</div>"""


def _totals_regional(profile: DocTypeProfile) -> str:
	if not profile.has_items:
		return ""
	return """
<div class="rt-totals-area">
<table class="rt-totals">
<tr><td>Subtotal</td><td class="r">{{ doc.get_formatted("net_total") if doc.get_formatted is defined else doc.net_total or "" }}</td></tr>
{% for tax in doc.taxes or [] %}
<tr><td>{{ tax.description or tax.account_head or "Tax" }}</td><td class="r">{{ tax.get_formatted("tax_amount") if tax.get_formatted is defined else tax.tax_amount or "" }}</td></tr>
{% endfor %}
<tr class="rt-grand"><td>TOTAL AMOUNT</td><td class="r">{{ doc.get_formatted("grand_total") if doc.get_formatted is defined else doc.grand_total or "" }}</td></tr>
</table>
</div>"""


def _render_zatca_tax(profile: DocTypeProfile) -> str:
	party = _party_vars(profile)
	items = _items_zatca(profile)
	totals = _totals_zatca(profile)
	in_words = (
		'{% if doc.in_words %}<div class="zt-words"><strong>In Words:</strong> {{ doc.in_words }}<br><span class="ar">{% if doc.in_words_ar %}{{ doc.in_words_ar }}{% endif %}</span></div>{% endif %}'
		if profile.has_in_words
		else ""
	)
	doc_title = profile.title
	return f"""{{# README ZATCA Tax Invoice · {profile.doc_type} #}}
{{% set title = "{doc_title}" %}}
{{% set date_field = "{profile.date_field}" %}}
{party}
<style>
@page {{ size: A4 portrait; margin: 8mm; }}
.zt-root {{ font-family: 'Segoe UI', Tahoma, Arial, sans-serif; font-size: 9px; color: #1a1a1a; }}
.ar {{ direction: rtl; font-family: Tahoma, Arial, sans-serif; }}
.zt-top {{ display: flex; align-items: flex-start; justify-content: space-between; border-bottom: 3px solid #006c35; padding-bottom: 10px; margin-bottom: 12px; }}
.zt-logo {{ display: flex; align-items: center; gap: 8px; }}
.zt-logo-mark {{ width: 52px; height: 52px; border-radius: 8px; background: linear-gradient(135deg,#006c35,#004d25); color: #fff; font-weight: 800; font-size: 11px; display: flex; align-items: center; justify-content: center; text-align: center; line-height: 1.1; }}
.zt-title {{ text-align: center; flex: 1; }}
.zt-title h1 {{ margin: 0; font-size: 22px; color: #1e3a8a; }}
.zt-title .sub {{ color: #006c35; font-weight: 700; font-size: 11px; margin-top: 4px; }}
.zt-qr {{ width: 96px; height: 96px; border: 1px solid #d1d5db; border-radius: 6px; display: flex; align-items: center; justify-content: center; background: #fff; }}
.zt-qr img {{ width: 88px; height: 88px; }}
.zt-grid {{ display: flex; gap: 10px; margin-bottom: 10px; }}
.zt-box {{ flex: 1; border: 1px solid #cbd5e1; }}
.zt-box-h {{ background: #1e3a8a; color: #fff; padding: 5px 8px; font-weight: 700; font-size: 9px; }}
.zt-box-b {{ padding: 8px; line-height: 1.45; min-height: 72px; }}
.zt-info {{ width: 34%; border: 1px solid #cbd5e1; margin-bottom: 10px; margin-left: auto; }}
.zt-info td {{ padding: 4px 8px; border-bottom: 1px solid #e5e7eb; font-size: 8px; }}
.zt-info td:first-child {{ color: #64748b; width: 42%; }}
.zt-table {{ width: 100%; border-collapse: collapse; margin: 8px 0; }}
.zt-table th {{ background: #1e3a8a; color: #fff; padding: 6px 4px; font-size: 7px; text-align: left; vertical-align: bottom; }}
.zt-table td {{ border-bottom: 1px solid #e5e7eb; padding: 5px 4px; font-size: 8px; }}
.zt-totals-wrap {{ display: flex; justify-content: flex-end; margin-top: 8px; }}
.zt-totals {{ width: 52%; border-collapse: collapse; }}
.zt-totals td {{ padding: 5px 8px; border: 1px solid #e5e7eb; }}
.zt-totals .zt-grand td {{ background: #006c35; color: #fff; font-weight: 800; font-size: 11px; }}
.zt-words {{ margin-top: 10px; font-size: 9px; line-height: 1.5; }}
.zt-meta {{ margin-top: 12px; border-top: 1px solid #e5e7eb; padding-top: 8px; font-size: 7px; color: #64748b; }}
.zt-meta b {{ color: #334155; }}
.zt-foot {{ text-align: center; margin-top: 8px; font-size: 8px; color: #006c35; font-weight: 600; }}
.r {{ text-align: right; }}
.epp-sig,.sig {{ display: none; }}
</style>
<div class="zt-root print-format">
<div class="zt-top">
  <div class="zt-logo">
    <div class="zt-logo-mark">ZATCA<br>KSA</div>
    <div style="font-size:8px;color:#64748b">Zakat, Tax and<br>Customs Authority</div>
  </div>
  <div class="zt-title">
    <h1><span class="ar">فاتورة ضريبية</span> / Tax Invoice</h1>
    <div class="sub"><span class="ar">(ضريبية)</span> / (Tax)</div>
  </div>
  <div class="zt-qr epp-qr qr">
    {{% set qr = doc.get("ksa_einv_qr") or doc.get("custom_qr_code") or "" %}}
    {{% if not qr %}}{{% set _qrp = frappe.call("erpnext_print_pack.print_barcodes.get_qr_and_barcode_data_uri", value=doc.name) %}}{{% if _qrp %}}{{% set qr = _qrp.get("qr") or "" %}}{{% endif %}}{{% endif %}}
    {{% if qr %}}<img src="{{{{ qr }}}}">{{% else %}}QR{{% endif %}}
  </div>
</div>
<div class="zt-grid">
  <div class="zt-box"><div class="zt-box-h">Seller / البائع</div><div class="zt-box-b"><strong>{{{{ doc.company or "" }}}}</strong><br>VAT ID: {{{{ doc.company_tax_id or "" }}}}<br>{{{{ doc.company_address_display or "" }}}}<br>CR: {{{{ doc.get("custom_company_cr_number") or "" }}}}</div></div>
  <div class="zt-box"><div class="zt-box-h">{{{{ party_label }}}} / المشتري</div><div class="zt-box-b"><strong>{{{{ party_name }}}}</strong><br>VAT ID: {{{{ doc.tax_id or doc.customer_tax_id or "" }}}}<br>{{{{ party_address }}}}</div></div>
</div>
<table class="zt-info"><tr><td>Invoice Number</td><td><b>{{{{ doc.name }}}}</b></td></tr>
<tr><td>Invoice Date</td><td>{{{{ frappe.utils.formatdate(doc.get(date_field)) if doc.get(date_field) else "" }}}}</td></tr>
<tr><td>Invoice Time</td><td>{{{{ doc.posting_time or "" }}}}</td></tr>
<tr><td>Invoice Type</td><td>{{{{ doc.is_return and "Credit Note" or title }}}}</td></tr>
<tr><td>Currency</td><td>{{{{ doc.currency or "" }}}}</td></tr></table>
{items}
<div style="display:flex;gap:12px;align-items:flex-start">
  <div style="flex:1">{in_words}</div>
  <div style="flex:1">{totals}</div>
</div>
<div class="zt-meta">
  <b>UUID:</b> {{{{ doc.get("uuid") or doc.name }}}}&nbsp;&nbsp;
  <b>Software ID:</b> ERPNext Print Pack&nbsp;&nbsp;
  <b>Sequence:</b> {{{{ doc.name }}}}&nbsp;&nbsp;
  <b>Environment:</b> Production
</div>
<div class="zt-foot"><span class="ar">تم إنشاء هذه الفاتورة الإلكترونية وفقاً لمتطلبات هيئة الزكاة والضريبة والجمارك</span><br>This e-invoice has been generated in compliance with ZATCA e-invoicing requirements.</div>
{DOC_BARCODE_SNIPPET}
</div>"""


def _render_regional_tax(profile: DocTypeProfile) -> str:
	party = _party_vars(profile)
	items = _items_regional(profile)
	totals = _totals_regional(profile)
	in_words = (
		'{% if doc.in_words %}<div class="rt-words"><strong>Amount in Words:</strong><br>{{ doc.in_words }}</div>{% endif %}'
		if profile.has_in_words
		else ""
	)
	terms = (
		'{% if doc.terms %}<div class="rt-terms"><strong>TERMS &amp; CONDITIONS</strong><br>{{ doc.terms }}</div>{% endif %}'
		if profile.has_terms
		else '<div class="rt-terms"><strong>TERMS &amp; CONDITIONS</strong><br>Payment due as per invoice date. Goods once sold will not be taken back.</div>'
	)
	due_row = '{% if doc.due_date %}<tr><td>Due Date</td><td>{{ frappe.utils.formatdate(doc.due_date) }}</td></tr>{% endif %}' if profile.has_due_date else ""
	ship_block = """
{% if ship_label and ship_address %}
<div class="rt-party"><div class="rt-party-h">SHIP TO</div><div class="rt-party-b">{{ ship_address }}</div></div>
{% endif %}""" if profile.has_party_customer else ""
	logo_block = """
{% set logo = frappe.db.get_value("Company", doc.company, "company_logo") if doc.company else "" %}
{% if logo %}<img src="{{ logo }}" style="max-height:46px;max-width:120px">{% else %}<div class="rt-logo">{{ (doc.company or "C")[:1] }}</div>{% endif %}"""
	bank_block = """
{% set bank = frappe.get_all("Bank Account", filters={"company": doc.company, "is_company_account": 1}, fields=["account_name","bank","bank_account_no","iban"], limit=1) %}
{% if bank %}Bank: {{ bank[0].bank or "" }}<br>Account: {{ bank[0].account_name or "" }}<br>A/C No: {{ bank[0].bank_account_no or "" }}<br>IBAN: {{ bank[0].iban or "" }}{% else %}—{% endif %}"""
	return f"""{{# README Regional Tax Invoice · {profile.doc_type} #}}
{{% set title = "{profile.title}" %}}
{{% set date_field = "{profile.date_field}" %}}
{party}
<style>
@page {{ size: A4 portrait; margin: 8mm; }}
.rt-root {{ font-family: 'Segoe UI', Arial, sans-serif; font-size: 9px; color: #1e293b; }}
.rt-head {{ border-top: 6px solid #0f2744; border-bottom: 2px solid #0f2744; padding: 10px 0 12px; display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px; }}
.rt-brand {{ display: flex; gap: 10px; align-items: center; }}
.rt-logo {{ width: 46px; height: 46px; background: #0f2744; color: #fff; font-size: 22px; font-weight: 800; display: flex; align-items: center; justify-content: center; clip-path: polygon(25% 0%, 75% 0%, 100% 50%, 75% 100%, 25% 100%, 0% 50%); }}
.rt-co {{ font-size: 16px; font-weight: 800; color: #0f2744; letter-spacing: 0.5px; }}
.rt-co-meta {{ font-size: 8px; color: #64748b; line-height: 1.5; margin-top: 4px; max-width: 340px; }}
.rt-doc-title {{ font-size: 28px; font-weight: 800; color: #0f2744; text-align: right; line-height: 1; }}
.rt-meta {{ width: 100%; margin: 8px 0 12px; border-collapse: collapse; }}
.rt-meta td {{ padding: 3px 8px; font-size: 8px; border: 1px solid #e2e8f0; }}
.rt-meta td:first-child {{ background: #f8fafc; color: #64748b; width: 120px; }}
.rt-parties {{ display: flex; gap: 12px; margin-bottom: 10px; }}
.rt-party {{ flex: 1; border: 1px solid #e2e8f0; }}
.rt-party-h {{ background: #0f2744; color: #fff; padding: 5px 8px; font-weight: 700; font-size: 9px; }}
.rt-party-b {{ padding: 8px; line-height: 1.45; min-height: 64px; }}
.rt-party-b strong {{ font-size: 10px; }}
.rt-table {{ width: 100%; border-collapse: collapse; margin: 8px 0; }}
.rt-table th {{ background: #0f2744; color: #fff; padding: 7px 5px; font-size: 8px; text-align: left; }}
.rt-table td {{ border-bottom: 1px solid #e2e8f0; padding: 6px 5px; font-size: 8px; }}
.rt-bottom {{ display: flex; gap: 10px; margin-top: 10px; align-items: flex-start; }}
.rt-words {{ flex: 1; font-size: 9px; line-height: 1.45; }}
.rt-totals-area {{ width: 42%; margin-left: auto; }}
.rt-totals {{ width: 100%; border-collapse: collapse; }}
.rt-totals td {{ padding: 5px 8px; border: 1px solid #e2e8f0; }}
.rt-totals .rt-grand td {{ background: #0f2744; color: #fff; font-weight: 800; font-size: 12px; }}
.rt-footer-row {{ display: flex; gap: 10px; margin-top: 12px; }}
.rt-bank, .rt-terms {{ flex: 1; border: 1px solid #e2e8f0; padding: 8px; font-size: 8px; line-height: 1.45; }}
.rt-bank strong, .rt-terms strong {{ color: #0f2744; display: block; margin-bottom: 4px; }}
.rt-sign {{ flex: 1; text-align: center; font-size: 8px; padding-top: 24px; }}
.rt-bar {{ background: #0f2744; color: #fff; text-align: center; padding: 8px; margin-top: 12px; font-style: italic; font-size: 10px; }}
.r {{ text-align: right; }}
</style>
<div class="rt-root print-format">
<div class="rt-head">
  <div>
    <div class="rt-brand">
      {logo_block}
      <div><div class="rt-co">{{{{ doc.company or "" }}}}</div></div>
    </div>
    <div class="rt-co-meta">{{{{ doc.company_address_display or "" }}}}<br>Tax ID: {{{{ doc.company_tax_id or "" }}}}</div>
  </div>
  <div><div class="rt-doc-title">TAX INVOICE</div></div>
</div>
<table class="rt-meta" style="width:55%;margin-left:auto">
<tr><td>Invoice No.</td><td><b>{{{{ doc.name }}}}</b></td></tr>
<tr><td>Invoice Date</td><td>{{{{ frappe.utils.formatdate(doc.get(date_field)) if doc.get(date_field) else "" }}}}</td></tr>
{due_row}
<tr><td>PO Number</td><td>{{{{ doc.po_no or "" }}}}</td></tr>
<tr><td>Place of Supply</td><td>{{{{ doc.place_of_supply or "" }}}}</td></tr>
<tr><td>Currency</td><td>{{{{ doc.currency or "" }}}}</td></tr>
</table>
<div class="rt-parties">
  <div class="rt-party"><div class="rt-party-h">{{{{ party_label or "BILL TO" }}}}</div><div class="rt-party-b"><strong>{{{{ party_name }}}}</strong><br>{{{{ party_address }}}}</div></div>
  {ship_block}
</div>
{items}
<div class="rt-bottom">
  {in_words}
  {totals}
</div>
<div class="rt-footer-row">
  <div class="rt-bank"><strong>BANK DETAILS</strong><br>
    {bank_block}
  </div>
  {terms}
  <div class="rt-sign">For {{{{ doc.company or "" }}}}<br><br>_________________________<br>Authorized Signatory</div>
</div>
<div class="rt-bar">Thank you for your business!</div>
{DOC_BARCODE_SNIPPET}
</div>"""
