#!/usr/bin/env python3
"""Bootstrap erpnext_print_pack: components, themes, formats, manifest."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "erpnext_print_pack"
COMPONENTS = APP / "components"
THEMES = APP / "themes"
FORMATS = APP / "print_pack" / "print_format"
MANIFEST = APP / "print_pack" / "manifest.json"

sys.path.insert(0, str(ROOT))
from erpnext_print_pack.doctype_profiles import DEFERRED_DOCTYPES, PROFILES  # noqa: E402
from erpnext_print_pack.themes.registry import THEME_REGISTRY, get_theme_css  # noqa: E402

PRESERVE_SLUGS = {"sales_invoice_bilingual_tax"}

COMPONENT_BODIES = {
	"headers/basic.html": """<div class="epp-header epp-box">
\t<div class="epp-primary bold">{{ doc.company or "" }}</div>
\t<div>{{ title }}</div>
\t<div>{{ doc.name or "" }} · {{ frappe.utils.formatdate(doc.get(date_field)) if doc.get(date_field) else "" }}</div>
</div>""",
	"headers/logo_left.html": """<table class="epp-table" style="border:0;margin-bottom:6px"><tr>
\t<td style="border:0;width:25%"><img src="{{ frappe.db.get_value('Company', doc.company, 'company_logo') or '' }}" style="max-height:48px"></td>
\t<td style="border:0"><div class="epp-primary bold">{{ doc.company or "" }}</div><div>{{ title }}</div></td>
</tr></table>""",
	"headers/logo_center.html": """<div class="center epp-box"><img src="{{ frappe.db.get_value('Company', doc.company, 'company_logo') or '' }}" style="max-height:52px"><div class="bold epp-primary">{{ title }}</div></div>""",
	"headers/company_details.html": """<div class="epp-box"><div class="bold epp-primary">{{ doc.company or "" }}</div><div>{{ doc.company_address_display or "" }}</div></div>""",
	"headers/compact.html": """<div class="epp-box" style="padding:3px 5px;font-size:8px"><span class="bold">{{ title }}</span> · {{ doc.name or "" }}</div>""",
	"headers/bilingual.html": """<div class="epp-box"><div class="bold epp-primary">{{ title }} <span style="float:right;direction:rtl">{{ title_secondary or "" }}</span></div></div>""",
	"headers/tax_registration.html": """<div class="epp-box"><div>Tax ID: {{ doc.company_tax_id or doc.tax_id or "" }}</div><div class="bold">{{ title }}</div></div>""",
	"headers/document_number.html": """<div class="epp-box"><div class="bold">{{ title }}</div><div>No: {{ doc.name or "" }}</div></div>""",
	"headers/landscape.html": """<table style="width:100%"><tr><td class="bold epp-primary">{{ doc.company or "" }}</td><td class="right bold">{{ title }} {{ doc.name or "" }}</td></tr></table>""",
	"headers/thermal.html": """<div class="center bold">{{ doc.company or "" }}</div><div class="center">{{ title }}</div><div class="center">{{ doc.name or "" }}</div><hr>""",
	"party_blocks/bill_to.html": """<div class="epp-box"><div class="bold epp-primary">Bill To</div><div>{{ doc.customer_name or doc.customer or doc.party_name or doc.party or "" }}</div><div>{{ doc.address_display or "" }}</div></div>""",
	"party_blocks/ship_to.html": """<div class="epp-box"><div class="bold epp-primary">Ship To</div><div>{{ doc.shipping_address_name or "" }}</div><div>{{ doc.shipping_address or doc.shipping_address_display or "" }}</div></div>""",
	"party_blocks/supplier.html": """<div class="epp-box"><div class="bold epp-primary">Supplier</div><div>{{ doc.supplier_name or doc.supplier or "" }}</div><div>{{ doc.address_display or doc.supplier_address or "" }}</div></div>""",
	"party_blocks/customer_shipping.html": """<table style="width:100%"><tr><td class="epp-box" style="width:49%"><div class="bold">Customer</div>{{ doc.customer_name or doc.customer or doc.party_name or "" }}</td><td style="width:2%"></td><td class="epp-box" style="width:49%"><div class="bold">Shipping</div>{{ doc.shipping_address or "" }}</td></tr></table>""",
	"party_blocks/contact.html": """<div class="epp-box"><div class="bold">Contact</div><div>{{ doc.contact_display or doc.contact_person or "" }}</div><div>{{ doc.contact_mobile or doc.contact_phone or "" }}</div></div>""",
	"party_blocks/tax_id.html": """<div class="epp-box"><div class="bold">Tax ID</div><div>{{ doc.tax_id or doc.company_tax_id or "" }}</div></div>""",
	"party_blocks/billing_delivery.html": """<div class="epp-box"><div class="bold">Billing / Delivery</div><div>{{ doc.address_display or "" }}</div></div>""",
	"party_blocks/bilingual.html": """<div class="epp-box"><span class="bold">Customer</span> : {{ doc.customer_name or doc.customer or "" }} <span style="float:right;direction:rtl">العميل</span></div>""",
	"party_blocks/vehicle_details.html": """<div class="epp-box"><div class="bold">Vehicle</div><div>{{ doc.vehicle or "" }} {{ doc.driver or doc.driver_name or "" }}</div></div>""",
	"party_blocks/shipping_details.html": """<div class="epp-box"><div class="bold">Shipping</div><div>{{ doc.tracking_number or "" }} {{ doc.carrier or "" }}</div></div>""",
	"item_tables/basic.html": """{% if doc.items %}<table class="epp-table"><thead><tr><th>#</th><th>Description</th><th>Qty</th><th>Rate</th><th>Amount</th></tr></thead><tbody>{% for row in doc.items %}<tr><td>{{ loop.index }}</td><td>{{ row.item_name or row.item_code or row.description or "" }}</td><td class="right">{{ row.get_formatted("qty", doc) if row.get_formatted is defined else row.qty or "" }}</td><td class="right">{{ row.get_formatted("rate", doc) if row.get_formatted is defined else row.rate or "" }}</td><td class="right">{{ row.get_formatted("amount", doc) if row.get_formatted is defined else row.amount or "" }}</td></tr>{% endfor %}</tbody></table>{% endif %}""",
	"item_tables/compact.html": """{% if doc.items %}<table class="epp-table" style="font-size:8px"><thead><tr><th>Item</th><th>Qty</th><th>Amt</th></tr></thead><tbody>{% for row in doc.items %}<tr><td>{{ row.item_code or row.item_name or "" }}</td><td class="right">{{ row.qty or "" }}</td><td class="right">{{ row.amount or "" }}</td></tr>{% endfor %}</tbody></table>{% endif %}""",
	"item_tables/tax_inclusive.html": """{% if doc.items %}<table class="epp-table"><thead><tr><th>#</th><th>Item</th><th>Qty</th><th>Rate</th><th>Tax</th><th>Amount</th></tr></thead><tbody>{% for row in doc.items %}<tr><td>{{ loop.index }}</td><td>{{ row.item_name or row.item_code or "" }}</td><td class="right">{{ row.qty or "" }}</td><td class="right">{{ row.rate or "" }}</td><td class="right">{{ row.item_tax_rate or "" }}</td><td class="right">{{ row.amount or "" }}</td></tr>{% endfor %}</tbody></table>{% endif %}""",
	"item_tables/discount.html": """{% if doc.items %}<table class="epp-table"><thead><tr><th>Item</th><th>Qty</th><th>Disc%</th><th>Amount</th></tr></thead><tbody>{% for row in doc.items %}<tr><td>{{ row.item_name or row.item_code or "" }}</td><td class="right">{{ row.qty or "" }}</td><td class="right">{{ row.discount_percentage or 0 }}</td><td class="right">{{ row.amount or "" }}</td></tr>{% endfor %}</tbody></table>{% endif %}""",
	"item_tables/batch_serial.html": """{% if doc.items %}<table class="epp-table"><thead><tr><th>Item</th><th>Batch</th><th>Serial</th><th>Qty</th></tr></thead><tbody>{% for row in doc.items %}<tr><td>{{ row.item_code or "" }}</td><td>{{ row.batch_no or "" }}</td><td>{{ row.serial_no or "" }}</td><td class="right">{{ row.qty or "" }}</td></tr>{% endfor %}</tbody></table>{% endif %}""",
	"item_tables/warehouse.html": """{% if doc.items %}<table class="epp-table"><thead><tr><th>Item</th><th>Warehouse</th><th>Qty</th></tr></thead><tbody>{% for row in doc.items %}<tr><td>{{ row.item_code or "" }}</td><td>{{ row.warehouse or row.s_warehouse or row.t_warehouse or "" }}</td><td class="right">{{ row.qty or "" }}</td></tr>{% endfor %}</tbody></table>{% endif %}""",
	"item_tables/stock_entry.html": """{% if doc.items %}<table class="epp-table"><thead><tr><th>#</th><th>Item</th><th>From WH</th><th>To WH</th><th>Qty</th><th>UOM</th><th>Rate</th><th>Amount</th></tr></thead><tbody>{% for row in doc.items %}<tr><td>{{ loop.index }}</td><td>{{ row.item_code or "" }}{% if row.item_name %}<br>{{ row.item_name }}{% endif %}</td><td>{{ row.s_warehouse or "" }}</td><td>{{ row.t_warehouse or "" }}</td><td class="right">{{ row.qty or "" }}</td><td>{{ row.uom or "" }}</td><td class="right">{{ row.basic_rate or row.valuation_rate or "" }}</td><td class="right">{{ row.amount or row.basic_amount or "" }}</td></tr>{% endfor %}</tbody></table>{% endif %}{% if doc.additional_costs %}<table class="epp-table" style="margin-top:8px"><thead><tr><th>Expense Account</th><th>Description</th><th>Amount</th></tr></thead><tbody>{% for row in doc.additional_costs %}<tr><td>{{ row.expense_account or "" }}</td><td>{{ row.description or "" }}</td><td class="right">{{ row.amount or "" }}</td></tr>{% endfor %}</tbody></table>{% endif %}""",
	"item_tables/journal_accounts.html": """{% if doc.accounts %}<table class="epp-table"><thead><tr><th>#</th><th>Account</th><th>Party</th><th>Cost Center</th><th>Debit</th><th>Credit</th></tr></thead><tbody>{% for row in doc.accounts %}<tr><td>{{ loop.index }}</td><td>{{ row.account or "" }}{% if row.user_remark %}<br><small>{{ row.user_remark }}</small>{% endif %}</td><td>{{ row.party_type or "" }} {{ row.party or "" }}</td><td>{{ row.cost_center or "" }}</td><td class="right">{{ row.debit_in_account_currency or row.debit or "" }}</td><td class="right">{{ row.credit_in_account_currency or row.credit or "" }}</td></tr>{% endfor %}</tbody></table>{% endif %}""",
	"item_tables/payment_details.html": """<table class="epp-table"><thead><tr><th>Field</th><th>Value</th></tr></thead><tbody><tr><td>Payment Type</td><td>{{ doc.payment_type or "" }}</td></tr><tr><td>Party</td><td>{{ doc.party_name or doc.party or "" }} ({{ doc.party_type or "" }})</td></tr><tr><td>Mode of Payment</td><td>{{ doc.mode_of_payment or "" }}</td></tr><tr><td>Paid From</td><td>{{ doc.paid_from or "" }}</td></tr><tr><td>Paid To</td><td>{{ doc.paid_to or "" }}</td></tr><tr><td>Paid Amount</td><td class="right">{{ doc.paid_amount or "" }}</td></tr>{% if doc.received_amount %}<tr><td>Received Amount</td><td class="right">{{ doc.received_amount }}</td></tr>{% endif %}</tbody></table>{% if doc.references %}<table class="epp-table" style="margin-top:8px"><thead><tr><th>Type</th><th>Reference</th><th>Outstanding</th><th>Allocated</th></tr></thead><tbody>{% for row in doc.references %}<tr><td>{{ row.reference_doctype or "" }}</td><td>{{ row.reference_name or "" }}</td><td class="right">{{ row.outstanding_amount or "" }}</td><td class="right">{{ row.allocated_amount or "" }}</td></tr>{% endfor %}</tbody></table>{% endif %}{% if doc.deductions %}<table class="epp-table" style="margin-top:8px"><thead><tr><th>Account</th><th>Amount</th></tr></thead><tbody>{% for row in doc.deductions %}<tr><td>{{ row.account or "" }}</td><td class="right">{{ row.amount or "" }}</td></tr>{% endfor %}</tbody></table>{% endif %}""",
	"item_tables/manufacturing.html": """{% if doc.items %}<table class="epp-table"><thead><tr><th>Item</th><th>Qty</th><th>UOM</th></tr></thead><tbody>{% for row in doc.items %}<tr><td>{{ row.item_code or row.item_name or "" }}</td><td class="right">{{ row.qty or row.required_qty or "" }}</td><td>{{ row.uom or row.stock_uom or "" }}</td></tr>{% endfor %}</tbody></table>{% endif %}""",
	"totals/journal.html": """<table class="epp-totals" style="width:45%;margin-left:auto"><tr><td>Total Debit</td><td class="right">{{ doc.total_debit or "" }}</td></tr><tr><td>Total Credit</td><td class="right">{{ doc.total_credit or "" }}</td></tr>{% if doc.total_amount %}<tr><td class="bold">Total Amount</td><td class="right bold">{{ doc.total_amount }}</td></tr>{% endif %}</table>{% if doc.total_amount_in_words %}<div class="epp-box">{{ doc.total_amount_in_words }}</div>{% endif %}""",
	"totals/payment.html": """<table class="epp-totals" style="width:50%;margin-left:auto"><tr><td>Paid Amount</td><td class="right">{{ doc.paid_amount or "" }}</td></tr>{% if doc.received_amount %}<tr><td>Received Amount</td><td class="right">{{ doc.received_amount }}</td></tr>{% endif %}{% if doc.total_allocated_amount %}<tr><td>Allocated</td><td class="right">{{ doc.total_allocated_amount }}</td></tr>{% endif %}{% if doc.unallocated_amount %}<tr><td>Unallocated</td><td class="right">{{ doc.unallocated_amount }}</td></tr>{% endif %}</table>""",
	"totals/stock_entry.html": """<table class="epp-totals" style="width:50%;margin-left:auto">{% if doc.total_outgoing_value %}<tr><td>Outgoing Value</td><td class="right">{{ doc.total_outgoing_value }}</td></tr>{% endif %}{% if doc.total_incoming_value %}<tr><td>Incoming Value</td><td class="right">{{ doc.total_incoming_value }}</td></tr>{% endif %}{% if doc.total_additional_costs %}<tr><td>Additional Costs</td><td class="right">{{ doc.total_additional_costs }}</td></tr>{% endif %}{% if doc.total_amount %}<tr><td class="bold">Total Amount</td><td class="right bold">{{ doc.total_amount }}</td></tr>{% endif %}</table>""",
	"totals/expense_claim.html": """<table class="epp-totals" style="width:55%;margin-left:auto"><tr><td>Mode of Payment</td><td class="right">{{ doc.mode_of_payment or "—" }}</td></tr><tr><td>Payable Account</td><td class="right">{{ doc.payable_account or "—" }}</td></tr><tr><td>Bank / Cash Account</td><td class="right">{{ doc.bank_or_cash_account or "—" }}</td></tr><tr><td>Total Claimed</td><td class="right">{{ doc.total_claimed_amount or "" }}</td></tr><tr><td>Total Sanctioned</td><td class="right">{{ doc.total_sanctioned_amount or "" }}</td></tr><tr><td class="bold">Grand Total</td><td class="right bold">{{ doc.grand_total or doc.total_sanctioned_amount or "" }}</td></tr></table>""",
	"item_tables/expense_claim.html": """<table class="epp-table"><thead><tr><th>Field</th><th>Value</th></tr></thead><tbody><tr><td>Employee</td><td>{{ doc.employee_name or doc.employee or "" }}</td></tr><tr><td>Mode of Payment</td><td>{{ doc.mode_of_payment or "—" }}</td></tr><tr><td>Payable Account</td><td>{{ doc.payable_account or "—" }}</td></tr><tr><td>Bank / Cash Account</td><td>{{ doc.bank_or_cash_account or "—" }}</td></tr></tbody></table>{% if doc.expenses %}<table class="epp-table" style="margin-top:8px"><thead><tr><th>#</th><th>Expense Type</th><th>Description</th><th>Amount</th><th>Sanctioned</th></tr></thead><tbody>{% for row in doc.expenses %}<tr><td>{{ loop.index }}</td><td>{{ row.expense_type or "" }}</td><td>{{ row.description or "" }}</td><td class="right">{{ row.amount or "" }}</td><td class="right">{{ row.sanctioned_amount or "" }}</td></tr>{% endfor %}</tbody></table>{% endif %}""",
	"item_tables/delivery.html": """{% if doc.items %}<table class="epp-table"><thead><tr><th>Item</th><th>Ordered</th><th>Delivered</th></tr></thead><tbody>{% for row in doc.items %}<tr><td>{{ row.item_code or "" }}</td><td class="right">{{ row.qty or "" }}</td><td class="right">{{ row.qty or "" }}</td></tr>{% endfor %}</tbody></table>{% endif %}""",
	"item_tables/thermal.html": """{% if doc.items %}{% for row in doc.items %}<div>{{ row.item_code or row.item_name or "" }} x {{ row.qty or "" }} @ {{ row.rate or "" }}</div>{% endfor %}{% endif %}""",
	"item_tables/landscape.html": """{% if doc.items %}<table class="epp-table"><thead><tr><th>#</th><th>Code</th><th>Description</th><th>Qty</th><th>UOM</th><th>Rate</th><th>Amount</th></tr></thead><tbody>{% for row in doc.items %}<tr><td>{{ loop.index }}</td><td>{{ row.item_code or "" }}</td><td>{{ row.description or row.item_name or "" }}</td><td class="right">{{ row.qty or "" }}</td><td>{{ row.uom or "" }}</td><td class="right">{{ row.rate or "" }}</td><td class="right">{{ row.amount or "" }}</td></tr>{% endfor %}</tbody></table>{% endif %}""",
	"item_tables/serial_list.html": """{% if doc.items %}{% for row in doc.items %}{% if row.serial_no %}<div>{{ row.item_code or "" }}: {{ row.serial_no }}</div>{% endif %}{% endfor %}{% endif %}""",
	"item_tables/batch_details.html": """{% if doc.items %}{% for row in doc.items %}{% if row.batch_no %}<div>{{ row.item_code or "" }} · Batch {{ row.batch_no }}</div>{% endif %}{% endfor %}{% endif %}""",
	"totals/basic.html": """<table class="epp-totals" style="width:45%;margin-left:auto"><tr><td>Net Total</td><td class="right">{{ doc.get_formatted("net_total") if doc.get_formatted is defined else doc.net_total or "" }}</td></tr><tr><td>Grand Total</td><td class="right bold">{{ doc.get_formatted("grand_total") if doc.get_formatted is defined else doc.grand_total or "" }}</td></tr></table>""",
	"totals/tax_breakdown.html": """<table class="epp-totals" style="width:50%;margin-left:auto"><tr><td>Net Total</td><td class="right">{{ doc.get_formatted("net_total") if doc.get_formatted is defined else doc.net_total or "" }}</td></tr>{% if doc.taxes %}<tr><td colspan="2" class="bold">Taxes</td></tr>{% for tax in doc.taxes %}<tr><td>{{ tax.description or tax.account_head or "" }}</td><td class="right">{{ tax.get_formatted("tax_amount") if tax.get_formatted is defined else tax.tax_amount or "" }}</td></tr>{% endfor %}{% endif %}<tr><td class="bold">Grand Total</td><td class="right bold">{{ doc.get_formatted("grand_total") if doc.get_formatted is defined else doc.grand_total or "" }}</td></tr></table>""",
	"totals/multi_currency.html": """<div class="epp-box">Currency: {{ doc.currency or "" }}{% if doc.conversion_rate and doc.conversion_rate != 1 %} · Rate {{ doc.conversion_rate }}{% endif %}</div>""",
	"totals/discount.html": """<table class="epp-totals" style="width:45%;margin-left:auto"><tr><td>Discount</td><td class="right">{{ doc.get_formatted("discount_amount") if doc.get_formatted is defined else doc.discount_amount or 0 }}</td></tr><tr><td>Grand Total</td><td class="right">{{ doc.get_formatted("grand_total") if doc.get_formatted is defined else doc.grand_total or "" }}</td></tr></table>""",
	"totals/rounded.html": """<table class="epp-totals" style="width:45%;margin-left:auto"><tr><td>Rounded Total</td><td class="right">{{ doc.get_formatted("rounded_total") if doc.get_formatted is defined else doc.rounded_total or doc.grand_total or "" }}</td></tr></table>""",
	"totals/outstanding.html": """<div class="epp-box">Outstanding: {{ doc.get_formatted("outstanding_amount") if doc.get_formatted is defined else doc.outstanding_amount or "" }}</div>""",
	"totals/advance_paid.html": """<div class="epp-box">Advance Paid: {{ doc.get_formatted("advance_paid") if doc.get_formatted is defined else doc.advance_paid or "" }}</div>""",
	"totals/payment_schedule.html": """{% if doc.payment_schedule %}<table class="epp-table"><tr><th>Due Date</th><th>Amount</th></tr>{% for row in doc.payment_schedule %}<tr><td>{{ frappe.utils.formatdate(row.due_date) if row.due_date else "" }}</td><td class="right">{{ row.payment_amount or "" }}</td></tr>{% endfor %}</table>{% endif %}""",
	"totals/amount_in_words.html": """{% if doc.in_words %}<div class="epp-box"><div class="bold">Amount in Words</div><div>{{ doc.in_words }}</div></div>{% endif %}""",
	"totals/bilingual.html": """<div class="epp-box"><span class="bold">Total</span> {{ doc.get_formatted("grand_total") if doc.get_formatted is defined else doc.grand_total or "" }} <span style="float:right;direction:rtl">الإجمالي</span></div>""",
	"qr_blocks/basic.html": """<div class="epp-box center">{% set qr = doc.get("qr_code") or doc.get("custom_qr_code") or doc.get("ksa_einv_qr") or "" %}{% if qr %}<img src="{{ qr }}" style="width:96px;height:96px">{% else %}<div style="border:1px dashed #999;width:96px;height:96px;margin:0 auto;line-height:96px">QR</div>{% endif %}</div>""",
	"qr_blocks/zatca_placeholder.html": """<div class="epp-box center"><div style="border:1px dashed #666;width:120px;height:120px;margin:0 auto;font-size:8px;padding-top:48px">ZATCA QR</div></div>""",
	"barcode_blocks/basic.html": """<div class="epp-box center">{% if doc.name %}<div style="font-family:monospace;letter-spacing:2px">{{ doc.name }}</div>{% endif %}</div>""",
	"signatures/single.html": """<div style="margin-top:18px">Signature ____________________</div>""",
	"signatures/multi.html": """<table style="width:100%;margin-top:18px"><tr><td>Prepared</td><td>Checked</td><td>Approved</td></tr><tr><td>__________</td><td>__________</td><td>__________</td></tr></table>""",
	"signatures/prepared_checked_approved.html": """<table style="width:100%;margin-top:16px"><tr><td>Prepared</td><td>Checked</td><td>Approved</td></tr></table>""",
	"signatures/delivery_acknowledgement.html": """<div style="margin-top:16px">Received in good condition: __________________ Date ________</div>""",
	"signatures/receiver_signature.html": """<div style="margin-top:16px">Receiver Signature __________________</div>""",
	"terms/basic.html": """{% if doc.terms %}<div class="epp-box"><div class="bold">Terms</div><div>{{ doc.terms }}</div></div>{% elif doc.tc_name %}<div class="epp-box">{{ frappe.db.get_value("Terms and Conditions", doc.tc_name, "terms") or "" }}</div>{% endif %}""",
	"terms/notes.html": """{% set _epp_remark = doc.remarks or doc.user_remark or doc.remark or doc.custom_remarks or doc.notes or doc.comment or "" %}{% if _epp_remark %}<div class="epp-box epp-remarks remarks" style="margin-top:12px"><div class="bold">Remarks</div><div>{{ _epp_remark }}</div></div>{% endif %}""",
	"terms/attachments_list.html": """{% if doc.attachments %}<div class="epp-box"><div class="bold">Attachments</div>{% for att in doc.attachments %}<div>{{ att.file_name or att.file_url or "" }}</div>{% endfor %}</div>{% endif %}""",
	"terms/warranty.html": """<div class="epp-box"><div class="bold">Warranty</div><div>Subject to standard warranty terms.</div></div>""",
	"payment_blocks/bank_details.html": """<div class="epp-box"><div class="bold">Bank Details</div><div>{{ doc.get("custom_bank_name") or "" }} {{ doc.get("custom_bank_account_number") or "" }} {{ doc.get("custom_iban") or "" }}</div></div>""",
	"payment_blocks/payment_instructions.html": """<div class="epp-box"><div class="bold">Payment Instructions</div><div>Please reference document {{ doc.name or "" }} on payment.</div></div>""",
	"footers/basic.html": """<div class="epp-footer center">Generated by ERPNext Print Pack · {{ doc.company or "" }}</div>""",
	"footers/page_number.html": """<div class="epp-footer right">Page <span class="page"></span></div>""",
	"tax_summaries/basic.html": """{% if doc.taxes %}<table class="epp-table"><tr><th>Tax</th><th>Amount</th></tr>{% for tax in doc.taxes %}<tr><td>{{ tax.description or tax.account_head or "" }}</td><td class="right">{{ tax.tax_amount or "" }}</td></tr>{% endfor %}</table>{% endif %}""",
	"tax_summaries/detailed.html": """{% if doc.taxes %}<table class="epp-table"><tr><th>Description</th><th>Rate</th><th>Amount</th></tr>{% for tax in doc.taxes %}<tr><td>{{ tax.description or "" }}</td><td class="right">{{ tax.rate or "" }}</td><td class="right">{{ tax.tax_amount or "" }}</td></tr>{% endfor %}</table>{% endif %}""",
}


