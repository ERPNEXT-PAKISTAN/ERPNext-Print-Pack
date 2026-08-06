# Troubleshooting

## Formats not visible after install

Run sync manually with dry-run, then live sync.

## Duplicate headers

Disable Letter Head for formats that include their own header.

## PDF spacing issues

ERPNext applies `.print-format td { padding: 6px !important }`. Templates include overrides where needed.

## Draft formats missing

Draft formats are disabled by default. Sync with `include_draft: true`.

## Locally modified format skipped

Expected behavior. Export, merge changes, or use `force=True` deliberately.
