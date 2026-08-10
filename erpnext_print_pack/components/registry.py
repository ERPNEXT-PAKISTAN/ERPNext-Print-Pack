"""Reusable print component registry."""

from __future__ import annotations

from pathlib import Path

COMPONENTS_DIR = Path(__file__).resolve().parent

COMPONENT_REGISTRY = {
	"header_basic": "headers/basic.html",
	"header_logo_left": "headers/logo_left.html",
	"header_logo_center": "headers/logo_center.html",
	"header_company_details": "headers/company_details.html",
	"header_compact": "headers/compact.html",
	"header_bilingual": "headers/bilingual.html",
	"header_tax_registration": "headers/tax_registration.html",
	"header_document_number": "headers/document_number.html",
	"header_landscape": "headers/landscape.html",
	"header_thermal": "headers/thermal.html",
	"party_bill_to": "party_blocks/bill_to.html",
	"party_ship_to": "party_blocks/ship_to.html",
	"party_supplier": "party_blocks/supplier.html",
	"party_customer_shipping": "party_blocks/customer_shipping.html",
	"party_contact": "party_blocks/contact.html",
	"party_tax_id": "party_blocks/tax_id.html",
	"party_billing_delivery": "party_blocks/billing_delivery.html",
	"party_bilingual": "party_blocks/bilingual.html",
	"items_basic": "item_tables/basic.html",
	"items_compact": "item_tables/compact.html",
	"items_tax_inclusive": "item_tables/tax_inclusive.html",
	"items_discount": "item_tables/discount.html",
	"items_batch_serial": "item_tables/batch_serial.html",
	"items_warehouse": "item_tables/warehouse.html",
	"items_stock_entry": "item_tables/stock_entry.html",
	"items_journal_accounts": "item_tables/journal_accounts.html",
	"items_payment_details": "item_tables/payment_details.html",
	"items_expense_claim": "item_tables/expense_claim.html",
	"items_work_order": "item_tables/work_order.html",
	"items_production_plan": "item_tables/production_plan.html",
	"items_job_card": "item_tables/job_card.html",
	"items_manufacturing": "item_tables/manufacturing.html",
	"items_delivery": "item_tables/delivery.html",
	"items_thermal": "item_tables/thermal.html",
	"items_landscape": "item_tables/landscape.html",
	"totals_basic": "totals/basic.html",
	"totals_tax_breakdown": "totals/tax_breakdown.html",
	"totals_multi_currency": "totals/multi_currency.html",
	"totals_discount": "totals/discount.html",
	"totals_rounded": "totals/rounded.html",
	"totals_outstanding": "totals/outstanding.html",
	"totals_advance_paid": "totals/advance_paid.html",
	"totals_payment_schedule": "totals/payment_schedule.html",
	"totals_amount_in_words": "totals/amount_in_words.html",
	"totals_bilingual": "totals/bilingual.html",
	"totals_journal": "totals/journal.html",
	"totals_payment": "totals/payment.html",
	"totals_stock_entry": "totals/stock_entry.html",
	"totals_expense_claim": "totals/expense_claim.html",
	"totals_work_order": "totals/work_order.html",
	"totals_production_plan": "totals/production_plan.html",
	"qr_block": "qr_blocks/basic.html",
	"qr_zatca_placeholder": "qr_blocks/zatca_placeholder.html",
	"barcode_block": "barcode_blocks/basic.html",
	"signature_single": "signatures/single.html",
	"signature_multi": "signatures/multi.html",
	"terms_block": "terms/basic.html",
	"bank_details": "payment_blocks/bank_details.html",
	"payment_instructions": "payment_blocks/payment_instructions.html",
	"footer_basic": "footers/basic.html",
	"page_number": "footers/page_number.html",
	"prepared_checked_approved": "signatures/prepared_checked_approved.html",
	"delivery_acknowledgement": "signatures/delivery_acknowledgement.html",
	"receiver_signature": "signatures/receiver_signature.html",
	"vehicle_details": "party_blocks/vehicle_details.html",
	"shipping_details": "party_blocks/shipping_details.html",
	"tax_summary": "tax_summaries/basic.html",
	"tax_summary_detailed": "tax_summaries/detailed.html",
	"notes_block": "terms/notes.html",
	"attachments_list": "terms/attachments_list.html",
	"serial_number_list": "item_tables/serial_list.html",
	"batch_details": "item_tables/batch_details.html",
	"warranty_info": "terms/warranty.html",
}


def load_component(name: str) -> str:
	rel = COMPONENT_REGISTRY.get(name)
	if not rel:
		return ""
	path = COMPONENTS_DIR / rel
	if path.exists():
		return path.read_text(encoding="utf-8")
	return ""
