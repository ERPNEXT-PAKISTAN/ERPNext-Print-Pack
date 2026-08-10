import json

import frappe

from erpnext_print_pack.print_format_sync import sync_all


def _run_stable_sync(context: str):
	"""Sync stable + draft formats (drafts stay disabled) so Enable always has HTML."""
	try:
		result = sync_all(
			statuses=("stable", "draft"),
			dry_run=False,
			force=False,
			include_draft=True,
			fail_fast=False,
		)
		summary = {
			"created": result.get("created"),
			"updated": result.get("updated"),
			"unchanged": result.get("unchanged"),
			"skipped_locally_modified": result.get("skipped_locally_modified"),
			"skipped_missing_doctype": result.get("skipped_missing_doctype"),
			"failed_validation": result.get("failed_validation"),
			"failed": result.get("failed"),
		}
		frappe.logger().info(f"erpnext_print_pack {context} sync: {json.dumps(summary)}")
		return result
	except Exception:
		frappe.log_error(title=f"erpnext_print_pack {context} sync failed")
		return None


def after_install():
	"""Install stable formats only; never force; never include drafts."""
	_run_stable_sync("after_install")


def after_migrate():
	_run_stable_sync("after_migrate")
