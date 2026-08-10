"""DocType-specific print detail blocks (accounts, references, stock lines, etc.)."""

from __future__ import annotations

from erpnext_print_pack.doctype_profiles import DocTypeProfile

REMARKS_BLOCK = """
{% set _epp_remark = doc.remarks or doc.user_remark or doc.remark or doc.custom_remarks or doc.notes or doc.comment or doc.description or "" %}
{% if _epp_remark %}
<div class="epp-remarks remarks" style="margin-top:14px;padding:10px 12px;border:1px solid #d1d5db;border-radius:4px;background:#fafafa">
<strong>Remarks</strong><br>
{{ _epp_remark }}
</div>
{% endif %}
"""


def remarks_block(profile: DocTypeProfile | None = None) -> str:
	"""Always render remarks at the bottom of print formats."""
	return REMARKS_BLOCK


def party_vars(profile: DocTypeProfile) -> str:
	if profile.doc_type == "Payment Entry":
		return """
{% set party_label = doc.party_type or "Party" %}
{% set ship_label = "" %}
{% set party_name = doc.party_name or doc.party or "" %}
{% set party_address = doc.party_address or doc.address_display or "" %}
{% set ship_address = "" %}
"""
	if profile.doc_type == "Journal Entry":
		return """
{% set party_label = "Pay to / Received from" %}
{% set ship_label = "" %}
{% set party_name = doc.pay_to_recd_from or "" %}
{% set party_address = "" %}
{% set ship_address = "" %}
"""
	if profile.doc_type == "Stock Entry":
		return """
{% set party_label = "Supplier" %}
{% set ship_label = "" %}
{% set party_name = doc.supplier_name or doc.supplier or "" %}
{% set party_address = doc.address_display or doc.supplier_address or "" %}
{% set ship_address = "" %}
"""
	if profile.has_party_customer:
		return """
{% set party_label = "Bill To" %}
{% set ship_label = "Ship To" %}
{% set party_name = doc.customer_name or doc.customer or doc.party_name or "" %}
{% set party_address = doc.address_display or "" %}
{% set ship_address = doc.shipping_address or doc.shipping_address_display or "" %}
"""
	if profile.has_party_supplier:
		return """
{% set party_label = "Supplier" %}
{% set ship_label = "Deliver To" %}
{% set party_name = doc.supplier_name or doc.supplier or "" %}
{% set party_address = doc.address_display or doc.supplier_address or "" %}
{% set ship_address = doc.shipping_address_display or "" %}
"""
	if profile.party_field == "employee":
		return """
{% set party_label = "Employee" %}
{% set ship_label = "" %}
{% set party_name = doc.employee_name or doc.employee or "" %}
{% set party_address = "" %}
{% set ship_address = "" %}
"""
	return """
{% set party_label = "Party" %}
{% set ship_label = "" %}
{% set party_name = doc.party_name or doc.party or "" %}
{% set party_address = doc.address_display or "" %}
{% set ship_address = "" %}
"""


