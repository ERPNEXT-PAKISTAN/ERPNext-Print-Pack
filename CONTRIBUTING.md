# Contributing

1. Fork the repository
2. Create a feature branch
3. Add or edit print formats under `erpnext_print_pack/print_pack/print_format/`
4. Include `metadata.json` with license and status
5. Run `python scripts/validate_repository.py` and `pytest`
6. Run `python scripts/build_catalog.py`
7. Open a pull request

Draft templates must set `"status": "draft"` and `"disabled": 1` in JSON.

Do not commit real customer data, site configs, or secrets.
