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
	if profile.doc_type == "BOM":
		return """
{% set party_label = "Finished Good" %}
{% set ship_label = "" %}
{% set party_name = (doc.item_name or doc.item or "") ~ ((" · Qty " ~ doc.quantity ~ ((" " ~ doc.uom) if doc.uom else "")) if doc.quantity else "") %}
{% set party_address = doc.description or "" %}
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
<tr><td>Status</td><td class="r">{{ doc.status or "" }}</td></tr>
<tr><td>Item</td><td class="r">{{ doc.production_item or "" }}{% if doc.item_name %} · {{ doc.item_name }}{% endif %}</td></tr>
<tr><td>Qty To Manufacture</td><td class="r">{{ doc.qty or "" }} {{ doc.stock_uom or "" }}</td></tr>
<tr><td>Manufactured Qty</td><td class="r">{{ doc.produced_qty or 0 }}</td></tr>
{% if doc.bom_no %}<tr><td>BOM</td><td class="r">{{ doc.bom_no }}</td></tr>{% endif %}
{% if doc.production_plan %}<tr><td>Production Plan</td><td class="r">{{ doc.production_plan }}</td></tr>{% endif %}
{% if doc.sales_order %}<tr><td>Sales Order</td><td class="r">{{ doc.sales_order }}</td></tr>{% endif %}
{% if doc.wip_warehouse %}<tr><td>WIP Warehouse</td><td class="r">{{ doc.wip_warehouse }}</td></tr>{% endif %}
{% if doc.fg_warehouse %}<tr><td>Target Warehouse</td><td class="r">{{ doc.fg_warehouse }}</td></tr>{% endif %}
{% if doc.source_warehouse %}<tr><td>Source Warehouse</td><td class="r">{{ doc.source_warehouse }}</td></tr>{% endif %}
{% if doc.planned_start_date %}<tr><td>Planned Start</td><td class="r">{{ frappe.utils.format_datetime(doc.planned_start_date) }}</td></tr>{% endif %}
{% if doc.planned_end_date %}<tr><td>Planned End</td><td class="r">{{ frappe.utils.format_datetime(doc.planned_end_date) }}</td></tr>{% endif %}
{% if doc.actual_start_date %}<tr><td>Actual Start</td><td class="r">{{ frappe.utils.format_datetime(doc.actual_start_date) }}</td></tr>{% endif %}
{% if doc.actual_end_date %}<tr><td>Actual End</td><td class="r">{{ frappe.utils.format_datetime(doc.actual_end_date) }}</td></tr>{% endif %}
{% if doc.project %}<tr><td>Project</td><td class="r">{{ doc.project }}</td></tr>{% endif %}
</table>
"""
	if dt == "BOM":
		return """
<table class="meta">
<tr><td>BOM</td><td class="r bold">{{ doc.name }}</td></tr>
<tr><td>Finished Good</td><td class="r">{{ doc.item or "" }}</td></tr>
<tr><td>Item Name</td><td class="r">{{ doc.item_name or "" }}</td></tr>
<tr><td>Output Qty</td><td class="r">{{ doc.quantity or "" }} {{ doc.uom or "" }}</td></tr>
{% if doc.is_active %}<tr><td>Active</td><td class="r">Yes</td></tr>{% endif %}
{% if doc.is_default %}<tr><td>Default</td><td class="r">Yes</td></tr>{% endif %}
{% if doc.with_operations %}<tr><td>With Operations</td><td class="r">Yes</td></tr>{% endif %}
{% if doc.routing %}<tr><td>Routing</td><td class="r">{{ doc.routing }}</td></tr>{% endif %}
{% if doc.currency %}<tr><td>Currency</td><td class="r">{{ doc.currency }}</td></tr>{% endif %}
{% if doc.project %}<tr><td>Project</td><td class="r">{{ doc.project }}</td></tr>{% endif %}
</table>
"""
	if dt == "Production Plan":
		return """
<table class="meta">
<tr><td>Production Plan</td><td class="r bold">{{ doc.name }}</td></tr>
<tr><td>Date</td><td class="r">{{ frappe.utils.formatdate(doc.posting_date) if doc.posting_date else "" }}</td></tr>
<tr><td>Status</td><td class="r">{{ doc.status or "" }}</td></tr>
{% if doc.get_items_from %}<tr><td>Get Items From</td><td class="r">{{ doc.get_items_from }}</td></tr>{% endif %}
{% if doc.customer %}<tr><td>Customer</td><td class="r">{{ doc.customer }}</td></tr>{% endif %}
{% if doc.warehouse or doc.for_warehouse %}<tr><td>Warehouse</td><td class="r">{{ doc.for_warehouse or doc.warehouse or "" }}</td></tr>{% endif %}
{% if doc.from_date or doc.to_date %}<tr><td>Period</td><td class="r">{{ frappe.utils.formatdate(doc.from_date) if doc.from_date else "" }}{% if doc.to_date %} → {{ frappe.utils.formatdate(doc.to_date) }}{% endif %}</td></tr>{% endif %}
{% if doc.project %}<tr><td>Project</td><td class="r">{{ doc.project }}</td></tr>{% endif %}
<tr><td>Total Planned Qty</td><td class="r">{{ doc.total_planned_qty or 0 }}</td></tr>
<tr><td>Total Produced Qty</td><td class="r">{{ doc.total_produced_qty or 0 }}</td></tr>
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
	if dt == "Production Plan":
		return _production_plan_tables()
	if dt == "Job Card":
		return _job_card_tables()
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
	if dt == "Work Order":
		return """