def meta_header(profile: DocTypeProfile) -> str:
	dt = profile.doc_type
	if dt == "Expense Claim":
		return """
<table class="meta">
<tr><td>Claim No</td><td class="r bold">{{ doc.name }}</td></tr>
<tr><td>Date</td><td class="r">{{ frappe.utils.formatdate(doc.posting_date) if doc.posting_date else "" }}</td></tr>
<tr><td>Employee</td><td class="r">{{ doc.employee_name or doc.employee or "" }}</td></tr>
{% if doc.department %}<tr><td>Department</td><td class="r">{{ doc.department }}</td></tr>{% endif %}
<tr><td>Approval Status</td><td class="r">{{ doc.approval_status or doc.status or "" }}</td></tr>
{% if doc.mode_of_payment %}<tr><td>Mode of Payment</td><td class="r">{{ doc.mode_of_payment }}</td></tr>{% endif %}
{% if doc.payable_account %}<tr><td>Payable Account</td><td class="r">{{ doc.payable_account }}</td></tr>{% endif %}
{% if doc.bank_or_cash_account %}<tr><td>Bank / Cash Account</td><td class="r">{{ doc.bank_or_cash_account }}</td></tr>{% endif %}
{% if doc.is_paid %}<tr><td>Paid</td><td class="r">Yes</td></tr>{% endif %}
</table>
"""
	if dt == "Journal Entry":
		return """
<table class="meta">
<tr><td>Voucher No</td><td class="r bold">{{ doc.name }}</td></tr>
<tr><td>Date</td><td class="r">{{ frappe.utils.formatdate(doc.posting_date) if doc.posting_date else "" }}</td></tr>
<tr><td>Voucher Type</td><td class="r">{{ doc.voucher_type or "" }}</td></tr>
{% if doc.cheque_no %}<tr><td>Cheque No</td><td class="r">{{ doc.cheque_no }}</td></tr>{% endif %}
{% if doc.cheque_date %}<tr><td>Cheque Date</td><td class="r">{{ frappe.utils.formatdate(doc.cheque_date) }}</td></tr>{% endif %}
{% if doc.mode_of_payment %}<tr><td>Mode of Payment</td><td class="r">{{ doc.mode_of_payment }}</td></tr>{% endif %}
{% if doc.bill_no %}<tr><td>Bill No</td><td class="r">{{ doc.bill_no }}</td></tr>{% endif %}
</table>
"""
	if dt == "Payment Entry":
		return """
<table class="meta">
<tr><td>Payment No</td><td class="r bold">{{ doc.name }}</td></tr>
<tr><td>Date</td><td class="r">{{ frappe.utils.formatdate(doc.posting_date) if doc.posting_date else "" }}</td></tr>
<tr><td>Payment Type</td><td class="r">{{ doc.payment_type or "" }}</td></tr>
<tr><td>Mode of Payment</td><td class="r">{{ doc.mode_of_payment or "—" }}</td></tr>
{% if doc.reference_no %}<tr><td>Reference No</td><td class="r">{{ doc.reference_no }}</td></tr>{% endif %}
{% if doc.reference_date %}<tr><td>Reference Date</td><td class="r">{{ frappe.utils.formatdate(doc.reference_date) }}</td></tr>{% endif %}
{% if doc.status %}<tr><td>Status</td><td class="r">{{ doc.status }}</td></tr>{% endif %}
</table>
"""
	if dt == "Stock Entry":
		return """
<table class="meta">
<tr><td>Stock Entry</td><td class="r bold">{{ doc.name }}</td></tr>
<tr><td>Date</td><td class="r">{{ frappe.utils.formatdate(doc.posting_date) if doc.posting_date else "" }}{% if doc.posting_time %} {{ doc.posting_time }}{% endif %}</td></tr>
<tr><td>Type</td><td class="r">{{ doc.stock_entry_type or doc.purpose or "" }}</td></tr>
{% if doc.from_warehouse %}<tr><td>From Warehouse</td><td class="r">{{ doc.from_warehouse }}</td></tr>{% endif %}
{% if doc.to_warehouse %}<tr><td>To Warehouse</td><td class="r">{{ doc.to_warehouse }}</td></tr>{% endif %}
{% if doc.work_order %}<tr><td>Work Order</td><td class="r">{{ doc.work_order }}</td></tr>{% endif %}
{% if doc.bom_no %}<tr><td>BOM</td><td class="r">{{ doc.bom_no }}</td></tr>{% endif %}
{% if doc.project %}<tr><td>Project</td><td class="r">{{ doc.project }}</td></tr>{% endif %}
</table>
"""
	if dt == "Material Request":
		return f"""
<table class="meta">
<tr><td>Document</td><td class="r bold">{{{{ doc.name }}}}</td></tr>
<tr><td>Date</td><td class="r">{{{{ frappe.utils.formatdate(doc.get("{profile.date_field}")) if doc.get("{profile.date_field}") else "" }}}}</td></tr>
<tr><td>Type</td><td class="r">{{{{ doc.material_request_type or "" }}}}</td></tr>
{{% if doc.schedule_date %}}<tr><td>Required By</td><td class="r">{{{{ frappe.utils.formatdate(doc.schedule_date) }}}}</td></tr>{{% endif %}}
{{% if doc.status %}}<tr><td>Status</td><td class="r">{{{{ doc.status }}}}</td></tr>{{% endif %}}
</table>
"""
	if dt == "Work Order":
		return """
<table class="meta">
<tr><td>Work Order</td><td class="r bold">{{ doc.name }}</td></tr>
<tr><td>Item</td><td class="r">{{ doc.production_item or doc.item_name or "" }}</td></tr>
<tr><td>Qty</td><td class="r">{{ doc.qty or "" }}</td></tr>
{% if doc.bom_no %}<tr><td>BOM</td><td class="r">{{ doc.bom_no }}</td></tr>{% endif %}
{% if doc.planned_start_date %}<tr><td>Planned Start</td><td class="r">{{ frappe.utils.format_datetime(doc.planned_start_date) }}</td></tr>{% endif %}
{% if doc.status %}<tr><td>Status</td><td class="r">{{ doc.status }}</td></tr>{% endif %}
</table>
"""
	due = (
		'{% if doc.due_date %}<tr><td>Due Date</td><td class="r">{{ frappe.utils.formatdate(doc.due_date) }}</td></tr>{% endif %}'
		if profile.has_due_date
		else ""
	)
	return f"""
<table class="meta">
<tr><td>Document</td><td class="r bold">{{{{ doc.name }}}}</td></tr>
<tr><td>Date</td><td class="r">{{{{ frappe.utils.formatdate(doc.get("{profile.date_field}")) if doc.get("{profile.date_field}") else "" }}}}</td></tr>
{due}
{{% if doc.currency %}}<tr><td>Currency</td><td class="r">{{{{ doc.currency }}}}</td></tr>{{% endif %}}
{{% if doc.status %}}<tr><td>Status</td><td class="r">{{{{ doc.status }}}}</td></tr>{{% endif %}}
{{% if doc.cost_center %}}<tr><td>Cost Center</td><td class="r">{{{{ doc.cost_center }}}}</td></tr>{{% endif %}}
{{% if doc.project %}}<tr><td>Project</td><td class="r">{{{{ doc.project }}}}</td></tr>{{% endif %}}
</table>
"""


def detail_table(profile: DocTypeProfile) -> str:
	"""Primary line table for the DocType (items / accounts / references)."""
	dt = profile.doc_type
	if dt == "Journal Entry":
		return _journal_accounts_table()
	if dt == "Payment Entry":
		return _payment_detail_tables()
	if dt == "Stock Entry":
		return _stock_entry_items_table()
	if dt == "Material Request":
		return _material_request_items_table()
	if dt == "Work Order":
		return _work_order_tables()
	if dt == "Salary Slip":
		return _salary_slip_tables()
	if dt == "Expense Claim":
		return _expense_claim_table()
	if dt == "Timesheet":
		return _timesheet_table()
	if dt == "BOM":
		return _bom_items_table()
	if dt == "Item":
		return _item_master_detail_block()
	if dt in ("Batch", "Serial No"):
		return ""
	if not profile.has_items:
		return ""
	if profile.category in ("stock", "manufacturing"):
		return _stockish_items_table()
	if profile.has_taxes:
		return _commercial_items_table(include_tax=True)
	return _commercial_items_table(include_tax=False)


