# Changelog

## 0.5.3 - 2026-08-11

### Print text layout fix
- Fixed vertical/stacked letter names in meta sections (Yellow Sidebar and others) caused by aggressive page-fit CSS
- Meta label columns now keep horizontal text; wrapping uses word boundaries only

## 0.5.2 - 2026-08-11

### BOM print coverage
- BOM formats show finished good, raw materials/components, operations, exploded/secondary items, and cost totals

### A4 page fit
- Shared page-fit CSS (`table-layout: fixed`, max-width 100%, word-wrap) for premium, theme, regional, and specimen layouts
- Sales Invoice item tables slimmed to equal-width columns that stay inside A4

## 0.5.1 - 2026-08-11

### Field coverage
- Expense Claim: mode of payment, payable account, bank/cash account, advances/taxes, remarks below
- Remarks block at bottom for Journal Entry, sales/purchase invoices & orders, delivery notes, stock, payments, etc.
- Item detail: valuation method/rate, tax templates, default warehouse/store, item group, UOMs, barcodes, item prices

### No HTML / Enable fix
- Root cause: draft formats were synced without HTML (210 empty disabled records)
- Migrate/sync now loads draft HTML too; Enable auto-syncs HTML if missing
- Sync preserves site Enable/Disable after first create

## 0.5.0 - 2026-08-11

### DocType-aware print layouts
- Added shared `detail_blocks` engine covering Journal Entry accounts (debit/credit/party/cost center), Payment Entry accounts/references/deductions/taxes, Stock Entry warehouses/batch/serial/additional costs, Material Request, Work Order, Salary Slip, Expense Claim, Timesheet, and BOM
- Regenerated premium/theme/regional/specimen formats (~995) with richer item/account tables, remarks, and totals
- Expanded Payment Entry / Journal Entry / Stock Entry theme coverage

### Reliability & UX
- Sync now hashes actual HTML (not stale metadata checksums) and batches registry writes atomically
- Generators emit required metadata (`attribution_required`, `erpnext_versions`)
- Catalog rebuilt to match disk; repository validation clean
- Print Format Browser: removed N+1 HTML lookups; sandboxed preview iframe
- Removed inline `onerror` handlers from FBR templates

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