<table class="totals">
<tr><td>Qty To Manufacture</td><td class="r">{{ doc.qty or 0 }}</td></tr>
<tr><td>Material Transferred</td><td class="r">{{ doc.material_transferred_for_manufacturing or 0 }}</td></tr>
<tr><td>Manufactured Qty</td><td class="r">{{ doc.produced_qty or 0 }}</td></tr>
{% if doc.process_loss_qty %}<tr><td>Process Loss Qty</td><td class="r">{{ doc.process_loss_qty }}</td></tr>{% endif %}
{% if doc.planned_operating_cost %}<tr><td>Planned Operating Cost</td><td class="r">{{ doc.get_formatted("planned_operating_cost") if doc.get_formatted is defined else doc.planned_operating_cost }}</td></tr>{% endif %}
{% if doc.actual_operating_cost %}<tr><td>Actual Operating Cost</td><td class="r">{{ doc.get_formatted("actual_operating_cost") if doc.get_formatted is defined else doc.actual_operating_cost }}</td></tr>{% endif %}
{% if doc.additional_operating_cost %}<tr><td>Additional Operating Cost</td><td class="r">{{ doc.get_formatted("additional_operating_cost") if doc.get_formatted is defined else doc.additional_operating_cost }}</td></tr>{% endif %}
{% if doc.total_operating_cost %}<tr class="grand"><td>Total Operating Cost</td><td class="r">{{ doc.get_formatted("total_operating_cost") if doc.get_formatted is defined else doc.total_operating_cost }}</td></tr>{% endif %}
</table>
"""
	if dt == "Production Plan":
		return """
<table class="totals">
<tr><td>Total Planned Qty</td><td class="r">{{ doc.total_planned_qty or 0 }}</td></tr>
<tr class="grand"><td>Total Produced Qty</td><td class="r">{{ doc.total_produced_qty or 0 }}</td></tr>
</table>
"""
	if dt == "BOM":
		return """