def totals_block(profile: DocTypeProfile) -> str:
	"""Totals only — remarks are rendered separately at the bottom."""
	dt = profile.doc_type
	if dt == "Journal Entry":
		return """
<table class="totals">
<tr><td>Total Debit</td><td class="r">{{ doc.get_formatted("total_debit") if doc.get_formatted is defined else doc.total_debit or "" }}</td></tr>
<tr><td>Total Credit</td><td class="r">{{ doc.get_formatted("total_credit") if doc.get_formatted is defined else doc.total_credit or "" }}</td></tr>
{% if doc.difference %}<tr><td>Difference</td><td class="r">{{ doc.get_formatted("difference") if doc.get_formatted is defined else doc.difference }}</td></tr>{% endif %}
{% if doc.total_amount %}<tr class="grand"><td>Total Amount</td><td class="r">{{ doc.get_formatted("total_amount") if doc.get_formatted is defined else doc.total_amount }}</td></tr>{% endif %}
</table>
{% if doc.total_amount_in_words %}<div class="words">{{ doc.total_amount_in_words }}</div>{% endif %}
"""
	if dt == "Payment Entry":
		return """
<table class="totals">
{% set _pay_amt = doc.paid_amount or doc.received_amount or doc.base_paid_amount or 0 %}
{% set _pay_cur = doc.paid_to_account_currency or doc.paid_from_account_currency or doc.company_currency or "" %}
<tr><td>Paid Amount</td><td class="r">{{ frappe.utils.fmt_money(doc.paid_amount, currency=doc.paid_from_account_currency or _pay_cur) if doc.paid_amount else "" }}</td></tr>
{% if doc.received_amount %}<tr><td>Received Amount</td><td class="r">{{ frappe.utils.fmt_money(doc.received_amount, currency=doc.paid_to_account_currency or _pay_cur) }}</td></tr>{% endif %}
{% if doc.total_allocated_amount %}<tr><td>Allocated</td><td class="r">{{ doc.get_formatted("total_allocated_amount") if doc.get_formatted is defined else doc.total_allocated_amount }}</td></tr>{% endif %}
{% if doc.unallocated_amount %}<tr><td>Unallocated</td><td class="r">{{ doc.get_formatted("unallocated_amount") if doc.get_formatted is defined else doc.unallocated_amount }}</td></tr>{% endif %}
{% if doc.difference_amount %}<tr><td>Difference</td><td class="r">{{ doc.get_formatted("difference_amount") if doc.get_formatted is defined else doc.difference_amount }}</td></tr>{% endif %}
{% if doc.total_taxes_and_charges %}<tr><td>Taxes</td><td class="r">{{ doc.get_formatted("total_taxes_and_charges") if doc.get_formatted is defined else doc.total_taxes_and_charges }}</td></tr>{% endif %}
<tr class="grand"><td>Amount</td><td class="r">{{ frappe.utils.fmt_money(_pay_amt, currency=_pay_cur) if _pay_amt else "" }}</td></tr>
</table>
{% if doc.in_words or doc.base_in_words %}<div class="words">{{ doc.in_words or doc.base_in_words }}</div>{% endif %}
"""
	if dt == "Expense Claim":
		return """
<table class="totals">
<tr><td>Mode of Payment</td><td class="r"><strong>{{ doc.mode_of_payment or "—" }}</strong></td></tr>
<tr><td>Payable Account</td><td class="r">{{ doc.payable_account or "—" }}</td></tr>
<tr><td>Bank / Cash Account</td><td class="r">{{ doc.bank_or_cash_account or "—" }}</td></tr>
{% if doc.cost_center %}<tr><td>Cost Center</td><td class="r">{{ doc.cost_center }}</td></tr>{% endif %}
<tr><td>Total Claimed</td><td class="r">{{ doc.get_formatted("total_claimed_amount") if doc.get_formatted is defined else doc.total_claimed_amount or "" }}</td></tr>
<tr><td>Total Sanctioned</td><td class="r">{{ doc.get_formatted("total_sanctioned_amount") if doc.get_formatted is defined else doc.total_sanctioned_amount or "" }}</td></tr>
{% if doc.total_advance_amount %}<tr><td>Advance</td><td class="r">{{ doc.get_formatted("total_advance_amount") if doc.get_formatted is defined else doc.total_advance_amount }}</td></tr>{% endif %}
{% if doc.total_taxes_and_charges %}<tr><td>Taxes</td><td class="r">{{ doc.get_formatted("total_taxes_and_charges") if doc.get_formatted is defined else doc.total_taxes_and_charges }}</td></tr>{% endif %}
<tr class="grand"><td>Grand Total</td><td class="r">{{ doc.get_formatted("grand_total") if doc.get_formatted is defined else doc.grand_total or doc.total_sanctioned_amount or "" }}</td></tr>
{% if doc.total_amount_reimbursed %}<tr><td>Reimbursed</td><td class="r">{{ doc.get_formatted("total_amount_reimbursed") if doc.get_formatted is defined else doc.total_amount_reimbursed }}</td></tr>{% endif %}
</table>
"""
	if dt == "Stock Entry":
		return """
<table class="totals">
{% if doc.total_outgoing_value %}<tr><td>Outgoing Value</td><td class="r">{{ doc.get_formatted("total_outgoing_value") if doc.get_formatted is defined else doc.total_outgoing_value }}</td></tr>{% endif %}
{% if doc.total_incoming_value %}<tr><td>Incoming Value</td><td class="r">{{ doc.get_formatted("total_incoming_value") if doc.get_formatted is defined else doc.total_incoming_value }}</td></tr>{% endif %}
{% if doc.total_additional_costs %}<tr><td>Additional Costs</td><td class="r">{{ doc.get_formatted("total_additional_costs") if doc.get_formatted is defined else doc.total_additional_costs }}</td></tr>{% endif %}
{% if doc.value_difference %}<tr><td>Value Difference</td><td class="r">{{ doc.get_formatted("value_difference") if doc.get_formatted is defined else doc.value_difference }}</td></tr>{% endif %}
{% if doc.total_amount %}<tr class="grand"><td>Total Amount</td><td class="r">{{ doc.get_formatted("total_amount") if doc.get_formatted is defined else doc.total_amount }}</td></tr>{% endif %}
</table>
"""
	if not profile.has_items and not profile.has_taxes:
		return ""
	if not profile.has_taxes:
		return """
<table class="totals">
<tr><td>Total</td><td class="r">{{ doc.get_formatted("grand_total") if doc.get_formatted is defined else doc.grand_total or doc.total or doc.total_amount or "" }}</td></tr>
{% if doc.rounded_total %}<tr><td>Rounded Total</td><td class="r">{{ doc.get_formatted("rounded_total") if doc.get_formatted is defined else doc.rounded_total }}</td></tr>{% endif %}
{% if doc.outstanding_amount %}<tr><td>Outstanding</td><td class="r">{{ doc.get_formatted("outstanding_amount") if doc.get_formatted is defined else doc.outstanding_amount }}</td></tr>{% endif %}
</table>
"""
	return """
<table class="totals">
<tr><td>Net Total</td><td class="r">{{ doc.get_formatted("net_total") if doc.get_formatted is defined else doc.net_total or "" }}</td></tr>
{% if doc.discount_amount %}<tr><td>Discount</td><td class="r">{{ doc.get_formatted("discount_amount") if doc.get_formatted is defined else doc.discount_amount }}</td></tr>{% endif %}
{% for tax in doc.taxes or [] %}<tr><td>{{ tax.description or tax.account_head or "Tax" }}</td><td class="r">{{ tax.get_formatted("tax_amount") if tax.get_formatted is defined else tax.tax_amount or "" }}</td></tr>{% endfor %}
<tr class="grand"><td>Grand Total</td><td class="r">{{ doc.get_formatted("grand_total") if doc.get_formatted is defined else doc.grand_total or "" }}</td></tr>
{% if doc.rounded_total %}<tr><td>Rounded Total</td><td class="r">{{ doc.get_formatted("rounded_total") if doc.get_formatted is defined else doc.rounded_total }}</td></tr>{% endif %}
{% if doc.outstanding_amount %}<tr><td>Outstanding</td><td class="r">{{ doc.get_formatted("outstanding_amount") if doc.get_formatted is defined else doc.outstanding_amount }}</td></tr>{% endif %}
{% if doc.advance_paid %}<tr><td>Advance Paid</td><td class="r">{{ doc.get_formatted("advance_paid") if doc.get_formatted is defined else doc.advance_paid }}</td></tr>{% endif %}
</table>
"""


