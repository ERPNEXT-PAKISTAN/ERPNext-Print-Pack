# Usage

1. Install the app
2. Open any supported DocType
3. Menu → Print → choose a format prefixed by theme name (e.g. **Modern Sales Invoice**)
4. Use **Sales Invoice Format** for the preserved bilingual tax layout

Re-sync after editing repository files:

```bash
bench --site YOUR-SITE execute erpnext_print_pack.print_format_sync.sync_all
```

Dry run first:

```bash
bench --site YOUR-SITE execute erpnext_print_pack.print_format_sync.sync_all --kwargs '{"dry_run": true}'
```