<table class="totals">
<tr><td>Raw Material Cost</td><td class="r">{{ doc.get_formatted("raw_material_cost") if doc.get_formatted is defined else doc.raw_material_cost or "" }}</td></tr>
<tr><td>Operating Cost</td><td class="r">{{ doc.get_formatted("operating_cost") if doc.get_formatted is defined else doc.operating_cost or "" }}</td></tr>
<tr class="grand"><td>Total Cost</td><td class="r">{{ doc.get_formatted("total_cost") if doc.get_formatted is defined else doc.total_cost or "" }}</td></tr>
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
{% if doc.description %}
<div style="margin-bottom:8px"><strong>Description</strong><br>{{ doc.description }}</div>
{% endif %}
{% if doc.required_items %}
<div style="margin:10px 0 4px;font-weight:700">Required Items</div>
<table class="items">
<thead>
<tr>
<th>#</th>
<th>Item</th>
<th>Source WH</th>
<th>Operation</th>
<th class="r">Required</th>
<th class="r">Transferred</th>
<th class="r">Consumed</th>
<th class="r">Available</th>
</tr>
</thead>
<tbody>
{% for row in doc.required_items %}
<tr>
<td>{{ loop.index }}</td>
<td><strong>{{ row.item_code or "" }}</strong>{% if row.item_name %}<br>{{ row.item_name }}{% endif %}{% if row.description and row.description != row.item_name %}<br><small>{{ row.description }}</small>{% endif %}</td>
<td>{{ row.source_warehouse or "" }}</td>
<td>{{ row.operation or "" }}</td>
<td class="r">{{ row.required_qty or "" }} {{ row.stock_uom or "" }}</td>
<td class="r">{{ row.transferred_qty or 0 }}</td>
<td class="r">{{ row.consumed_qty or 0 }}</td>
<td class="r">{{ row.available_qty_at_source_warehouse or row.available_qty_at_wip_warehouse or 0 }}</td>
</tr>
{% endfor %}
</tbody>
</table>
{% endif %}
{% if doc.operations %}
<div style="margin:14px 0 4px;font-weight:700">Operations</div>
<table class="items">
<thead>
<tr>
<th>#</th>
<th>Operation</th>
<th>Workstation</th>
<th>Status</th>
<th class="r">Completed</th>
<th class="r">Time (min)</th>
<th>Planned Start</th>
<th>Planned End</th>
<th class="r">Planned Cost</th>
<th class="r">Actual Cost</th>
</tr>
</thead>
<tbody>
{% for row in doc.operations %}
<tr>
<td>{{ loop.index }}</td>
<td><strong>{{ row.operation or "" }}</strong>{% if row.description %}<br><small>{{ row.description }}</small>{% endif %}{% if row.finished_good %}<br><small>FG: {{ row.finished_good }}</small>{% endif %}</td>
<td>{{ row.workstation or row.workstation_type or "" }}</td>
<td>{{ row.status or "" }}</td>
<td class="r">{{ row.completed_qty or 0 }}{% if row.pending_qty %} / pending {{ row.pending_qty }}{% endif %}</td>
<td class="r">{{ row.actual_operation_time or row.time_in_mins or "" }}</td>
<td>{{ frappe.utils.format_datetime(row.planned_start_time) if row.planned_start_time else "" }}</td>
<td>{{ frappe.utils.format_datetime(row.planned_end_time) if row.planned_end_time else "" }}</td>
<td class="r">{{ row.get_formatted("planned_operating_cost") if row.get_formatted is defined else row.planned_operating_cost or "" }}</td>
<td class="r">{{ row.get_formatted("actual_operating_cost") if row.get_formatted is defined else row.actual_operating_cost or "" }}</td>
</tr>
{% endfor %}
</tbody>
</table>
{% endif %}
{% set job_cards = frappe.get_all("Job Card", filters={"work_order": doc.name}, fields=["name", "operation", "workstation", "status", "for_quantity", "total_completed_qty", "total_time_in_mins", "posting_date", "employee"], order_by="creation asc", limit_page_length=100) %}
{% if job_cards %}
<div style="margin:14px 0 4px;font-weight:700">Linked Job Cards</div>
<table class="items">
<thead>
<tr>
<th>#</th>
<th>Job Card</th>
<th>Operation</th>
<th>Workstation</th>
<th>Status</th>
<th class="r">Qty</th>
<th class="r">Completed</th>
<th class="r">Time (min)</th>
<th>Date</th>
</tr>
</thead>
<tbody>
{% for row in job_cards %}
<tr>
<td>{{ loop.index }}</td>
<td><strong>{{ row.name }}</strong></td>
<td>{{ row.operation or "" }}</td>
<td>{{ row.workstation or "" }}</td>
<td>{{ row.status or "" }}</td>
<td class="r">{{ row.for_quantity or "" }}</td>
<td class="r">{{ row.total_completed_qty or 0 }}</td>
<td class="r">{{ row.total_time_in_mins or "" }}</td>
<td>{{ frappe.utils.formatdate(row.posting_date) if row.posting_date else "" }}</td>
</tr>
{% endfor %}
</tbody>
</table>
{% endif %}
{% if doc.non_stock_items %}
<div style="margin:14px 0 4px;font-weight:700">Additional Costs</div>
<table class="items">
<thead><tr><th>#</th><th>Item</th><th class="r">Qty</th><th class="r">Rate</th><th class="r">Amount</th></tr></thead>
<tbody>
{% for row in doc.non_stock_items %}
<tr>
<td>{{ loop.index }}</td>
<td>{{ row.item_code or row.item_name or "" }}</td>
<td class="r">{{ row.required_qty or row.qty or "" }}</td>
<td class="r">{{ row.rate or "" }}</td>
<td class="r">{{ row.amount or "" }}</td>
</tr>
{% endfor %}
</tbody>
</table>
{% endif %}
{% if doc.secondary_items %}
<div style="margin:14px 0 4px;font-weight:700">Secondary Items</div>
<table class="items">
<thead><tr><th>#</th><th>Item</th><th class="r">Qty</th><th>Warehouse</th></tr></thead>
<tbody>
{% for row in doc.secondary_items %}
<tr>
<td>{{ loop.index }}</td>
<td>{{ row.item_code or row.item_name or "" }}</td>
<td class="r">{{ row.required_qty or row.qty or "" }}</td>
<td>{{ row.source_warehouse or row.warehouse or "" }}</td>
</tr>
{% endfor %}
</tbody>
</table>
{% endif %}
"""


def _production_plan_tables() -> str:
	return """
{% if doc.sales_orders %}
<div style="margin:10px 0 4px;font-weight:700">Sales Orders</div>
<table class="items">
<thead><tr><th>#</th><th>Sales Order</th><th>Date</th><th>Customer</th><th>Status</th><th class="r">Grand Total</th></tr></thead>
<tbody>
{% for row in doc.sales_orders %}
<tr>
<td>{{ loop.index }}</td>
<td><strong>{{ row.sales_order or "" }}</strong></td>
<td>{{ frappe.utils.formatdate(row.sales_order_date) if row.sales_order_date else "" }}</td>
<td>{{ row.customer or "" }}</td>
<td>{{ row.status or "" }}</td>
<td class="r">{{ row.get_formatted("grand_total") if row.get_formatted is defined else row.grand_total or "" }}</td>
</tr>
{% endfor %}
</tbody>
</table>
{% endif %}
{% if doc.material_requests %}
<div style="margin:14px 0 4px;font-weight:700">Material Requests</div>
<table class="items">
<thead><tr><th>#</th><th>Material Request</th><th>Date</th></tr></thead>
<tbody>
{% for row in doc.material_requests %}
<tr>
<td>{{ loop.index }}</td>
<td><strong>{{ row.material_request or "" }}</strong></td>
<td>{{ frappe.utils.formatdate(row.material_request_date) if row.material_request_date else "" }}</td>
</tr>
{% endfor %}
</tbody>
</table>
{% endif %}
{% if doc.po_items %}
<div style="margin:14px 0 4px;font-weight:700">Assembly / Production Items</div>
<table class="items">
<thead>
<tr>
<th>#</th>
<th>Item</th>
<th>BOM</th>
<th>Warehouse</th>
<th class="r">Planned Qty</th>
<th class="r">Pending</th>
<th class="r">Ordered</th>
<th class="r">Produced</th>
<th>Sales Order / MR</th>
<th>Start Date</th>
</tr>
</thead>
<tbody>
{% for row in doc.po_items %}
<tr>
<td>{{ loop.index }}</td>
<td><strong>{{ row.item_code or "" }}</strong>{% if row.description %}<br><small>{{ row.description }}</small>{% endif %}</td>
<td>{{ row.bom_no or "" }}</td>
<td>{{ row.warehouse or "" }}</td>
<td class="r">{{ row.planned_qty or "" }} {{ row.stock_uom or "" }}</td>
<td class="r">{{ row.pending_qty or 0 }}</td>
<td class="r">{{ row.ordered_qty or 0 }}</td>
<td class="r">{{ row.produced_qty or 0 }}</td>
<td>{% if row.sales_order %}SO: {{ row.sales_order }}{% endif %}{% if row.material_request %}<br>MR: {{ row.material_request }}{% endif %}</td>
<td>{{ frappe.utils.format_datetime(row.planned_start_date) if row.planned_start_date else "" }}</td>
</tr>
{% endfor %}
</tbody>
</table>
{% endif %}
{% if doc.sub_assembly_items %}
<div style="margin:14px 0 4px;font-weight:700">Sub Assembly Items</div>
<table class="items">
<thead>
<tr>
<th>#</th>
<th>Item</th>
<th>BOM</th>
<th>Type</th>
<th>Warehouse</th>
<th class="r">Qty</th>
<th class="r">Required</th>
<th class="r">Ordered</th>
<th class="r">Produced</th>
<th>Supplier / SO</th>
</tr>
</thead>
<tbody>
{% for row in doc.sub_assembly_items %}
<tr>
<td>{{ loop.index }}</td>
<td><strong>{{ row.production_item or row.item_name or "" }}</strong>{% if row.parent_item_code %}<br><small>Parent: {{ row.parent_item_code }}</small>{% endif %}</td>
<td>{{ row.bom_no or "" }}</td>
<td>{{ row.type_of_manufacturing or "" }}</td>
<td>{{ row.fg_warehouse or "" }}</td>
<td class="r">{{ row.qty or "" }} {{ row.uom or row.stock_uom or "" }}</td>
<td class="r">{{ row.required_qty or 0 }}</td>
<td class="r">{{ row.ordered_qty or 0 }}</td>
<td class="r">{{ row.wo_produced_qty or 0 }}</td>
<td>{% if row.supplier %}{{ row.supplier }}{% endif %}{% if row.sales_order %}<br>SO: {{ row.sales_order }}{% endif %}{% if row.purchase_order %}<br>PO: {{ row.purchase_order }}{% endif %}</td>
</tr>
{% endfor %}
</tbody>
</table>
{% endif %}
{% if doc.mr_items %}
<div style="margin:14px 0 4px;font-weight:700">Raw Materials</div>
<table class="items">
<thead>
<tr>
<th>#</th>
<th>Item</th>
<th>Warehouse</th>
<th>MR Type</th>
<th class="r">Required Qty</th>
<th class="r">Projected</th>
<th class="r">Actual</th>
<th class="r">Requested</th>
<th class="r">Ordered</th>
<th>Sales Order</th>
<th>Schedule</th>
</tr>
</thead>
<tbody>
{% for row in doc.mr_items %}
<tr>
<td>{{ loop.index }}</td>
<td><strong>{{ row.item_code or "" }}</strong>{% if row.item_name %}<br>{{ row.item_name }}{% endif %}{% if row.main_item_code %}<br><small>For: {{ row.main_item_code }}</small>{% endif %}</td>
<td>{{ row.warehouse or row.from_warehouse or "" }}</td>
<td>{{ row.material_request_type or "" }}</td>
<td class="r">{{ row.quantity or row.required_bom_qty or "" }} {{ row.uom or "" }}</td>
<td class="r">{{ row.projected_qty or 0 }}</td>
<td class="r">{{ row.actual_qty or 0 }}</td>
<td class="r">{{ row.requested_qty or 0 }}</td>
<td class="r">{{ row.ordered_qty or 0 }}</td>
<td>{{ row.sales_order or "" }}</td>
<td>{{ frappe.utils.formatdate(row.schedule_date) if row.schedule_date else "" }}</td>
</tr>
{% endfor %}
</tbody>
</table>
{% endif %}
{% set work_orders = frappe.get_all("Work Order", filters={"production_plan": doc.name}, fields=["name", "production_item", "item_name", "qty", "produced_qty", "status", "bom_no", "planned_start_date"], order_by="creation asc", limit_page_length=100) %}
{% if work_orders %}
<div style="margin:14px 0 4px;font-weight:700">Linked Work Orders</div>
<table class="items">
<thead>
<tr>
<th>#</th>
<th>Work Order</th>
<th>Item</th>
<th>BOM</th>
<th class="r">Qty</th>
<th class="r">Produced</th>
<th>Status</th>
<th>Planned Start</th>
</tr>
</thead>
<tbody>
{% for row in work_orders %}
<tr>
<td>{{ loop.index }}</td>
<td><strong>{{ row.name }}</strong></td>
<td>{{ row.production_item or "" }}{% if row.item_name %}<br><small>{{ row.item_name }}</small>{% endif %}</td>
<td>{{ row.bom_no or "" }}</td>
<td class="r">{{ row.qty or "" }}</td>
<td class="r">{{ row.produced_qty or 0 }}</td>
<td>{{ row.status or "" }}</td>
<td>{{ frappe.utils.format_datetime(row.planned_start_date) if row.planned_start_date else "" }}</td>
</tr>
{% endfor %}
</tbody>
</table>
{% endif %}
"""


def _job_card_tables() -> str:
	return """
