# Changelog

## 0.3.0 - 2026-08-06

### Production hardening
- Removed Print Format from Frappe fixtures (sync engine is sole source of truth)
- Added per-site sync registry with last_synced_checksum ownership tracking
- Rewrote sync summary: discovered/eligible/skipped_locally_modified/skipped_unmanaged/etc.
- Dry-run now validates Jinja via `frappe.utils.jinja.validate_template`
- Hardened converter against path traversal, unsafe URLs, and forbidden tags
- Hardened exporter with atomic writes, overwrite guards, unmanaged/standard blocks
- Expanded parametrized tests across all 318 formats
- Added site-level validate_print_formats and audit_doctypes scripts

## 0.2.0 - 2026-08-06

- Rebuilt erpnext_print_pack as a community-ready print format library
- Added 319 print formats (102 stable, 217 draft)
- Added 60 reusable components and 24 themes
- Added robust sync/export engine with dry-run and checksum safety
- Added HTML converter, validation scripts, tests, and GitHub Actions
- Preserved bilingual Sales Invoice Format template

## 0.1.0

- Initial scaffold with bilingual sales invoice and basic sync
