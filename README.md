# ERPNext Print Pack

A production-ready **ERPNext / Frappe v15–v16** print-format library with **320+ Jinja templates**, reusable components, themes, sync tooling, and an HTML converter.

## Features

- **320 print formats** across sales, purchasing, stock, manufacturing, HR, and labels
- **102 stable** templates installed by default; **218 draft** templates for review
- **60 reusable components** (headers, party blocks, item tables, totals, QR, signatures)
- **24 neutral visual themes** (Minimal, Modern, Corporate, Bilingual, Thermal, etc.)
- **One-command sync** with dry-run, checksum safety, and ownership detection
- **Site-to-files export** for customization workflows
- **HTML converter** for draft imports with license tracking
- **Validation + pytest + GitHub Actions**

## Quick start

```bash
cd frappe-bench
bench get-app https://github.com/YOUR_USER/erpnext-print-pack.git
bench --site YOUR-SITE install-app erpnext_print_pack
bench --site YOUR-SITE migrate
```

## Sync commands

```bash
# Dry run
bench --site YOUR-SITE execute erpnext_print_pack.print_format_sync.sync_all --kwargs '{"dry_run": true}'

# Sync all stable formats
bench --site YOUR-SITE execute erpnext_print_pack.print_format_sync.sync_all

# Sync one DocType
bench --site YOUR-SITE execute erpnext_print_pack.print_format_sync.sync_all --kwargs '{"doc_type": "Sales Invoice"}'

# Sync one format
bench --site YOUR-SITE execute erpnext_print_pack.print_format_sync.sync_one --kwargs '{"print_format_name": "Modern Sales Invoice"}'

# Include draft templates
bench --site YOUR-SITE execute erpnext_print_pack.print_format_sync.sync_all --kwargs '{"include_draft": true}'
```

## Export

```bash
bench --site YOUR-SITE execute erpnext_print_pack.scripts.export_print_format.execute --kwargs '{"print_format_name": "Modern Sales Invoice", "overwrite": true}'
```

## Converter

```bash
bench --site YOUR-SITE execute erpnext_print_pack.converter.cli.run --kwargs '{
  "input_path": "/tmp/invoice.html",
  "doc_type": "Sales Invoice",
  "name": "Imported Modern Invoice",
  "source_license": "MIT"
}'
```

## Developer validation

```bash
cd apps/erpnext_print_pack
python scripts/validate_repository.py
python scripts/build_catalog.py
python scripts/check_licenses.py
pytest -q
python scripts/bootstrap_library.py   # regenerate library from code
```

## Documentation

- [Installation](docs/installation.md)
- [Usage](docs/usage.md)
- [Customization](docs/customization.md)
- [Components](docs/components.md)
- [Themes](docs/themes.md)
- [Converter](docs/converter.md)
- [Supported DocTypes](docs/supported_doctypes.md)
- [Licensing](docs/licensing.md)
- [Troubleshooting](docs/troubleshooting.md)
- [Format catalog](FORMAT_CATALOG.md)

## Preserved template

The original **Sales Invoice Format** bilingual tax invoice (`sales_invoice_bilingual_tax`) is preserved unchanged.

## License

MIT — see [LICENSE](LICENSE) and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
