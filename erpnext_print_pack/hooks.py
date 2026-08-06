app_name = "erpnext_print_pack"
app_title = "ERPNext Print Pack"
app_publisher = "Taimoor"
app_description = "Community-ready ERPNext print format library with 900+ Jinja templates, regional tax invoices, thermal POS, and print browser"
app_email = "taimoor986@gmail.com"
app_license = "MIT"
app_logo_url = "/assets/erpnext_print_pack/images/print_pack_logo.svg"
app_home = "/app/print-format-browser"

required_apps = ["erpnext"]

add_to_apps_screen = [
	{
		"name": "erpnext_print_pack",
		"logo": app_logo_url,
		"title": "ERPNext Print Pack",
		"route": app_home,
	}
]

fixtures = [
	{
		"dt": "Custom Field",
		"filters": [["name", "in", [
			"Sales Invoice-custom_bank_account",
			"Sales Invoice-custom_bank_name",
			"Sales Invoice-custom_bank_account_number",
			"Sales Invoice-custom_iban",
			"Sales Invoice-custom_branch_name",
			"Sales Invoice-custom_branch_logo",
			"Sales Invoice-custom_arabic_company_logo",
			"Sales Invoice-custom_watermark_logo",
			"Sales Invoice-custom_brands_footer_image",
			"Sales Invoice-custom_company_cr_number",
			"Sales Invoice-custom_company_postal_code",
			"Sales Invoice-custom_company_additional_number",
			"Sales Invoice-custom_company_building_number",
			"Sales Invoice-custom_company_city",
			"Sales Invoice-custom_company_street",
			"Sales Invoice-custom_company_district",
			"Sales Invoice-custom_company_phone",
			"Sales Invoice-custom_company_phone_2",
			"Sales Invoice-custom_company_tel",
			"Sales Invoice-custom_company_email",
			"Sales Invoice-custom_company_name_ar",
			"Sales Invoice-custom_company_description",
			"Sales Invoice-custom_company_description_ar",
			"Sales Invoice-custom_customer_name_ar",
			"Sales Invoice-custom_customer_cr",
			"Sales Invoice-custom_customer_cr_number",
			"Sales Invoice-custom_customer_id",
			"Sales Invoice-custom_old_balance",
			"Sales Invoice-custom_salesman_name",
			"Sales Invoice-custom_footer_address_en",
			"Sales Invoice-custom_footer_address_ar",
			"Address-custom_building_number",
			"Address-custom_additional_number",
			"Address-custom_district",
			"Address-custom_cr_number",
			"Sales Invoice Item-custom_item_name_ar",
			"Sales Invoice Item-custom_description_ar",
		]]],
	},
]

# Print Formats are NOT managed via fixtures.
# Source of truth: print_pack/print_format/* + manifest + print_format_sync.py

after_install = "erpnext_print_pack.install.after_install"
after_migrate = ["erpnext_print_pack.install.after_migrate"]

jinja = {
	"methods": [
		"erpnext_print_pack.jinja_methods.print_helpers",
	],
}
