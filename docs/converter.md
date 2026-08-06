# Converter

Convert compatible HTML invoice files into **draft** ERPNext print formats.

```bash
bench --site YOUR-SITE execute erpnext_print_pack.converter.cli.run --kwargs '{
  "input_path": "/tmp/invoice.html",
  "doc_type": "Sales Invoice",
  "name": "Imported Invoice",
  "source_url": "https://github.com/example/repo",
  "source_license": "MIT"
}'
```

Converted templates are always `status: draft` until manually reviewed.

Scripts, remote fonts, animations, and JavaScript are stripped or flagged.