def _journal_accounts_table() -> str:
	return """
{% if doc.accounts %}
<table class="items">
<thead>
<tr>
<th>#</th>
<th>Account</th>
<th>Party</th>
<th>Cost Center</th>
<th>Against</th>
<th class="r">Debit</th>
<th class="r">Credit</th>
</tr>
</thead>
<tbody>
{% for row in doc.accounts %}
<tr>
<td>{{ loop.index }}</td>
<td><strong>{{ row.account or "" }}</strong>{% if row.account_type %}<br><small>{{ row.account_type }}</small>{% endif %}{% if row.user_remark %}<br><small>{{ row.user_remark }}</small>{% endif %}</td>
<td>{{ row.party_type or "" }}{% if row.party %} {{ row.party }}{% endif %}</td>
<td>{{ row.cost_center or "" }}</td>
<td>{{ row.against_account or "" }}</td>
<td class="r">{{ row.get_formatted("debit_in_account_currency") if row.get_formatted is defined else row.debit_in_account_currency or row.debit or "" }}</td>
<td class="r">{{ row.get_formatted("credit_in_account_currency") if row.get_formatted is defined else row.credit_in_account_currency or row.credit or "" }}</td>
</tr>
{% endfor %}
</tbody>
</table>
{% endif %}
"""


