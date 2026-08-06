# Customization

1. Export an existing format from your site
2. Edit HTML locally under `print_pack/print_format/<slug>/`
3. Update `metadata.json` checksum by re-running bootstrap or saving via export
4. Sync with dry-run, then live sync

User-modified Print Formats that are not app-owned are **never overwritten**.

Use `force=True` only when you intentionally want to replace site content.
