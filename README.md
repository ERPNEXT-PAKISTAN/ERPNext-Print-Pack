# ERPNext Print Pack

A production-ready **ERPNext / Frappe v15 and v16** print-format library with **900+ Jinja templates** for **all countries and tax authorities** — regional e-invoices, proforma styles, thermal POS receipts, premium layouts, item detail sheets, and a built-in **Print Format Browser**.

![ZATCA E-Invoice specimen](docs/images/preview_zatca_invoice.svg)

![Regional tax invoice sample](docs/images/preview_fbr_pakistan_invoice.svg)

## Features

- **900+ print formats** across sales, purchasing, stock, manufacturing, HR, payments, and labels
- **Print Format Browser** — preview, filter by region/layout, set default, print/PDF
- **Global regional layouts** — Saudi ZATCA, UAE VAT, Pakistan FBR, India GST, USA, Gulf, and more
- **Proforma invoices** — multiple styles for quotations and sales documents
- **Thermal / POS** — 80mm receipts with word-wrapped item names
- **Payment Entry receipts** — payment type, party, mode of payment, bank/cash account, amount
- **Item detail reports** — item image, valuation method, barcode, last two purchases
- **Document voucher barcodes** — Code128 of ERPNext document name on premium/specimen layouts

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