def write_components():
	for rel, body in COMPONENT_BODIES.items():
		path = COMPONENTS / rel
		path.parent.mkdir(parents=True, exist_ok=True)
		path.write_text(body.strip() + "\n", encoding="utf-8")


def write_themes():
	for key in THEME_REGISTRY:
		path = THEMES / f"{key}.css"
		path.write_text(get_theme_css(key).strip() + "\n", encoding="utf-8")


def pick_components(profile, theme: str) -> list[str]:
	parts = []
	if theme == "thermal":
		parts += ["header_thermal", "items_thermal", "totals_basic", "footer_basic"]
	elif theme == "landscape":
		parts += ["header_landscape", "party_bill_to" if profile.has_party_customer else "party_supplier", "items_landscape", "totals_basic", "footer_basic"]
	elif theme == "bilingual":
		parts += ["header_bilingual", "party_bilingual", "items_basic", "totals_bilingual", "footer_basic"]
	elif theme == "tax_focused":
		parts += ["header_tax_registration", "party_tax_id", "items_tax_inclusive", "tax_summary_detailed", "totals_tax_breakdown", "totals_amount_in_words"]
	elif theme == "qr_enabled":
		parts += ["header_basic", "party_bill_to" if profile.has_party_customer else "party_supplier", "qr_block", "items_basic", "totals_basic"]
	elif theme == "barcode_enabled":
		parts += ["header_compact", "barcode_block", "items_compact", "totals_basic"]
	elif theme == "compact":
		parts += ["header_compact", "party_contact", "items_compact", "totals_basic"]
	elif theme == "executive":
		parts += ["header_logo_left", "party_customer_shipping" if profile.has_party_customer else "party_supplier", "items_basic", "totals_tax_breakdown", "signature_multi", "terms_block"]
	elif theme == "retail" or theme == "wholesale":
		parts += ["header_logo_center", "party_bill_to" if profile.has_party_customer else "party_supplier", "items_basic", "totals_basic", "payment_instructions"]
	elif profile.has_items and profile.category in ("stock", "manufacturing"):
		parts += ["header_basic", "items_warehouse" if profile.category == "stock" else "items_manufacturing", "totals_basic"]
	elif profile.doc_type == "Payment Entry":
		parts += ["header_document_number", "items_payment_details", "totals_payment", "signature_single", "notes_block", "footer_basic"]
	elif profile.doc_type == "Journal Entry":
		parts += ["header_document_number", "items_journal_accounts", "totals_journal", "signature_multi", "notes_block", "footer_basic"]
	elif profile.doc_type == "Stock Entry":
		parts += ["header_basic", "items_stock_entry", "totals_stock_entry", "signature_multi", "notes_block", "footer_basic"]
	elif profile.doc_type == "Expense Claim":
		parts += ["header_document_number", "items_expense_claim", "totals_expense_claim", "signature_multi", "notes_block", "footer_basic"]
	elif profile.doc_type in ("Item", "Batch", "Serial No"):
		parts += ["header_compact", "barcode_block", "notes_block"]
	else:
		parts += ["header_basic"]
		if profile.has_party_customer:
			parts.append("party_bill_to")
		if profile.has_party_supplier:
			parts.append("party_supplier")
		if profile.has_items:
			parts.append("items_basic")
		parts += ["totals_basic"]
		if profile.has_in_words:
			parts.append("totals_amount_in_words")
		if profile.has_terms:
			parts.append("terms_block")
		parts.append("signature_single")
		parts.append("notes_block")
		parts.append("footer_basic")
	return parts