<table class="items" style="margin-bottom:10px">
<thead><tr><th>Field</th><th>Value</th></tr></thead>
<tbody>
<tr><td>Work Order</td><td><strong>{{ doc.work_order or "" }}</strong></td></tr>
<tr><td>Operation</td><td>{{ doc.operation or "" }}</td></tr>
<tr><td>Workstation</td><td>{{ doc.workstation or doc.workstation_type or "" }}</td></tr>
<tr><td>Item</td><td>{{ doc.production_item or doc.finished_good or "" }}{% if doc.item_name %} · {{ doc.item_name }}{% endif %}</td></tr>
<tr><td>Qty To Manufacture</td><td>{{ doc.for_quantity or "" }}</td></tr>
<tr><td>Completed Qty</td><td>{{ doc.total_completed_qty or 0 }}</td></tr>
<tr><td>Status</td><td>{{ doc.status or "" }}</td></tr>
{% if doc.bom_no %}<tr><td>BOM</td><td>{{ doc.bom_no }}</td></tr>{% endif %}
{% if doc.wip_warehouse %}<tr><td>WIP Warehouse</td><td>{{ doc.wip_warehouse }}</td></tr>{% endif %}
{% if doc.total_time_in_mins %}<tr><td>Total Time (min)</td><td>{{ doc.total_time_in_mins }}</td></tr>{% endif %}
</tbody>
</table>
{% if doc.time_logs %}
<div style="margin:10px 0 4px;font-weight:700">Time Logs</div>
<table class="items">
<thead><tr><th>#</th><th>Employee</th><th>From</th><th>To</th><th class="r">Completed Qty</th><th class="r">Time (min)</th></tr></thead>
<tbody>
{% for row in doc.time_logs %}
<tr>
<td>{{ loop.index }}</td>
<td>{{ row.employee or row.employee_name or "" }}</td>
<td>{{ frappe.utils.format_datetime(row.from_time) if row.from_time else "" }}</td>
<td>{{ frappe.utils.format_datetime(row.to_time) if row.to_time else "" }}</td>
<td class="r">{{ row.completed_qty or "" }}</td>
<td class="r">{{ row.time_in_mins or "" }}</td>
</tr>
{% endfor %}
</tbody>
</table>
{% endif %}
{% if doc.items %}
<div style="margin:14px 0 4px;font-weight:700">Items</div>
<table class="items">
<thead><tr><th>#</th><th>Item</th><th>Source WH</th><th class="r">Required</th><th class="r">Transferred</th></tr></thead>
<tbody>
{% for row in doc.items %}
<tr>
<td>{{ loop.index }}</td>
<td>{{ row.item_code or "" }}{% if row.item_name %}<br>{{ row.item_name }}{% endif %}</td>
<td>{{ row.source_warehouse or "" }}</td>
<td class="r">{{ row.required_qty or "" }}</td>
<td class="r">{{ row.transferred_qty or 0 }}</td>
</tr>
{% endfor %}
</tbody>
</table>
{% endif %}
{% if doc.sub_operations %}
<div style="margin:14px 0 4px;font-weight:700">Sub Operations</div>
<table class="items">
<thead><tr><th>#</th><th>Operation</th><th>Status</th><th class="r">Completed</th></tr></thead>
<tbody>
{% for row in doc.sub_operations %}
<tr>
<td>{{ loop.index }}</td>
<td>{{ row.operation or "" }}</td>
<td>{{ row.status or "" }}</td>
<td class="r">{{ row.completed_qty or 0 }}</td>
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
<table class="items" style="margin-bottom:10px">
<thead><tr><th>Field</th><th>Value</th></tr></thead>
<tbody>
<tr><td>Finished Good</td><td><strong>{{ doc.item or "" }}</strong>{% if doc.item_name %} · {{ doc.item_name }}{% endif %}</td></tr>
<tr><td>Output Qty</td><td>{{ doc.quantity or "" }} {{ doc.uom or "" }}</td></tr>
{% if doc.description %}<tr><td>Description</td><td>{{ doc.description }}</td></tr>{% endif %}
{% if doc.routing %}<tr><td>Routing</td><td>{{ doc.routing }}</td></tr>{% endif %}
{% if doc.default_source_warehouse %}<tr><td>Default Source WH</td><td>{{ doc.default_source_warehouse }}</td></tr>{% endif %}
{% if doc.default_target_warehouse %}<tr><td>Default Target WH</td><td>{{ doc.default_target_warehouse }}</td></tr>{% endif %}
<tr><td>Flags</td><td>{% if doc.is_active %}Active {% endif %}{% if doc.is_default %}Default {% endif %}{% if doc.with_operations %}With Operations{% endif %}</td></tr>
</tbody>
</table>
{% if doc.items %}
<div style="margin:12px 0 4px;font-weight:700">Raw Materials / Components</div>
<table class="items">
<thead>
<tr>
<th style="width:4%">#</th>
<th style="width:28%">Item</th>
<th style="width:12%">Operation</th>
<th style="width:14%">Source WH</th>
<th style="width:10%" class="r">Qty</th>
<th style="width:8%">UOM</th>
<th style="width:12%" class="r">Rate</th>
<th style="width:12%" class="r">Amount</th>
</tr>
</thead>
<tbody>
{% for row in doc.items %}
<tr>
<td>{{ loop.index }}</td>
<td><strong>{{ row.item_code or "" }}</strong>{% if row.item_name %}<br>{{ row.item_name }}{% endif %}{% if row.bom_no %}<br><small>BOM: {{ row.bom_no }}</small>{% endif %}</td>
<td>{{ row.operation or "" }}</td>
<td>{{ row.source_warehouse or "" }}</td>
<td class="r">{{ row.qty or "" }}</td>
<td>{{ row.uom or row.stock_uom or "" }}</td>
<td class="r">{{ row.get_formatted("rate") if row.get_formatted is defined else row.rate or "" }}</td>
<td class="r">{{ row.get_formatted("amount") if row.get_formatted is defined else row.amount or "" }}</td>
</tr>
{% endfor %}
</tbody>
</table>
{% endif %}
{% if doc.operations %}
<div style="margin:14px 0 4px;font-weight:700">Operations</div>
<table class="items">
<thead>
<tr>
<th style="width:4%">#</th>
<th style="width:22%">Operation</th>
<th style="width:16%">Workstation</th>
<th style="width:12%" class="r">Time (min)</th>
<th style="width:12%" class="r">Hour Rate</th>
<th style="width:14%" class="r">Operating Cost</th>
<th style="width:20%">FG / Notes</th>
</tr>
</thead>
<tbody>
{% for row in doc.operations %}
<tr>
<td>{{ loop.index }}</td>
<td><strong>{{ row.operation or "" }}</strong>{% if row.description %}<br><small>{{ row.description }}</small>{% endif %}</td>
<td>{{ row.workstation or row.workstation_type or "" }}</td>
<td class="r">{{ row.time_in_mins or "" }}</td>
<td class="r">{{ row.get_formatted("hour_rate") if row.get_formatted is defined else row.hour_rate or "" }}</td>
<td class="r">{{ row.get_formatted("operating_cost") if row.get_formatted is defined else row.operating_cost or "" }}</td>
<td>{% if row.finished_good %}{{ row.finished_good }}{% if row.finished_good_qty %} × {{ row.finished_good_qty }}{% endif %}{% endif %}</td>
</tr>
{% endfor %}
</tbody>
</table>
{% endif %}
{% if doc.exploded_items %}
<div style="margin:14px 0 4px;font-weight:700">Exploded Items</div>
<table class="items">
<thead>
<tr>
<th style="width:5%">#</th>
<th style="width:35%">Item</th>
<th style="width:15%" class="r">Qty</th>
<th style="width:10%">UOM</th>
<th style="width:17%" class="r">Rate</th>
<th style="width:18%" class="r">Amount</th>
</tr>
</thead>
<tbody>
{% for row in doc.exploded_items %}
<tr>
<td>{{ loop.index }}</td>
<td><strong>{{ row.item_code or "" }}</strong>{% if row.item_name %}<br>{{ row.item_name }}{% endif %}</td>
<td class="r">{{ row.qty or row.stock_qty or "" }}</td>
<td>{{ row.stock_uom or row.uom or "" }}</td>
<td class="r">{{ row.rate or "" }}</td>
<td class="r">{{ row.amount or "" }}</td>
</tr>
{% endfor %}
</tbody>
</table>
{% endif %}
{% if doc.secondary_items %}
<div style="margin:14px 0 4px;font-weight:700">Secondary Items</div>
<table class="items">
<thead><tr><th>#</th><th>Item</th><th class="r">Qty</th><th>UOM</th><th class="r">Rate</th><th class="r">Amount</th></tr></thead>
<tbody>
{% for row in doc.secondary_items %}
<tr>
<td>{{ loop.index }}</td>
<td>{{ row.item_code or row.item_name or "" }}</td>
<td class="r">{{ row.qty or "" }}</td>
<td>{{ row.uom or "" }}</td>
<td class="r">{{ row.rate or "" }}</td>
<td class="r">{{ row.amount or "" }}</td>
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
	# Keep column count A4-safe: merge code into description; optional tax as small note.
	tax_note = (
		'{% if row.item_tax_amount or row.gst_tax %}<br><small>Tax: {{ row.item_tax_amount or row.gst_tax }}</small>{% endif %}'
		if include_tax
		else ""
	)
	return f"""
{{% if doc.items %}}
<table class="items">
<thead>
<tr>
<th style="width:5%">#</th>
<th style="width:42%">Item</th>
<th style="width:10%" class="r">Qty</th>
<th style="width:8%">UOM</th>
<th style="width:14%" class="r">Rate</th>
<th style="width:8%" class="r">Disc%</th>
<th style="width:13%" class="r">Amount</th>
</tr>
</thead>
<tbody>
{{% for row in doc.items %}}
<tr>
<td>{{{{ loop.index }}}}</td>
<td><strong>{{{{ row.item_code or "" }}}}</strong>{{% if row.item_name %}}<br>{{{{ row.item_name }}}}{{% endif %}}{{% if row.description and row.description != (row.item_name or row.item_code) %}}<br><small>{{{{ row.description }}}}</small>{{% endif %}}{{% if row.batch_no %}}<br><small>Batch: {{{{ row.batch_no }}}}</small>{{% endif %}}{{% if row.serial_no %}}<br><small>Serial: {{{{ row.serial_no }}}}</small>{{% endif %}}{tax_note}</td>
<td class="r">{{{{ row.get_formatted("qty", doc) if row.get_formatted is defined else row.qty or "" }}}}</td>
<td>{{{{ row.uom or row.stock_uom or "" }}}}</td>
<td class="r">{{{{ row.get_formatted("rate", doc) if row.get_formatted is defined else row.rate or "" }}}}</td>
<td class="r">{{{{ row.discount_percentage or 0 }}}}</td>
<td class="r">{{{{ row.get_formatted("amount", doc) if row.get_formatted is defined else row.amount or "" }}}}</td>
</tr>
{{% endfor %}}
</tbody>
</table>
{{% endif %}}
{{% if doc.payment_schedule %}}
<table class="items" style="margin-top:10px">
<thead><tr><th style="width:40%">Payment Term</th><th style="width:30%">Due Date</th><th style="width:30%" class="r">Amount</th></tr></thead>
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
