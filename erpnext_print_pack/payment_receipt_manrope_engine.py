"""Manrope Payment Receipt — shared HTML/CSS for Payment Entry."""

from __future__ import annotations

from erpnext_print_pack.doctype_profiles import DocTypeProfile
from erpnext_print_pack.print_snippets import DOC_BARCODE_SNIPPET

LAYOUT_KEY = "payment_receipt_manrope"
LAYOUT_LABEL = "Manrope Payment Receipt"
LAYOUT_META = {
	"label": LAYOUT_LABEL,
	"region": "ALL",
	"layout_type": "colorful",
	"description": "Payment receipt — Manrope green brand, amount banner, applied invoices table",
}

_PAYMENT_AMOUNT = """{% set _pay_amt = doc.paid_amount or doc.received_amount or doc.base_paid_amount or 0 %}{% set _pay_cur = doc.paid_to_account_currency or doc.paid_from_account_currency or doc.company_currency or "" %}{{ frappe.utils.fmt_money(_pay_amt, currency=_pay_cur) if _pay_amt else "" }}"""


def format_name(profile: DocTypeProfile) -> str:
	return f"{LAYOUT_LABEL} {profile.title}"


def format_slug(profile: DocTypeProfile) -> str:
	return f"{profile.slug}_{LAYOUT_KEY}"