def build_html(profile, theme: str, title: str) -> str:
	from erpnext_print_pack.components.registry import load_component

	css = get_theme_css(theme)
	parts = []
	for key in pick_components(profile, theme):
		body = load_component(key)
		if body:
			parts.append(body)

	date_field = profile.date_field
	html = f"""{{# Generated by erpnext_print_pack · {profile.doc_type} · {theme} · original #}}
{{% set title = "{title}" %}}
{{% set date_field = "{date_field}" %}}
<style>
{css}
.print-format .epp-table > tbody > tr > td {{ padding: 0 !important; }}
</style>
<div class="epp-root print-format">
{chr(10).join(parts)}
</div>
"""
	return html


def format_slug(profile_slug: str, theme: str) -> str:
	return f"{profile_slug}_{theme}"


def format_name(profile, theme: str) -> str:
	label = THEME_REGISTRY[theme]["label"]
	return f"{label} {profile.title}"


def checksum(content: str) -> str:
	return hashlib.sha256(content.encode("utf-8")).hexdigest()


def write_format(profile, theme: str, status: str):
	slug = format_slug(profile.slug, theme)
	if slug in PRESERVE_SLUGS:
		return None
	name = format_name(profile, theme)
	fdir = FORMATS / slug
	fdir.mkdir(parents=True, exist_ok=True)
	html = build_html(profile, theme, profile.title)
	orientation = THEME_REGISTRY[theme].get("orientation", profile.orientation_default)
	paper = THEME_REGISTRY[theme].get("paper", profile.paper_default)
	features = []
	if profile.has_taxes:
		features.append("tax-summary")
	if profile.has_in_words:
		features.append("amount-in-words")
	if theme == "bilingual":
		features.append("bilingual")
	if theme == "qr_enabled":
		features.append("qr")
	if theme == "barcode_enabled":
		features.append("barcode")
	if theme == "landscape":
		features.append("landscape")
	if theme == "thermal":
		features.append("thermal")

	meta = {
		"name": name,
		"slug": slug,
		"doc_type": profile.doc_type,
		"theme": theme,
		"category": profile.category,
		"orientation": orientation,
		"paper_size": paper,
		"languages": ["en", "ar"] if theme == "bilingual" else ["en"],
		"features": features,
		"source_type": "original",
		"source_url": None,
		"source_license": "MIT",
		"attribution_required": False,
		"erpnext_versions": ["15", "16"],
		"status": status,
		"checksum": checksum(html),
	}
	(fdir / "metadata.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
	pf = {
		"doctype": "Print Format",
		"name": name,
		"doc_type": profile.doc_type,
		"module": "Print Pack",
		"custom_format": 1,
		"print_format_type": "Jinja",
		"standard": "No",
		"disabled": 0 if status == "stable" else 1,
		"default_print_language": "en",
		"margin_top": 6.0,
		"margin_bottom": 6.0,
		"margin_left": 8.0,
		"margin_right": 8.0,
		"page_number": "Hide",
		"css": "",
	}
	(fdir / f"{slug}.json").write_text(json.dumps(pf, indent=1) + "\n", encoding="utf-8")
	(fdir / f"{slug}.html").write_text(html, encoding="utf-8")
	(fdir / "README.md").write_text(
		f"# {name}\n\nDocType: **{profile.doc_type}** · Theme: **{theme}** · Status: **{status}**\n",
		encoding="utf-8",
	)
	return meta


def generate_all():
	manifest = {"generated_on": str(date.today()), "formats": [], "deferred_doctypes": DEFERRED_DOCTYPES}
	stable_count = 0
	draft_count = 0
	for profile in PROFILES.values():
		for i, theme in enumerate(profile.supported_themes):
			# first 3 themes per doctype stable, rest draft unless high-priority doctype
			if profile.slug == "sales_invoice":
				status = "stable" if i < 12 else ("draft" if i < 20 else "draft")
			elif profile.category in ("sales", "purchasing", "payments"):
				status = "stable" if i < 3 else "draft"
			else:
				status = "stable" if i < 2 else "draft"
			meta = write_format(profile, theme, status)
			if meta:
				manifest["formats"].append(meta)
				if status == "stable":
					stable_count += 1
				else:
					draft_count += 1
	MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
	return len(manifest["formats"]), stable_count, draft_count


def main():
	write_components()
	write_themes()
	total, stable, draft = generate_all()
	print(f"Components: {len(COMPONENT_BODIES)}")
	print(f"Themes: {len(THEME_REGISTRY)}")
	print(f"Formats: {total} (stable={stable}, draft={draft})")


if __name__ == "__main__":
	main()
