#!/usr/bin/env python3
import frappe

from erpnext_print_pack.print_format_sync import export_print_format


def execute(
	print_format_name: str,
	overwrite: bool = False,
	dry_run: bool = False,
	allow_standard: bool = False,
	allow_unmanaged: bool = False,
):
	frappe.only_for("System Manager")
	result = export_print_format(
		print_format_name,
		overwrite=overwrite,
		dry_run=dry_run,
		allow_standard=allow_standard,
		allow_unmanaged=allow_unmanaged,
	)
	print(result)
	return result