def _payment_detail_tables() -> str:
	return """
<table class="items" style="margin-bottom:10px">
<thead><tr><th>Field</th><th>Value</th></tr></thead>
<tbody>
<tr><td>Party Type</td><td>{{ doc.party_type or "" }}</td></tr>
<tr><td>Party</td><td><strong>{{ doc.party_name or doc.party or "" }}</strong></td></tr>
<tr><td>Paid From</td><td>{{ doc.paid_from or "" }}{% if doc.paid_from_account_currency %} ({{ doc.paid_from_account_currency }}){% endif %}</td></tr>
<tr><td>Paid To</td><td>{{ doc.paid_to or "" }}{% if doc.paid_to_account_currency %} ({{ doc.paid_to_account_currency }}){% endif %}</td></tr>
{% if doc.bank_account %}<tr><td>Bank Account</td><td>{{ doc.bank_account }}</td></tr>{% endif %}
{% if doc.party_bank_account %}<tr><td>Party Bank</td><td>{{ doc.party_bank_account }}</td></tr>{% endif %}
{% if doc.bank %}<tr><td>Bank</td><td>{{ doc.bank }}{% if doc.bank_account_no %} · {{ doc.bank_account_no }}{% endif %}</td></tr>{% endif %}
{% if doc.cost_center %}<tr><td>Cost Center</td><td>{{ doc.cost_center }}</td></tr>{% endif %}
{% if doc.project %}<tr><td>Project</td><td>{{ doc.project }}</td></tr>{% endif %}
</tbody>
</table>
{% if doc.references %}
<table class="items">
<thead>
<tr>
<th>#</th>
<th>Type</th>
<th>Reference</th>
<th>Due Date</th>
<th class="r">Outstanding</th>
<th class="r">Allocated</th>
</tr>
</thead>
<tbody>
{% for row in doc.references %}
<tr>
<td>{{ loop.index }}</td>
<td>{{ row.reference_doctype or "" }}</td>
<td><strong>{{ row.reference_name or "" }}</strong>{% if row.bill_no %}<br><small>Bill: {{ row.bill_no }}</small>{% endif %}</td>
<td>{{ frappe.utils.formatdate(row.due_date) if row.due_date else "" }}</td>
<td class="r">{{ row.get_formatted("outstanding_amount") if row.get_formatted is defined else row.outstanding_amount or "" }}</td>
<td class="r">{{ row.get_formatted("allocated_amount") if row.get_formatted is defined else row.allocated_amount or "" }}</td>
</tr>
{% endfor %}
</tbody>
</table>
{% endif %}
{% if doc.deductions %}
<table class="items" style="margin-top:10px">
<thead><tr><th>#</th><th>Account</th><th>Cost Center</th><th class="r">Amount</th></tr></thead>
<tbody>
{% for row in doc.deductions %}
<tr>
<td>{{ loop.index }}</td>
<td>{{ row.account or "" }}</td>
<td>{{ row.cost_center or "" }}</td>
<td class="r">{{ row.get_formatted("amount") if row.get_formatted is defined else row.amount or "" }}</td>
</tr>
{% endfor %}
</tbody>
</table>
{% endif %}
{% if doc.taxes %}
<table class="items" style="margin-top:10px">
<thead><tr><th>Tax</th><th class="r">Rate</th><th class="r">Amount</th></tr></thead>
<tbody>
{% for tax in doc.taxes %}
<tr>
<td>{{ tax.description or tax.account_head or "Tax" }}</td>
<td class="r">{{ tax.rate or "" }}</td>
<td class="r">{{ tax.get_formatted("tax_amount") if tax.get_formatted is defined else tax.tax_amount or "" }}</td>
</tr>
{% endfor %}
</tbody>
</table>
{% endif %}
"""


def _stock_entry_items_table() -> str:
	return """
{% if doc.items %}
<table class="items">
<thead>
<tr>
<th>#</th>
<th>Item</th>
<th>From WH</th>
<th>To WH</th>
<th class="r">Qty</th>
<th>UOM</th>
<th class="r">Basic Rate</th>
<th class="r">Amount</th>
<th>Batch / Serial</th>
</tr>
</thead>
<tbody>
{% for row in doc.items %}
<tr>
<td>{{ loop.index }}</td>
<td><strong>{{ row.item_code or "" }}</strong>{% if row.item_name and row.item_name != row.item_code %}<br>{{ row.item_name }}{% endif %}{% if row.description and row.description != row.item_name %}<br><small>{{ row.description }}</small>{% endif %}</td>
<td>{{ row.s_warehouse or "" }}</td>
<td>{{ row.t_warehouse or "" }}</td>
<td class="r">{{ row.get_formatted("qty") if row.get_formatted is defined else row.qty or "" }}</td>
<td>{{ row.uom or row.stock_uom or "" }}</td>
<td class="r">{{ row.get_formatted("basic_rate") if row.get_formatted is defined else row.basic_rate or row.valuation_rate or "" }}</td>
<td class="r">{{ row.get_formatted("amount") if row.get_formatted is defined else row.amount or row.basic_amount or "" }}</td>
<td>{% if row.batch_no %}Batch: {{ row.batch_no }}{% endif %}{% if row.serial_no %}<br><small>{{ row.serial_no }}</small>{% endif %}</td>
</tr>
{% endfor %}
</tbody>
</table>
{% endif %}
{% if doc.additional_costs %}
<table class="items" style="margin-top:10px">
<thead><tr><th>#</th><th>Expense Account</th><th>Description</th><th class="r">Amount</th></tr></thead>
<tbody>
{% for row in doc.additional_costs %}
<tr>
<td>{{ loop.index }}</td>
<td>{{ row.expense_account or "" }}</td>
<td>{{ row.description or "" }}</td>
<td class="r">{{ row.get_formatted("amount") if row.get_formatted is defined else row.amount or "" }}</td>
</tr>
{% endfor %}
</tbody>
</table>
{% endif %}
"""


def _material_request_items_table() -> str:
	return """
{% if doc.items %}
<table class="items">
<thead>
<tr>
<th>#</th>
<th>Item</th>
<th>Warehouse</th>
<th class="r">Qty</th>
<th>UOM</th>
<th>Required By</th>
<th class="r">Ordered</th>
<th class="r">Received</th>
</tr>
</thead>
<tbody>
{% for row in doc.items %}
<tr>
<td>{{ loop.index }}</td>
<td><strong>{{ row.item_code or "" }}</strong>{% if row.item_name %}<br>{{ row.item_name }}{% endif %}{% if row.description %}<br><small>{{ row.description }}</small>{% endif %}</td>
<td>{{ row.warehouse or "" }}</td>
<td class="r">{{ row.qty or "" }}</td>
<td>{{ row.uom or row.stock_uom or "" }}</td>
<td>{{ frappe.utils.formatdate(row.schedule_date) if row.schedule_date else "" }}</td>
<td class="r">{{ row.ordered_qty or 0 }}</td>
<td class="r">{{ row.received_qty or 0 }}</td>
</tr>
{% endfor %}
</tbody>
</table>
{% endif %}
"""