def render_payment_receipt_manrope(profile: DocTypeProfile) -> str:
	if profile.doc_type != "Payment Entry":
		raise ValueError(f"{LAYOUT_KEY} supports Payment Entry only")

	return f"""{{# Manrope Payment Receipt · Payment Entry #}}
{{% set date_field = "{profile.date_field}" %}}
{{% set party_label = doc.party_type or "Party" %}}
{{% set party_name = doc.party_name or doc.party or "" %}}
{{% set party_address = doc.party_address or doc.address_display or "" %}}
<style>
:root{{
--ink:#1a2332;--ink-soft:#5b6675;--line:#e2e6ec;--line-strong:#c7cedb;
--brand:#0b6e4f;--brand-dark:#074935;--brand-tint:#eaf5f0;--paper:#ffffff;
}}
*{{box-sizing:border-box;}}
.pr-root{{font-family:'Manrope','Segoe UI',Arial,sans-serif;color:var(--ink);font-size:11px;-webkit-font-smoothing:antialiased;}}
.pr-sheet{{background:var(--paper);padding:0;position:relative;}}
.pr-header{{display:flex;justify-content:space-between;align-items:flex-start;gap:20px;padding-bottom:16px;border-bottom:3px solid var(--brand);}}
.pr-company-block{{display:flex;gap:14px;align-items:center;}}
.pr-logo{{width:60px;height:60px;border-radius:12px;background:var(--brand);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:17px;flex-shrink:0;overflow:hidden;}}
.pr-logo img{{max-width:100%;max-height:100%;object-fit:contain;border-radius:12px;}}
.pr-company-name{{font-weight:800;font-size:17px;color:var(--ink);}}
.pr-company-sub{{font-size:11px;color:var(--ink-soft);font-weight:600;margin-top:2px;}}
.pr-company-meta{{font-size:10px;color:var(--ink-soft);margin-top:5px;line-height:1.6;}}
.pr-company-meta b{{color:var(--ink);font-weight:700;}}
.pr-doc-tag{{text-align:right;}}
.pr-doc-tag .type{{font-size:20px;font-weight:800;color:var(--brand-dark);letter-spacing:.3px;}}
.pr-doc-tag .badge{{display:inline-block;margin-top:8px;background:var(--brand-tint);color:var(--brand-dark);font-size:10px;font-weight:700;padding:3px 10px;border-radius:20px;border:1px solid #cfe6db;}}
.pr-meta-strip{{display:flex;margin-top:18px;border:1px solid var(--line);border-radius:10px;overflow:hidden;}}
.pr-meta-cell{{flex:1;padding:10px 14px;border-left:1px solid var(--line);}}
.pr-meta-cell:first-child{{border-left:none;}}
.pr-meta-label{{font-size:9px;color:var(--ink-soft);text-transform:uppercase;letter-spacing:.6px;font-weight:700;}}
.pr-meta-value{{font-size:12px;font-weight:700;color:var(--ink);margin-top:4px;}}
.pr-amount-banner{{margin-top:20px;background:var(--brand);color:#fff;border-radius:12px;padding:16px 20px;display:flex;justify-content:space-between;align-items:center;}}
.pr-amount-banner .lbl{{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;color:#d9f2e6;}}
.pr-amount-banner .val{{font-size:26px;font-weight:800;margin-top:2px;}}
.pr-amount-banner .words{{font-size:10px;color:#d9f2e6;margin-top:6px;max-width:340px;}}
.pr-amount-banner .status{{background:rgba(255,255,255,.16);padding:6px 14px;border-radius:20px;font-size:11px;font-weight:700;border:1px solid rgba(255,255,255,.35);white-space:nowrap;}}
.pr-details{{display:flex;gap:16px;margin-top:18px;}}
.pr-detail-card{{flex:1;background:#fbfbfc;border:1px solid var(--line);border-radius:10px;padding:12px 14px;}}
.pr-detail-title{{font-size:10px;font-weight:700;color:var(--brand-dark);text-transform:uppercase;letter-spacing:.6px;margin-bottom:8px;}}
.pr-detail-name{{font-weight:700;font-size:13px;}}
.pr-detail-line{{font-size:11px;color:var(--ink-soft);margin-top:3px;line-height:1.6;}}
.pr-detail-line b{{color:var(--ink);}}
table.applied{{width:100%;border-collapse:collapse;margin-top:20px;font-size:11px;}}
table.applied thead th{{background:var(--brand-dark);color:#fff;padding:9px 10px;font-weight:700;font-size:10px;text-align:left;text-transform:uppercase;letter-spacing:.3px;}}
table.applied thead th.num{{text-align:right;}}
table.applied thead th:first-child{{border-radius:8px 0 0 0;}}
table.applied thead th:last-child{{border-radius:0 8px 0 0;}}
table.applied tbody td{{padding:9px 10px;border-bottom:1px solid var(--line);}}
table.applied tbody tr:nth-child(even){{background:#fafbfc;}}
table.applied td.num{{text-align:right;font-variant-numeric:tabular-nums;}}
table.applied tfoot td{{padding:10px;font-weight:800;border-top:2px solid var(--brand);}}
table.applied tfoot td.num{{text-align:right;}}
.pr-sign-row{{display:flex;justify-content:space-between;margin-top:36px;}}
.pr-sign-block{{width:220px;text-align:center;}}
.pr-sign-line{{border-top:1px solid var(--line-strong);padding-top:6px;font-size:10px;color:var(--ink-soft);font-weight:600;}}
.pr-footer{{margin-top:26px;padding-top:12px;border-top:1px solid var(--line);display:flex;justify-content:space-between;align-items:center;font-size:9px;color:#9aa2af;}}
.pr-footer .brand{{display:flex;align-items:center;gap:6px;font-weight:700;color:var(--brand-dark);}}
.pr-footer .dot{{width:6px;height:6px;border-radius:50%;background:var(--brand);}}
.epp-sig,.sig,.epp-footer,.footer{{display:none;}}
.print-format table.applied > tbody > tr > td{{padding:9px 10px !important;}}
@page{{size:A4 portrait;margin:10mm;}}
</style>
<div class="pr-root print-format">
<div class="pr-sheet">
<div class="pr-header">
<div class="pr-company-block">
<div class="pr-logo">
{{% set logo = frappe.db.get_value("Company", doc.company, "company_logo") if doc.company else "" %}}
{{% if logo %}}<img src="{{{{ logo }}}}">{{% else %}}CO{{% endif %}}
</div>
<div>
<div class="pr-company-name">{{{{ doc.company or "" }}}}</div>
<div class="pr-company-sub">{{{{ doc.get("custom_company_location") or "" }}}}</div>
<div class="pr-company-meta">
<b>VAT Registration No.:</b> {{{{ doc.company_tax_id or "" }}}} &nbsp;•&nbsp;
<b>CR No.:</b> {{{{ doc.get("custom_company_cr_number") or "" }}}}
</div>
</div>
</div>
<div class="pr-doc-tag">
<div class="type">{{{{ "PAYMENT RECEIPT" if doc.payment_type == "Receive" else ("PAYMENT VOUCHER" if doc.payment_type == "Pay" else "PAYMENT ENTRY") }}}}</div>
<div class="badge">Official Receipt</div>
</div>
</div>
<div class="pr-meta-strip">
<div class="pr-meta-cell"><div class="pr-meta-label">Receipt No.</div><div class="pr-meta-value">{{{{ doc.name }}}}</div></div>
<div class="pr-meta-cell"><div class="pr-meta-label">Payment Date</div><div class="pr-meta-value">{{{{ frappe.utils.formatdate(doc.get(date_field), "dd MMM yyyy") if doc.get(date_field) else "" }}}}</div></div>
<div class="pr-meta-cell"><div class="pr-meta-label">Payment Mode</div><div class="pr-meta-value">{{{{ doc.mode_of_payment or "—" }}}}</div></div>
<div class="pr-meta-cell"><div class="pr-meta-label">Reference No.</div><div class="pr-meta-value">{{{{ doc.reference_no or doc.cheque_no or "—" }}}}</div></div>
</div>
<div class="pr-amount-banner">
<div>
<div class="lbl">{{{{ "Amount Received" if doc.payment_type == "Receive" else ("Amount Paid" if doc.payment_type == "Pay" else "Amount") }}}}</div>
<div class="val">{_PAYMENT_AMOUNT}</div>
{{% if doc.in_words %}}<div class="words">{{{{ doc.in_words }}}}</div>{{% endif %}}
</div>
<div class="status">{{{{ "✓ " + (doc.status or "Submitted") }}}}</div>
</div>
<div class="pr-details">
<div class="pr-detail-card">
<div class="pr-detail-title">{{{{ "Received From" if doc.payment_type == "Receive" else ("Paid To" if doc.payment_type == "Pay" else party_label) }}}}</div>
<div class="pr-detail-name">{{{{ party_name }}}}</div>
<div class="pr-detail-line"><b>{{{{ party_label }}}}</b> {{{{ doc.party or "" }}}}</div>
<div class="pr-detail-line">{{{{ party_address }}}}</div>
</div>
<div class="pr-detail-card">
<div class="pr-detail-title">{{{{ "Received By" if doc.payment_type == "Receive" else ("Paid By" if doc.payment_type == "Pay" else "Company") }}}}</div>
<div class="pr-detail-name">{{{{ doc.company or "" }}}}</div>
<div class="pr-detail-line"><b>VAT No.:</b> {{{{ doc.company_tax_id or "" }}}}</div>
<div class="pr-detail-line">{{{{ doc.company_address_display or "" }}}}</div>
</div>
</div>
{{% if doc.references %}}
<table class="applied">
<thead>
<tr>
<th style="width:22%">Invoice No.</th>
<th style="width:20%">Invoice Date</th>
<th class="num" style="width:19%">Invoice Total</th>
<th class="num" style="width:19%">Previously Paid</th>
<th class="num" style="width:20%">Amount Applied</th>
</tr>
</thead>
<tbody>
{{% for row in doc.references %}}
<tr>
<td>{{{{ row.reference_name or "" }}}}</td>
<td>{{{{ frappe.utils.formatdate(frappe.db.get_value(row.reference_doctype, row.reference_name, "posting_date") or row.due_date) if row.reference_doctype and row.reference_name else (frappe.utils.formatdate(row.due_date) if row.due_date else "") }}}}</td>
<td class="num">{{{{ row.get_formatted("total_amount") if row.get_formatted is defined and row.total_amount is defined else row.total_amount or "" }}}}</td>
<td class="num">{{{{ frappe.utils.fmt_money((row.total_amount or 0) - (row.outstanding_amount or 0), currency=doc.company_currency) if (row.total_amount is not none or row.outstanding_amount is not none) else "" }}}}</td>
<td class="num">{{{{ row.get_formatted("allocated_amount") if row.get_formatted is defined else row.allocated_amount or "" }}}}</td>
</tr>
{{% endfor %}}
</tbody>
<tfoot>
<tr>
<td colspan="4">Total Amount {{{{ "Received" if doc.payment_type == "Receive" else "Paid" }}}}</td>
<td class="num">{_PAYMENT_AMOUNT}</td>
</tr>
</tfoot>
</table>
{{% endif %}}
<div class="pr-sign-row">
<div class="pr-sign-block"><div class="pr-sign-line">{{{{ "Received By — Authorized Signatory" if doc.payment_type == "Receive" else "Paid By — Authorized Signatory" }}}}</div></div>
<div class="pr-sign-block"><div class="pr-sign-line">Company Stamp</div></div>
</div>
<div class="pr-footer">
<div>This receipt confirms payment collection and is not a tax invoice.</div>
<div class="brand"><span class="dot"></span>Generated via ERPNext</div>
</div>
</div>
{DOC_BARCODE_SNIPPET}
</div>"""
