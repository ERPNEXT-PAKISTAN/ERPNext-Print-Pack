"""Sales Invoice / Address custom fields for bilingual & KSA ZATCA print formats.

These fields are for print templates only (not FBR). They are placed on a
dedicated "Print Pack" tab so they do not clutter the main invoice form.
"""

from __future__ import annotations

import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


PRINT_PACK_FIELDS = {
	"Sales Invoice": [
		{
			"fieldname": "custom_print_pack_tab",
			"label": "Print Pack",
			"fieldtype": "Tab Break",
			"insert_after": "terms_tab",
		},
		{
			"fieldname": "custom_print_pack_company_section",
			"label": "Company Print Details",
			"fieldtype": "Section Break",
			"insert_after": "custom_print_pack_tab",
		},
		{
			"fieldname": "custom_company_name_ar",
			"label": "Company Name (AR)",
			"fieldtype": "Data",
			"insert_after": "custom_print_pack_company_section",
		},
		{
			"fieldname": "custom_company_description",
			"label": "Company Description",
			"fieldtype": "Small Text",
			"insert_after": "custom_company_name_ar",
		},
		{
			"fieldname": "custom_company_description_ar",
			"label": "Company Description (AR)",
			"fieldtype": "Small Text",
			"insert_after": "custom_company_description",
		},
		{
			"fieldname": "custom_company_phone",
			"label": "Company Phone",
			"fieldtype": "Data",
			"insert_after": "custom_company_description_ar",
		},
		{
			"fieldname": "custom_company_tel",
			"label": "Company Tel",
			"fieldtype": "Data",
			"insert_after": "custom_company_phone",
		},
		{
			"fieldname": "custom_company_phone_2",
			"label": "Company Phone 2",
			"fieldtype": "Data",
			"insert_after": "custom_company_tel",
		},
		{
			"fieldname": "custom_company_email",
			"label": "Company Email",
			"fieldtype": "Data",
			"insert_after": "custom_company_phone_2",
		},
		{
			"fieldname": "custom_company_cr_number",
			"label": "Company CR Number",
			"fieldtype": "Data",
			"insert_after": "custom_company_email",
		},
		{
			"fieldname": "custom_company_building_number",
			"label": "Company Building Number",
			"fieldtype": "Data",
			"insert_after": "custom_company_cr_number",
		},
		{
			"fieldname": "custom_company_postal_code",
			"label": "Company Postal Code",
			"fieldtype": "Data",
			"insert_after": "custom_company_building_number",
		},
		{
			"fieldname": "custom_company_additional_number",
			"label": "Company Additional Number",
			"fieldtype": "Data",
			"insert_after": "custom_company_postal_code",
		},
		{
			"fieldname": "custom_company_city",
			"label": "Company City",
			"fieldtype": "Data",
			"insert_after": "custom_company_additional_number",
		},
		{
			"fieldname": "custom_company_street",
			"label": "Company Street",
			"fieldtype": "Data",
			"insert_after": "custom_company_city",
		},
		{
			"fieldname": "custom_company_district",
			"label": "Company District",
			"fieldtype": "Data",
			"insert_after": "custom_company_street",
		},
		{
			"fieldname": "custom_print_pack_col_break_1",
			"fieldtype": "Column Break",
			"insert_after": "custom_company_district",
		},
		{
			"fieldname": "custom_branch_name",
			"label": "Branch Name",
			"fieldtype": "Data",
			"insert_after": "custom_print_pack_col_break_1",
		},
		{
			"fieldname": "custom_branch_logo",
			"label": "Branch Logo",
			"fieldtype": "Attach Image",
			"insert_after": "custom_branch_name",
		},
		{
			"fieldname": "custom_arabic_company_logo",
			"label": "Arabic Company Logo",
			"fieldtype": "Attach Image",
			"insert_after": "custom_branch_logo",
		},
		{
			"fieldname": "custom_watermark_logo",
			"label": "Watermark Logo",
			"fieldtype": "Attach Image",
			"insert_after": "custom_arabic_company_logo",
		},
		{
			"fieldname": "custom_brands_footer_image",
			"label": "Brands Footer Image",
			"fieldtype": "Attach Image",
			"insert_after": "custom_watermark_logo",
		},
		{
			"fieldname": "custom_footer_address_en",
			"label": "Footer Address EN",
			"fieldtype": "Small Text",
			"insert_after": "custom_brands_footer_image",
		},
		{
			"fieldname": "custom_footer_address_ar",
			"label": "Footer Address AR",
			"fieldtype": "Small Text",
			"insert_after": "custom_footer_address_en",
		},
		{
			"fieldname": "custom_print_pack_customer_section",
			"label": "Customer Print Details",
			"fieldtype": "Section Break",
			"insert_after": "custom_footer_address_ar",
			"collapsible": 1,
		},
		{
			"fieldname": "custom_customer_id",
			"label": "Customer ID",
			"fieldtype": "Data",
			"insert_after": "custom_print_pack_customer_section",
		},
		{
			"fieldname": "custom_customer_name_ar",
			"label": "Customer Name (AR)",
			"fieldtype": "Data",
			"insert_after": "custom_customer_id",
		},
		{
			"fieldname": "custom_customer_cr",
			"label": "Customer CR",
			"fieldtype": "Data",
			"insert_after": "custom_customer_name_ar",
		},
		{
			"fieldname": "custom_customer_cr_number",
			"label": "Customer CR Number",
			"fieldtype": "Data",
			"insert_after": "custom_customer_cr",
		},
		{
			"fieldname": "custom_old_balance",
			"label": "Old Balance",
			"fieldtype": "Currency",
			"insert_after": "custom_customer_cr_number",
			"options": "currency",
		},
		{
			"fieldname": "custom_print_pack_bank_section",
			"label": "Bank & Salesman",
			"fieldtype": "Section Break",
			"insert_after": "custom_old_balance",
			"collapsible": 1,
		},
		{
			"fieldname": "custom_salesman_name",
			"label": "Salesman Name",
			"fieldtype": "Data",
			"insert_after": "custom_print_pack_bank_section",
		},
		{
			"fieldname": "custom_bank_name",
			"label": "Bank Name",
			"fieldtype": "Data",
			"insert_after": "custom_salesman_name",
		},
		{
			"fieldname": "custom_bank_account",
			"label": "Bank Account",
			"fieldtype": "Link",
			"options": "Bank Account",
			"insert_after": "custom_bank_name",
		},
		{
			"fieldname": "custom_bank_account_number",
			"label": "Bank Account Number",
			"fieldtype": "Data",
			"insert_after": "custom_bank_account",
		},
		{
			"fieldname": "custom_iban",
			"label": "IBAN",
			"fieldtype": "Data",
			"insert_after": "custom_bank_account_number",
		},
	],
	"Sales Invoice Item": [
		{
			"fieldname": "custom_item_name_ar",
			"label": "Item Name (AR)",
			"fieldtype": "Data",
			"insert_after": "item_name",
		},
		{
			"fieldname": "custom_description_ar",
			"label": "Description (AR)",
			"fieldtype": "Text",
			"insert_after": "description",
		},
	],
	"Address": [
		{
			"fieldname": "custom_building_number",
			"label": "Building Number",
			"fieldtype": "Data",
			"insert_after": "address_line1",
		},
		{
			"fieldname": "custom_additional_number",
			"label": "Additional Number",
			"fieldtype": "Data",
			"insert_after": "custom_building_number",
		},
		{
			"fieldname": "custom_district",
			"label": "District",
			"fieldtype": "Data",
			"insert_after": "custom_additional_number",
		},
		{
			"fieldname": "custom_cr_number",
			"label": "CR Number",
			"fieldtype": "Data",
			"insert_after": "custom_district",
		},
	],
}


def sync_print_pack_custom_fields():
	"""Create/update Print Pack fields and place SI fields on the Print Pack tab."""
	create_custom_fields(PRINT_PACK_FIELDS, ignore_validate=True, update=True)
	# Force insert_after chain (create_custom_fields update can skip reorder on some versions)
	for doctype, fields in PRINT_PACK_FIELDS.items():
		for spec in fields:
			name = f"{doctype}-{spec['fieldname']}"
			if not frappe.db.exists("Custom Field", name):
				continue
			values = {
				"label": spec.get("label"),
				"insert_after": spec.get("insert_after"),
				"fieldtype": spec.get("fieldtype"),
			}
			if spec.get("options"):
				values["options"] = spec["options"]
			if "collapsible" in spec:
				values["collapsible"] = spec["collapsible"]
			frappe.db.set_value("Custom Field", name, values, update_modified=False)
	frappe.clear_cache(doctype="Sales Invoice")
	frappe.clear_cache(doctype="Sales Invoice Item")
	frappe.clear_cache(doctype="Address")