def _work_order_tables() -> str:
	return """
{% if doc.required_items %}
<table class="items">
<thead><tr><th>#</th><th>Required Item</th><th>Source WH</th><th class="r">Required Qty</th><th class="r">Transferred</th><th class="r">Consumed</th></tr></thead>
<tbody>
{% for row in doc.required_items %}
<tr>
<td>{{ loop.index }}</td>
<td><strong>{{ row.item_code or "" }}</strong>{% if row.item_name %}<br>{{ row.item_name }}{% endif %}</td>
<td>{{ row.source_warehouse or "" }}</td>
<td class="r">{{ row.required_qty or "" }}</td>
<td class="r">{{ row.transferred_qty or 0 }}</td>
<td class="r">{{ row.consumed_qty or 0 }}</td>
</tr>
{% endfor %}
</tbody>
</table>
{% endif %}
"""


def _salary_slip_tables() -> str:
	return """
{% if doc.earnings %}
<table class="items">
<thead><tr><th>#</th><th>Earnings</th><th class="r">Amount</th></tr></thead>
<tbody>
{% for row in doc.earnings %}
<tr><td>{{ loop.index }}</td><td>{{ row.salary_component or "" }}</td><td class="r">{{ row.get_formatted("amount") if row.get_formatted is defined else row.amount or "" }}</td></tr>
{% endfor %}
</tbody>
</table>
{% endif %}
{% if doc.deductions %}
<table class="items" style="margin-top:10px">
<thead><tr><th>#</th><th>Deductions</th><th class="r">Amount</th></tr></thead>
<tbody>
{% for row in doc.deductions %}
<tr><td>{{ loop.index }}</td><td>{{ row.salary_component or "" }}</td><td class="r">{{ row.get_formatted("amount") if row.get_formatted is defined else row.amount or "" }}</td></tr>
{% endfor %}
</tbody>
</table>
{% endif %}
"""


def _expense_claim_table() -> str:
	return """
<table class="items" style="margin-bottom:10px">
<thead><tr><th>Field</th><th>Value</th></tr></thead>
<tbody>
<tr><td>Employee</td><td><strong>{{ doc.employee_name or doc.employee or "" }}</strong>{% if doc.department %} · {{ doc.department }}{% endif %}</td></tr>
<tr><td>Mode of Payment</td><td>{{ doc.mode_of_payment or "—" }}</td></tr>
<tr><td>Payable Account</td><td>{{ doc.payable_account or "—" }}</td></tr>
<tr><td>Bank / Cash Account</td><td>{{ doc.bank_or_cash_account or "—" }}</td></tr>
{% if doc.cost_center %}<tr><td>Cost Center</td><td>{{ doc.cost_center }}</td></tr>{% endif %}
{% if doc.project %}<tr><td>Project</td><td>{{ doc.project }}</td></tr>{% endif %}
<tr><td>Approval / Status</td><td>{{ doc.approval_status or "" }}{% if doc.status %} · {{ doc.status }}{% endif %}</td></tr>
</tbody>
</table>
{% if doc.expenses %}
<table class="items">
<thead><tr><th>#</th><th>Expense Type</th><th>Description</th><th>Date</th><th class="r">Amount</th><th class="r">Sanctioned</th></tr></thead>
<tbody>
{% for row in doc.expenses %}
<tr>
<td>{{ loop.index }}</td>
<td>{{ row.expense_type or "" }}</td>
<td>{{ row.description or "" }}</td>
<td>{{ frappe.utils.formatdate(row.expense_date) if row.expense_date else "" }}</td>
<td class="r">{{ row.get_formatted("amount") if row.get_formatted is defined else row.amount or "" }}</td>
<td class="r">{{ row.get_formatted("sanctioned_amount") if row.get_formatted is defined else row.sanctioned_amount or "" }}</td>
</tr>
{% endfor %}
</tbody>
</table>
{% endif %}
{% if doc.taxes %}
<table class="items" style="margin-top:10px">
<thead><tr><th>Tax</th><th class="r">Rate</th><th class="r">Amount</th></tr></thead>
<tbody>
{% for tax in doc.taxes %}
<tr>
<td>{{ tax.description or tax.account_head or "Tax" }}</td>
<td class="r">{{ tax.rate or "" }}</td>
<td class="r">{{ tax.get_formatted("tax_amount") if tax.get_formatted is defined else tax.tax_amount or "" }}</td>
</tr>
{% endfor %}
</tbody>
</table>
{% endif %}
{% if doc.advances %}
<table class="items" style="margin-top:10px">
<thead><tr><th>Advance</th><th class="r">Allocated</th></tr></thead>
<tbody>
{% for row in doc.advances %}
<tr>
<td>{{ row.employee_advance or row.advance or "" }}</td>
<td class="r">{{ row.get_formatted("allocated_amount") if row.get_formatted is defined else row.allocated_amount or "" }}</td>
</tr>
{% endfor %}
</tbody>
</table>
{% endif %}
"""


