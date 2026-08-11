"""ZATCA Manrope tax invoice — shared HTML/CSS (English LTR, green brand, Phase 2 QR)."""

from __future__ import annotations

from erpnext_print_pack.doctype_profiles import DocTypeProfile
from erpnext_print_pack.print_snippets import DOC_BARCODE_SNIPPET

LAYOUT_KEY = "zatca_manrope"
LAYOUT_LABEL = "ZATCA Manrope Tax Invoice"
LAYOUT_META = {
	"label": LAYOUT_LABEL,
	"region": "SA",
	"layout_type": "specimen",
	"description": "English ZATCA tax invoice — Manrope font, meta strip, VAT columns, QR, bank details",
}


def format_name(profile: DocTypeProfile) -> str:
	return f"{LAYOUT_LABEL} {profile.title}"


def format_slug(profile: DocTypeProfile) -> str:
	return f"{profile.slug}_{LAYOUT_KEY}"


def render_zatca_manrope(profile: DocTypeProfile) -> str:
	if profile.has_party_customer:
		party_name = "{{ doc.customer_name or doc.customer or doc.party_name or \"\" }}"
		party_tax = "{{ doc.tax_id or doc.customer_tax_id or \"\" }}"
		party_address = "{{ doc.address_display or \"\" }}"
		party_label = "Bill To"
	elif profile.has_party_supplier:
		party_name = "{{ doc.supplier_name or doc.supplier or \"\" }}"
		party_tax = "{{ doc.tax_id or doc.supplier_tax_id or \"\" }}"
		party_address = "{{ doc.address_display or doc.supplier_address or \"\" }}"
		party_label = "Supplier"
	else:
		party_name = "{{ doc.party_name or doc.party or \"\" }}"
		party_tax = "{{ doc.tax_id or \"\" }}"
		party_address = "{{ doc.address_display or \"\" }}"
		party_label = "Party"

	items_block = ""
	if profile.has_items:
		items_block = """
{% if doc.items %}
<table class="items">
<thead>
<tr>
<th style="width:6%">#</th>
<th style="width:34%">Description</th>
<th class="num" style="width:9%">Qty</th>
<th class="num" style="width:14%">Unit Price</th>
<th class="num" style="width:10%">Discount</th>
<th class="num" style="width:9%">VAT %</th>
<th class="num" style="width:9%">VAT Amt</th>
<th class="num" style="width:13%">Total</th>
</tr>
</thead>
<tbody>
{% for row in doc.items %}
{% set line_net = row.net_amount if row.net_amount is not none else (row.amount or 0) %}
{% set line_disc = row.discount_amount or 0 %}
{% set tax_rate = row.item_tax_rate if row.item_tax_rate is not none else "" %}
{% set line_tax = row.get("tax_amount") or 0 %}
{% set line_total = (line_net or 0) + (line_tax or 0) %}
<tr>
<td>{{ loop.index }}</td>
<td class="desc">
<span class="item-title">{{ row.item_name or row.item_code or row.description or "" }}</span>
{% if row.description and row.description != (row.item_name or row.item_code) %}
<span class="item-sub">{{ row.description }}</span>
{% endif %}
</td>
<td class="num">{{ row.qty or "" }}</td>
<td class="num">{{ row.get_formatted("rate", doc) if row.get_formatted is defined else row.rate or "" }}</td>
<td class="num">{{ row.get_formatted("discount_amount", doc) if row.get_formatted is defined and row.discount_amount else line_disc or "0.00" }}</td>
<td class="num">{% if tax_rate %}{{ tax_rate }}%{% endif %}</td>
<td class="num">{{ row.get_formatted("tax_amount", doc) if row.get_formatted is defined and row.tax_amount is defined else line_tax or "" }}</td>
<td class="num">{{ row.get_formatted("amount", doc) if row.get_formatted is defined else line_total or "" }}</td>
</tr>
{% endfor %}
</tbody>
</table>
{% endif %}"""

	totals_taxes = ""
	if profile.has_taxes:
		totals_taxes = """
{% for tax in doc.taxes or [] %}
<div class="row"><div class="lbl">{{ tax.description or "VAT (15%)" }}</div><div class="val">{{ tax.get_formatted("tax_amount") if tax.get_formatted is defined else tax.tax_amount or "" }} {{ doc.currency or "" }}</div></div>
{% endfor %}"""
	else:
		totals_taxes = """
{% if doc.total_taxes_and_charges %}
<div class="row"><div class="lbl">VAT (15%)</div><div class="val">{{ doc.get_formatted("total_taxes_and_charges") if doc.get_formatted is defined else doc.total_taxes_and_charges or "" }} {{ doc.currency or "" }}</div></div>
{% endif %}"""

	in_words = ""
	if profile.has_in_words:
		in_words = """
{% if doc.in_words %}
<div class="notes-card">
<div class="title">Amount in Words</div>
{{ doc.in_words }}
</div>
{% endif %}"""
	else:
		in_words = '<div class="notes-card"></div>'

	doc_title = "TAX INVOICE"
	if profile.doc_type in ("Quotation", "Sales Order"):
		doc_title = profile.title.upper()
	elif profile.doc_type == "Delivery Note":
		doc_title = "DELIVERY NOTE"

	return f"""{{# ZATCA Manrope · {profile.doc_type} #}}
{{% set date_field = "{profile.date_field}" %}}
<style>
:root{{
--ink:#1a2332;--ink-soft:#5b6675;--line:#e2e6ec;--line-strong:#c7cedb;
--brand:#0b6e4f;--brand-dark:#074935;--brand-tint:#eaf5f0;--accent:#c9a15a;
--bg:#f4f6f8;--paper:#ffffff;
}}
*{{box-sizing:border-box;}}
.zm-root{{font-family:'Manrope','Segoe UI',Arial,sans-serif;color:var(--ink);font-size:11px;-webkit-font-smoothing:antialiased;}}
.zm-sheet{{background:var(--paper);padding:0;position:relative;}}
.zm-header{{display:flex;justify-content:space-between;align-items:flex-start;gap:20px;padding-bottom:16px;border-bottom:3px solid var(--brand);}}
.zm-company-block{{display:flex;gap:14px;align-items:center;}}
.zm-logo{{width:64px;height:64px;border-radius:12px;background:var(--brand);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:18px;flex-shrink:0;overflow:hidden;}}
.zm-logo img{{max-width:100%;max-height:100%;object-fit:contain;border-radius:12px;}}
.zm-company-name{{font-weight:800;font-size:17px;color:var(--ink);}}
.zm-company-sub{{font-size:11px;color:var(--ink-soft);font-weight:600;margin-top:2px;}}
.zm-company-meta{{font-size:10.5px;color:var(--ink-soft);margin-top:6px;line-height:1.7;}}
.zm-company-meta b{{color:var(--ink);font-weight:700;}}
.zm-invoice-tag{{text-align:right;}}
.zm-invoice-tag .type{{font-size:21px;font-weight:800;color:var(--brand-dark);letter-spacing:.3px;}}
.zm-invoice-tag .badge{{display:inline-block;margin-top:8px;background:var(--brand-tint);color:var(--brand-dark);font-size:10px;font-weight:700;padding:3px 10px;border-radius:20px;border:1px solid #cfe6db;}}
.zm-meta-strip{{display:flex;margin-top:18px;border:1px solid var(--line);border-radius:10px;overflow:hidden;}}
.zm-meta-cell{{flex:1;padding:10px 14px;border-left:1px solid var(--line);}}
.zm-meta-cell:first-child{{border-left:none;}}
.zm-meta-label{{font-size:9px;color:var(--ink-soft);text-transform:uppercase;letter-spacing:.6px;font-weight:700;}}
.zm-meta-value{{font-size:12px;font-weight:700;color:var(--ink);margin-top:4px;}}
.zm-parties{{display:flex;gap:16px;margin-top:18px;}}
.zm-party-card{{flex:1;background:#fbfbfc;border:1px solid var(--line);border-radius:10px;padding:12px 14px;}}
.zm-party-title{{font-size:10px;font-weight:700;color:var(--brand-dark);text-transform:uppercase;letter-spacing:.6px;margin-bottom:8px;}}
.zm-party-name{{font-weight:700;font-size:13px;}}
.zm-party-line{{font-size:11px;color:var(--ink-soft);margin-top:3px;line-height:1.6;}}
.zm-party-line b{{color:var(--ink);}}
table.items{{width:100%;border-collapse:collapse;margin-top:20px;font-size:11px;}}
table.items thead th{{background:var(--brand-dark);color:#fff;padding:9px 10px;font-weight:700;font-size:10px;text-align:left;text-transform:uppercase;letter-spacing:.3px;}}
table.items thead th.num{{text-align:right;}}
table.items thead th:first-child{{border-radius:8px 0 0 0;}}
table.items thead th:last-child{{border-radius:0 8px 0 0;}}
table.items tbody td{{padding:9px 10px;border-bottom:1px solid var(--line);vertical-align:top;}}
table.items tbody tr:nth-child(even){{background:#fafbfc;}}
table.items td.desc .item-title{{font-weight:600;display:block;}}
table.items td.desc .item-sub{{display:block;font-size:10px;color:var(--ink-soft);margin-top:2px;}}
table.items td.num{{text-align:right;font-variant-numeric:tabular-nums;}}
.zm-totals-wrap{{display:flex;justify-content:space-between;margin-top:18px;gap:20px;}}
.zm-qr-block{{display:flex;flex-direction:column;align-items:center;gap:8px;padding-top:6px;}}
.zm-qr-box{{width:110px;height:110px;border:1px solid var(--line-strong);border-radius:8px;background:#fff;display:flex;align-items:center;justify-content:center;font-size:9px;color:var(--ink-soft);text-align:center;padding:6px;}}
.zm-qr-box img{{width:100px;height:100px;}}
.zm-qr-caption{{font-size:9px;color:var(--ink-soft);text-align:center;max-width:130px;line-height:1.5;}}
.zm-qr-caption b{{display:block;color:var(--ink);}}
.zm-totals-table{{width:290px;font-size:12px;}}
.zm-totals-table .row{{display:flex;justify-content:space-between;padding:8px 12px;border-bottom:1px solid var(--line);}}
.zm-totals-table .row .lbl{{color:var(--ink-soft);font-weight:600;}}
.zm-totals-table .row .val{{font-weight:700;}}
.zm-totals-table .grand{{background:var(--brand);color:#fff;border-radius:8px;margin-top:8px;padding:11px 14px;}}
.zm-totals-table .grand .lbl{{color:#eafff2;}}
.zm-totals-table .grand .val{{font-size:15px;}}
.zm-notes{{margin-top:20px;display:flex;gap:16px;}}
.zm-notes .notes-card{{flex:1.4;border:1px dashed var(--line-strong);border-radius:10px;padding:12px 14px;font-size:11px;color:var(--ink-soft);}}
.zm-notes .bank-card{{flex:1;}}
.zm-notes-card .title{{font-weight:700;color:var(--ink);font-size:11px;margin-bottom:5px;}}
.zm-bank-card .row2{{display:flex;justify-content:space-between;margin-top:5px;}}
.zm-bank-card .row2 b{{color:var(--ink);direction:ltr;}}
.zm-footer{{margin-top:26px;padding-top:12px;border-top:1px solid var(--line);display:flex;justify-content:space-between;align-items:center;font-size:9px;color:#9aa2af;}}
.zm-footer .zatca{{display:flex;align-items:center;gap:6px;font-weight:700;color:var(--brand-dark);}}
.zm-footer .dot{{width:6px;height:6px;border-radius:50%;background:var(--brand);}}
.epp-sig,.sig,.epp-footer,.footer{{display:none;}}
.print-format table.items > tbody > tr > td{{padding:9px 10px !important;}}
@page{{size:A4 portrait;margin:10mm;}}
</style>
<div class="zm-root print-format">
<div class="zm-sheet">
<div class="zm-header">
<div class="zm-company-block">
<div class="zm-logo">
{{% set logo = frappe.db.get_value("Company", doc.company, "company_logo") if doc.company else "" %}}
{{% if logo %}}<img src="{{{{ logo }}}}">{{% else %}}CO{{% endif %}}
</div>
<div>
<div class="zm-company-name">{{{{ doc.company or "" }}}}</div>
<div class="zm-company-sub">{{{{ doc.get("custom_company_location") or "" }}}}</div>
<div class="zm-company-meta">
<b>VAT Registration No.:</b> {{{{ doc.company_tax_id or "" }}}} &nbsp;•&nbsp;
<b>CR No.:</b> {{{{ doc.get("custom_company_cr_number") or "" }}}}<br>
{{{{ doc.company_address_display or "" }}}}
</div>
</div>
</div>
<div class="zm-invoice-tag">
<div class="type">{doc_title}</div>
<div class="badge">ZATCA E-Invoicing Compliant</div>
</div>
</div>
<div class="zm-meta-strip">
<div class="zm-meta-cell"><div class="zm-meta-label">Invoice No.</div><div class="zm-meta-value">{{{{ doc.name }}}}</div></div>
<div class="zm-meta-cell"><div class="zm-meta-label">Issue Date</div><div class="zm-meta-value">{{{{ frappe.utils.formatdate(doc.get(date_field), "dd MMM yyyy") if doc.get(date_field) else "" }}}}</div></div>
<div class="zm-meta-cell"><div class="zm-meta-label">Supply Date</div><div class="zm-meta-value">{{{{ frappe.utils.formatdate(doc.get("delivery_date") or doc.get(date_field), "dd MMM yyyy") if doc.get("delivery_date") or doc.get(date_field) else "" }}}}</div></div>
<div class="zm-meta-cell"><div class="zm-meta-label">Payment Method</div><div class="zm-meta-value">{{{{ doc.mode_of_payment or doc.payment_terms_template or "" }}}}</div></div>
</div>
<div class="zm-parties">
<div class="zm-party-card">
<div class="zm-party-title">Seller</div>
<div class="zm-party-name">{{{{ doc.company or "" }}}}</div>
<div class="zm-party-line"><b>VAT No.:</b> {{{{ doc.company_tax_id or "" }}}}</div>
<div class="zm-party-line">{{{{ doc.company_address_display or "" }}}}</div>
</div>
<div class="zm-party-card">
<div class="zm-party-title">{party_label}</div>
<div class="zm-party-name">{party_name}</div>
<div class="zm-party-line"><b>VAT No.:</b> {party_tax}</div>
<div class="zm-party-line">{party_address}</div>
</div>
</div>
{items_block}
<div class="zm-totals-wrap">
<div class="zm-qr-block epp-qr qr">
<div class="zm-qr-box">
{{% set qr = doc.get("ksa_einv_qr") or doc.get("custom_qr_code") or "" %}}
{{% if not qr %}}{{% set _qrp = frappe.call("erpnext_print_pack.print_barcodes.get_qr_and_barcode_data_uri", value=doc.name) %}}{{% if _qrp %}}{{% set qr = _qrp.get("qr") or "" %}}{{% endif %}}{{% endif %}}
{{% if qr %}}<img src="{{{{ qr }}}}">{{% else %}}ZATCA<br>QR CODE<br>(Base64 TLV){{% endif %}}
</div>
<div class="zm-qr-caption"><b>Scan to verify</b>Seller, VAT No., Timestamp, Total &amp; VAT amount encoded per ZATCA Phase 2 spec</div>
</div>
<div class="zm-totals-table">
<div class="row"><div class="lbl">Subtotal</div><div class="val">{{{{ doc.get_formatted("net_total") if doc.get_formatted is defined else doc.net_total or "" }}}} {{{{ doc.currency or "" }}}}</div></div>
<div class="row"><div class="lbl">Discount</div><div class="val">{{{{ doc.get_formatted("total_discount") if doc.get_formatted is defined and doc.total_discount else doc.discount_amount or "0.00" }}}} {{{{ doc.currency or "" }}}}</div></div>
<div class="row"><div class="lbl">Taxable Amount</div><div class="val">{{{{ doc.get_formatted("net_total") if doc.get_formatted is defined else doc.net_total or "" }}}} {{{{ doc.currency or "" }}}}</div></div>
{totals_taxes}
<div class="row grand"><div class="lbl">Total Due</div><div class="val">{{{{ doc.get_formatted("grand_total") if doc.get_formatted is defined else doc.grand_total or "" }}}} {{{{ doc.currency or "" }}}}</div></div>
</div>
</div>
<div class="zm-notes">
{in_words}
<div class="notes-card bank-card zm-bank-card">
<div class="title">Bank Details</div>
{{% set bank = frappe.get_all("Bank Account", filters={{"company": doc.company, "is_company_account": 1}}, fields=["bank","iban","bank_account_no"], limit=1) %}}
{{% if bank %}}
<div class="row2"><span>Bank</span><b>{{{{ bank[0].bank or "" }}}}</b></div>
<div class="row2"><span>IBAN</span><b>{{{{ bank[0].iban or bank[0].bank_account_no or "" }}}}</b></div>
{{% else %}}—{{% endif %}}
</div>
</div>
<div class="zm-footer">
<div>This is a system-generated tax invoice and does not require a signature or stamp.</div>
<div class="zatca"><span class="dot"></span>Fatoora / ZATCA Phase 2</div>
</div>
{DOC_BARCODE_SNIPPET}
</div>
</div>"""
