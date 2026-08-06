Install with Bench:

```bash
bench get-app https://github.com/YOUR_USER/erpnext-print-pack.git
bench --site YOUR-SITE install-app erpnext_print_pack
bench --site YOUR-SITE migrate
```

Requirements: ERPNext 15 or 16, Frappe 15 or 16.

Only **stable** formats sync on install. Draft formats remain in the repository for review.

Disable Letter Head on custom header formats if duplicate headers appear.