def _timesheet_table() -> str:
	return """
{% if doc.time_logs %}
<table class="items">
<thead><tr><th>#</th><th>Activity</th><th>From</th><th>To</th><th class="r">Hours</th><th class="r">Billing Amt</th></tr></thead>
<tbody>
{% for row in doc.time_logs %}
<tr>
<td>{{ loop.index }}</td>
<td>{{ row.activity_type or row.project or "" }}{% if row.task %}<br><small>{{ row.task }}</small>{% endif %}</td>
<td>{{ frappe.utils.format_datetime(row.from_time) if row.from_time else "" }}</td>
<td>{{ frappe.utils.format_datetime(row.to_time) if row.to_time else "" }}</td>
<td class="r">{{ row.hours or "" }}</td>
<td class="r">{{ row.get_formatted("billing_amount") if row.get_formatted is defined else row.billing_amount or "" }}</td>
</tr>
{% endfor %}
</tbody>
</table>
{% endif %}
"""


def _bom_items_table() -> str:
	return """
{% if doc.items %}
<table class="items">
<thead><tr><th>#</th><th>Item</th><th class="r">Qty</th><th>UOM</th><th class="r">Rate</th><th class="r">Amount</th><th>Source WH</th></tr></thead>
<tbody>
{% for row in doc.items %}
<tr>
<td>{{ loop.index }}</td>
<td><strong>{{ row.item_code or "" }}</strong>{% if row.item_name %}<br>{{ row.item_name }}{% endif %}</td>
<td class="r">{{ row.qty or "" }}</td>
<td>{{ row.uom or row.stock_uom or "" }}</td>
<td class="r">{{ row.rate or "" }}</td>
<td class="r">{{ row.amount or "" }}</td>
<td>{{ row.source_warehouse or "" }}</td>
</tr>
{% endfor %}
</tbody>
</table>
{% endif %}
"""


def _stockish_items_table() -> str:
	return """
{% if doc.items %}
<table class="items">
<thead>
<tr>
<th>#</th>
<th>Item</th>
<th>Warehouse</th>
<th class="r">Qty</th>
<th>UOM</th>
<th>Batch / Serial</th>
<th class="r">Rate</th>
<th class="r">Amount</th>
</tr>
</thead>
<tbody>
{% for row in doc.items %}
<tr>
<td>{{ loop.index }}</td>
<td><strong>{{ row.item_code or row.item_name or "" }}</strong>{% if row.item_name and row.item_name != row.item_code %}<br>{{ row.item_name }}{% endif %}{% if row.description and row.description != row.item_name %}<br><small>{{ row.description }}</small>{% endif %}</td>
<td>{{ row.warehouse or row.s_warehouse or row.t_warehouse or row.target_warehouse or "" }}</td>
<td class="r">{{ row.get_formatted("qty", doc) if row.get_formatted is defined else row.qty or row.required_qty or "" }}</td>
<td>{{ row.uom or row.stock_uom or "" }}</td>
<td>{% if row.batch_no %}{{ row.batch_no }}{% endif %}{% if row.serial_no %}<br><small>{{ row.serial_no }}</small>{% endif %}</td>
<td class="r">{{ row.get_formatted("rate", doc) if row.get_formatted is defined else row.rate or row.basic_rate or "" }}</td>
<td class="r">{{ row.get_formatted("amount", doc) if row.get_formatted is defined else row.amount or row.basic_amount or "" }}</td>
</tr>
{% endfor %}
</tbody>
</table>
{% endif %}
"""


def _commercial_items_table(include_tax: bool = False) -> str:
	tax_h = "<th class=\"r\">Tax</th>" if include_tax else ""
	tax_c = (
		'<td class="r">{{ row.item_tax_amount or row.gst_tax or "" }}</td>'
		if include_tax
		else ""
	)
	return f"""
{{% if doc.items %}}
<table class="items">
<thead>
<tr>
<th>#</th>
<th>Code</th>
<th>Description</th>
<th class="r">Qty</th>
<th>UOM</th>
<th class="r">Rate</th>
<th class="r">Disc%</th>
{tax_h}
<th class="r">Amount</th>
</tr>
</thead>
<tbody>
{{% for row in doc.items %}}
<tr>
<td>{{{{ loop.index }}}}</td>
<td>{{{{ row.item_code or "" }}}}</td>
<td><strong>{{{{ row.item_name or row.description or "" }}}}</strong>{{% if row.description and row.description != (row.item_name or row.item_code) %}}<br><small>{{{{ row.description }}}}</small>{{% endif %}}{{% if row.batch_no %}}<br><small>Batch: {{{{ row.batch_no }}}}</small>{{% endif %}}{{% if row.serial_no %}}<br><small>Serial: {{{{ row.serial_no }}}}</small>{{% endif %}}</td>
<td class="r">{{{{ row.get_formatted("qty", doc) if row.get_formatted is defined else row.qty or "" }}}}</td>
<td>{{{{ row.uom or row.stock_uom or "" }}}}</td>
<td class="r">{{{{ row.get_formatted("rate", doc) if row.get_formatted is defined else row.rate or "" }}}}</td>
<td class="r">{{{{ row.discount_percentage or 0 }}}}</td>
{tax_c}
<td class="r">{{{{ row.get_formatted("amount", doc) if row.get_formatted is defined else row.amount or "" }}}}</td>
</tr>
{{% endfor %}}
</tbody>
</table>
{{% endif %}}
{{% if doc.payment_schedule %}}
<table class="items" style="margin-top:10px">
<thead><tr><th>Payment Term</th><th>Due Date</th><th class="r">Amount</th></tr></thead>
<tbody>
{{% for row in doc.payment_schedule %}}
<tr>
<td>{{{{ row.payment_term or "" }}}}</td>
<td>{{{{ frappe.utils.formatdate(row.due_date) if row.due_date else "" }}}}</td>
<td class="r">{{{{ row.get_formatted("payment_amount") if row.get_formatted is defined else row.payment_amount or "" }}}}</td>
</tr>
{{% endfor %}}
</tbody>
</table>
{{% endif %}}
"""


