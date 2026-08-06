import json

import frappe

from erpnext_print_pack.print_format_sync import sync_all


def after_install():
	"""Install stable formats only; never force; never include drafts."""
	try:
		result = sync_all(
			statuses=("stable",),
			dry_run=False,
			force=False,
			include_draft=False,
			fail_fast=False,
		)
		frappe.logger().info(f"erpnext_print_pack after_install sync: {json.dumps(result)}")
	except Exception:
		frappe.log_error(title="erpnext_print_pack after_install sync failed")


def after_migrate():
	try:
		result = sync_all(
			statuses=("stable",),
			dry_run=False,
			force=False,
			include_draft=False,
			fail_fast=False,
		)
		frappe.logger().info(f"erpnext_print_pack after_migrate sync: {json.dumps(result)}")
	except Exception:
		frappe.log_error(title="erpnext_print_pack after_migrate sync failed")
