"""DocType field profiles for print format generation."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class DocTypeProfile:
	slug: str
	doc_type: str
	category: str
	title: str
	has_items: bool = False
	has_taxes: bool = False
	has_party_customer: bool = False
	has_party_supplier: bool = False
	has_due_date: bool = False
	has_in_words: bool = False
	has_terms: bool = False
	date_field: str = "posting_date"
	party_field: str | None = None
	party_name_field: str | None = None
	supported_themes: list[str] = field(default_factory=list)
	orientation_default: str = "portrait"
	paper_default: str = "A4"


PROFILES: dict[str, DocTypeProfile] = {}


def _register(profile: DocTypeProfile):
	PROFILES[profile.slug] = profile


THEMES_SALES = [
	"minimal", "modern", "corporate", "executive", "material", "elegant", "compact",
	"clean", "technical", "professional_blue", "professional_green", "monochrome",
	"soft_gray", "premium", "landscape", "thermal", "bilingual", "tax_focused",
	"qr_enabled", "barcode_enabled", "industrial", "retail", "wholesale", "manufacturing",
]
THEMES_STANDARD = [
	"minimal", "modern", "corporate", "compact", "clean", "technical",
	"professional_blue", "monochrome", "soft_gray", "premium", "landscape", "thermal",
]
THEMES_PURCHASE = THEMES_STANDARD + ["executive", "elegant", "tax_focused"]
THEMES_STOCK = ["minimal", "modern", "compact", "technical", "industrial", "manufacturing", "thermal", "landscape"]
THEMES_HR = ["minimal", "modern", "corporate", "compact", "clean", "professional_blue"]
THEMES_LABEL = ["minimal", "thermal", "compact", "barcode_enabled", "qr_enabled"]

_register(DocTypeProfile("sales_invoice", "Sales Invoice", "sales", "Sales Invoice", True, True, True, False, True, True, True, "posting_date", "customer", "customer_name", THEMES_SALES))
_register(DocTypeProfile("delivery_note", "Delivery Note", "sales", "Delivery Note", True, False, True, False, False, False, True, "posting_date", "customer", "customer_name", THEMES_STANDARD + ["retail", "manufacturing"]))
_register(DocTypeProfile("quotation", "Quotation", "sales", "Quotation", True, True, True, False, True, False, True, "transaction_date", "party_name", "party_name", THEMES_STANDARD + ["elegant", "premium"]))
_register(DocTypeProfile("sales_order", "Sales Order", "sales", "Sales Order", True, True, True, False, True, False, True, "transaction_date", "customer", "customer_name", THEMES_STANDARD + ["executive"]))
_register(DocTypeProfile("pick_list", "Pick List", "sales", "Pick List", True, False, True, False, False, False, False, "posting_date", "customer", "customer_name", THEMES_STOCK[:8]))
_register(DocTypeProfile("pos_invoice", "POS Invoice", "sales", "POS Invoice", True, True, True, False, False, False, False, "posting_date", "customer", "customer_name", ["thermal", "compact", "minimal", "modern", "retail", "barcode_enabled", "qr_enabled"]))
_register(DocTypeProfile("purchase_order", "Purchase Order", "purchasing", "Purchase Order", True, True, False, True, True, False, True, "transaction_date", "supplier", "supplier_name", THEMES_PURCHASE))
_register(DocTypeProfile("purchase_receipt", "Purchase Receipt", "purchasing", "Purchase Receipt", True, False, False, True, False, False, True, "posting_date", "supplier", "supplier_name", THEMES_PURCHASE[:12]))
_register(DocTypeProfile("purchase_invoice", "Purchase Invoice", "purchasing", "Purchase Invoice", True, True, False, True, True, True, True, "posting_date", "supplier", "supplier_name", THEMES_PURCHASE))
_register(DocTypeProfile("request_for_quotation", "Request for Quotation", "purchasing", "Request for Quotation", True, False, False, True, False, False, True, "transaction_date", "supplier", "supplier", THEMES_STANDARD[:10]))
_register(DocTypeProfile("supplier_quotation", "Supplier Quotation", "purchasing", "Supplier Quotation", True, True, False, True, True, False, True, "transaction_date", "supplier", "supplier_name", THEMES_STANDARD[:10]))
_register(DocTypeProfile("payment_entry", "Payment Entry", "payments", "Payment Entry", False, False, False, False, False, True, False, "posting_date", "party", "party_name", THEMES_STANDARD + ["executive", "elegant", "tax_focused"]))
_register(DocTypeProfile("journal_entry", "Journal Entry", "payments", "Journal Entry", False, False, False, False, False, True, False, "posting_date", None, None, THEMES_STANDARD + ["executive", "landscape"]))
_register(DocTypeProfile("payment_request", "Payment Request", "payments", "Payment Request", False, False, True, False, True, False, True, "transaction_date", "party", "party_name", THEMES_STANDARD[:8]))
_register(DocTypeProfile("dunning", "Dunning", "payments", "Dunning", False, False, True, False, True, False, True, "posting_date", "customer", "customer_name", ["minimal", "modern", "corporate", "professional_blue"]))
_register(DocTypeProfile("stock_entry", "Stock Entry", "stock", "Stock Entry", True, False, False, False, False, False, False, "posting_date", "supplier", "supplier_name", THEMES_STOCK + ["barcode_enabled", "qr_enabled"]))
_register(DocTypeProfile("material_request", "Material Request", "stock", "Material Request", True, False, False, False, False, False, False, "transaction_date", None, None, THEMES_STOCK[:8]))
_register(DocTypeProfile("delivery_trip", "Delivery Trip", "stock", "Delivery Trip", False, False, True, False, False, False, False, "departure_time", "driver", "driver_name", ["minimal", "modern", "compact", "landscape"]))
_register(DocTypeProfile("shipment", "Shipment", "stock", "Shipment", True, False, True, False, False, False, False, "pickup_date", "delivery_customer", "delivery_customer_name", THEMES_STOCK[:6]))
_register(DocTypeProfile("work_order", "Work Order", "manufacturing", "Work Order", False, False, False, False, False, False, False, "planned_start_date", None, None, THEMES_STOCK + ["manufacturing"]))
_register(DocTypeProfile("job_card", "Job Card", "manufacturing", "Job Card", False, False, False, False, False, False, False, "posting_date", None, None, THEMES_STOCK[:8]))
_register(DocTypeProfile("production_plan", "Production Plan", "manufacturing", "Production Plan", True, False, False, False, False, False, False, "posting_date", None, None, ["minimal", "modern", "manufacturing", "industrial"]))
_register(DocTypeProfile("bom", "BOM", "manufacturing", "Bill of Materials", True, False, False, False, False, False, False, "creation", "item", "item", ["minimal", "modern", "technical", "manufacturing"]))
_register(DocTypeProfile("subcontracting_order", "Subcontracting Order", "manufacturing", "Subcontracting Order", True, False, False, True, False, False, False, "transaction_date", "supplier", "supplier_name", THEMES_STANDARD[:8]))
_register(DocTypeProfile("subcontracting_receipt", "Subcontracting Receipt", "manufacturing", "Subcontracting Receipt", True, False, False, True, False, False, False, "posting_date", "supplier", "supplier_name", THEMES_STANDARD[:8]))
_register(DocTypeProfile("timesheet", "Timesheet", "projects", "Timesheet", True, False, True, False, False, False, False, "start_date", "customer", "customer_name", THEMES_HR[:8]))
_register(DocTypeProfile("project", "Project", "projects", "Project", False, False, True, False, False, False, False, "expected_start_date", "customer", "customer", THEMES_HR[:6]))
_register(DocTypeProfile("maintenance_visit", "Maintenance Visit", "projects", "Maintenance Visit", False, False, True, False, False, False, True, "mntc_date", "customer", "customer_name", THEMES_HR[:6]))
_register(DocTypeProfile("maintenance_schedule", "Maintenance Schedule", "projects", "Maintenance Schedule", False, False, True, False, False, False, False, "scheduled_date", "customer", "customer", ["minimal", "modern", "compact"]))
_register(DocTypeProfile("installation_note", "Installation Note", "projects", "Installation Note", True, False, True, False, False, False, True, "installation_date", "customer", "customer_name", THEMES_STANDARD[:8]))
_register(DocTypeProfile("issue", "Issue", "projects", "Issue", False, False, True, False, False, False, False, "opening_date", "customer", "customer", THEMES_HR[:6]))
_register(DocTypeProfile("salary_slip", "Salary Slip", "hr", "Salary Slip", True, False, False, False, False, False, False, "start_date", "employee", "employee_name", THEMES_HR))
_register(DocTypeProfile("expense_claim", "Expense Claim", "hr", "Expense Claim", True, False, False, False, False, False, False, "posting_date", "employee", "employee_name", THEMES_HR))
_register(DocTypeProfile("employee_advance", "Employee Advance", "hr", "Employee Advance", False, False, False, False, False, False, False, "posting_date", "employee", "employee_name", THEMES_HR[:6]))
_register(DocTypeProfile("leave_application", "Leave Application", "hr", "Leave Application", False, False, False, False, False, False, False, "from_date", "employee", "employee_name", THEMES_HR[:6]))
_register(DocTypeProfile("job_offer", "Job Offer", "hr", "Job Offer", False, False, False, False, False, False, True, "offer_date", "applicant_name", "applicant_name", THEMES_HR[:6]))
_register(DocTypeProfile("item_label", "Item", "stock", "Item Label", False, False, False, False, False, False, False, "creation", "name", "item_name", THEMES_LABEL))
_register(DocTypeProfile("item_detail", "Item", "stock", "Item Detail Report", False, False, False, False, False, False, False, "creation", "name", "item_name", THEMES_STANDARD[:8]))
_register(DocTypeProfile("batch_label", "Batch", "stock", "Batch Label", False, False, False, False, False, False, False, "creation", "item", "item", THEMES_LABEL))
_register(DocTypeProfile("serial_label", "Serial No", "stock", "Serial Label", False, False, False, False, False, False, False, "creation", "item_code", "item_name", THEMES_LABEL))

DEFERRED_DOCTYPES = [
	"Packing Slip",
	"Customer Statement",
	"General Ledger",
	"Account Statement",
	"Gate Pass",
	"Goods Receipt Note",
	"Warranty Claim",
	"Interview",
	"Appointment Letter",
	"Attendance",
	"Sales Taxes and Charges Template",
]
