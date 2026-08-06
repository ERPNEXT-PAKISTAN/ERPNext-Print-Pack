import pytest

pytest.importorskip("frappe")

try:
	import frappe

	if not getattr(frappe.local, "site", None):
		pytest.skip("Frappe site context not available", allow_module_level=True)
except Exception:
	pytest.skip("Frappe not initialized", allow_module_level=True)

from erpnext_print_pack.print_format_sync import sync_all


class TestSyncBehavior:
	def test_dry_run_does_not_write(self):
		before = frappe.db.count("Print Format", {"module": "Print Pack"})
		result = sync_all(dry_run=True, statuses=("stable",))
		after = frappe.db.count("Print Format", {"module": "Print Pack"})
		assert before == after
		assert result["discovered"] >= 100
		assert result["skipped_draft"] >= 200

	def test_drafts_excluded_by_default(self):
		result = sync_all(dry_run=True, statuses=("stable",))
		assert result["skipped_draft"] > 0
		assert result["eligible"] <= result["discovered"]
