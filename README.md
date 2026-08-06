# ERPNext Print Pack

A production-ready **ERPNext / Frappe v15–v16** print-format library with **900+ Jinja templates**, regional tax invoices (Saudi ZATCA, UAE VAT, Pakistan FBR), proforma styles, thermal POS receipts, premium layouts, and a built-in **Print Format Browser**.

![ZATCA E-Invoice specimen](docs/images/preview_zatca_invoice.svg)

![FBR Pakistan sales tax invoice](docs/images/preview_fbr_pakistan_invoice.svg)

## Features

- **900+ print formats** across sales, purchasing, stock, manufacturing, HR, and labels
- **Print Format Browser** — preview, filter by region/layout, set default, print/PDF
- **Regional tax layouts** — Saudi ZATCA, UAE VAT, Pakistan FBR, India GST, USA, Gulf
- **FBR Pakistan-1 / 2 / 3** — adapted from FBR Integration (standalone copies, no conflict)
- **Proforma invoices** — 4 styles (ZATCA, UAE, Modern, Classic)
- **Thermal / POS** — 80mm receipts with word-wrapped item names
- **Document voucher barcodes** — Code128 of ERPNext document name on premium/specimen layouts
- **Pakistan FBR QR** — uses `custom_fbr_invoice_no` when present
- **Frappe v15 workspace** — **Print Pack** workspace with browser shortcut

## New installation

```bash
cd frappe-bench
bench get-app https://github.com/ERPNEXT-PAKISTAN/ERPNext-Print-Pack.git
bench --site site1.local install-app erpnext_print_pack
bench --site site1.local migrate
bench --site site1.local clear-cache
```

Open **Print Pack** from the app screen (purple printer icon) or go to `/app/print-format-browser`.

## Update an existing site

```bash
cd frappe-bench
bench update --apps erpnext_print_pack
bench --site site1.local migrate
bench --site site1.local clear-cache
```

Formats sync automatically on `migrate` via `after_migrate`. You can also use **Sync HTML (Stable)** from the Print Format Browser menu.

## Frappe v15 workspace

After migrate, find **Print Pack** in the desk sidebar. It links to:

- Print Format Browser (main page)
- Print Format, Letter Head, Print Settings
- Popular documents (Sales Invoice, Delivery Note, POS Invoice, Payment Entry)

## FBR Pakistan formats

Three sales tax invoice layouts copied from **FBR Integration** (read-only source; original app untouched):

| Format | Source |
|--------|--------|
| FBR Pakistan-1 Sales Invoice | Sales Invoice Tax |
| FBR Pakistan-2 Sales Invoice | FBR Sales Invoice |
| FBR Pakistan-3 Sales Invoice | FBR Letterhead-2 |

QR and barcode use `custom_fbr_invoice_no` via `erpnext_print_pack.print_barcodes` (no dependency on FBR Integration at print time).

## Developer validation

```bash
cd apps/erpnext_print_pack
python scripts/validate_repository.py
python scripts/build_catalog.py
pytest -q
```

## Documentation

- [Installation](docs/installation.md)
- [Usage](docs/usage.md)
- [Customization](docs/customization.md)
- [Supported DocTypes](docs/supported_doctypes.md)
- [Licensing](docs/licensing.md)
- [Troubleshooting](docs/troubleshooting.md)

## Preserved template

The original **Sales Invoice Format** bilingual tax invoice (`sales_invoice_bilingual_tax`) is preserved unchanged.

## License

MIT — see [LICENSE](LICENSE) and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