def _item_master_detail_block() -> str:
	return """
{% if doc.image %}
<div style="margin-bottom:10px"><img src="{{ doc.image }}" style="max-height:100px;max-width:100px;border:1px solid #ddd;border-radius:6px"></div>
{% endif %}
<table class="items" style="margin-bottom:10px">
<thead><tr><th>Field</th><th>Value</th></tr></thead>
<tbody>
<tr><td>Item Code</td><td><strong>{{ doc.name }}</strong></td></tr>
<tr><td>Item Name</td><td>{{ doc.item_name or "" }}</td></tr>
<tr><td>Item Group</td><td>{{ doc.item_group or "" }}</td></tr>
<tr><td>Brand</td><td>{{ doc.brand or "—" }}</td></tr>
<tr><td>Stock UOM</td><td>{{ doc.stock_uom or "" }}{% if doc.sales_uom %} · Sales: {{ doc.sales_uom }}{% endif %}{% if doc.purchase_uom %} · Purchase: {{ doc.purchase_uom }}{% endif %}</td></tr>
<tr><td>Valuation Method</td><td>{{ doc.valuation_method or "—" }}</td></tr>
<tr><td>Valuation Rate</td><td class="r">{{ frappe.utils.fmt_money(doc.valuation_rate) if doc.valuation_rate else "—" }}</td></tr>
<tr><td>Standard Rate</td><td class="r">{{ frappe.utils.fmt_money(doc.standard_rate) if doc.standard_rate else "—" }}</td></tr>
<tr><td>Maintain Stock</td><td>{{ "Yes" if doc.is_stock_item else "No" }}</td></tr>
{% if doc.item_defaults %}
{% for d in doc.item_defaults %}
{% if d.default_warehouse %}<tr><td>Store / Warehouse</td><td>{{ d.default_warehouse }}{% if d.company %} ({{ d.company }}){% endif %}</td></tr>{% endif %}
{% endfor %}
{% endif %}
{% if doc.barcode %}<tr><td>Barcode</td><td>{{ doc.barcode }}</td></tr>{% endif %}
{% if doc.barcodes %}
{% for b in doc.barcodes %}
<tr><td>Barcode</td><td>{{ b.barcode or "" }}{% if b.barcode_type %} ({{ b.barcode_type }}){% endif %}</td></tr>
{% endfor %}
{% endif %}
{% if doc.gst_hsn_code %}<tr><td>HSN</td><td>{{ doc.gst_hsn_code }}</td></tr>{% endif %}
</tbody>
</table>
{% if doc.taxes %}
<table class="items" style="margin-top:8px">
<thead><tr><th>Tax Template / Type</th><th class="r">Rate</th></tr></thead>
<tbody>
{% for t in doc.taxes %}
<tr><td>{{ t.item_tax_template or t.tax_type or t.tax_category or "Tax" }}</td><td class="r">{{ t.tax_rate or "" }}</td></tr>
{% endfor %}
</tbody>
</table>
{% endif %}
{% if doc.uoms %}
<table class="items" style="margin-top:8px">
<thead><tr><th>UOM</th><th class="r">Conversion Factor</th></tr></thead>
<tbody>
{% for row in doc.uoms %}
<tr><td>{{ row.uom or "" }}</td><td class="r">{{ row.conversion_factor or "" }}</td></tr>
{% endfor %}
</tbody>
</table>
{% endif %}
{% set prices = frappe.get_all("Item Price", filters={"item_code": doc.name}, fields=["price_list", "price_list_rate", "currency", "uom", "valid_from"], order_by="price_list asc", limit_page_length=20) %}
{% if prices %}
<table class="items" style="margin-top:8px">
<thead><tr><th>Price List</th><th>UOM</th><th>Currency</th><th class="r">Rate</th></tr></thead>
<tbody>
{% for row in prices %}
<tr>
<td>{{ row.price_list or "" }}</td>
<td>{{ row.uom or doc.stock_uom or "" }}</td>
<td>{{ row.currency or "" }}</td>
<td class="r">{{ frappe.utils.fmt_money(row.price_list_rate, currency=row.currency) if row.price_list_rate else "" }}</td>
</tr>
{% endfor %}
</tbody>
</table>
{% endif %}
{% set purchases = frappe.db.sql("select pi.supplier_name, pi.supplier, pii.rate, pii.qty, pii.stock_uom, pi.posting_date from `tabPurchase Invoice Item` pii inner join `tabPurchase Invoice` pi on pi.name=pii.parent where pii.item_code=%s and pi.docstatus=1 order by pi.posting_date desc limit 2", doc.name, as_dict=1) %}
{% if purchases %}
<table class="items" style="margin-top:8px">
<thead><tr><th>Date</th><th>Supplier</th><th class="r">Qty</th><th class="r">Rate</th></tr></thead>
<tbody>
{% for row in purchases %}
<tr>
<td>{{ frappe.utils.formatdate(row.posting_date) if row.posting_date else "" }}</td>
<td>{{ row.supplier_name or row.supplier or "" }}</td>
<td class="r">{{ row.qty or "" }} {% if row.stock_uom %}{{ row.stock_uom }}{% endif %}</td>
<td class="r">{{ frappe.utils.fmt_money(row.rate) if row.rate else "" }}</td>
</tr>
{% endfor %}
</tbody>
</table>
{% endif %}
{% if doc.description %}
<div class="epp-remarks remarks" style="margin-top:10px;padding:8px;border:1px solid #ddd"><strong>Description</strong><br>{{ doc.description }}</div>
{% endif %}
"""
