"""Persisted sync ownership and checksum registry (per site)."""

from __future__ import annotations

import json
from pathlib import Path

import frappe

APP_ROOT = Path(__file__).resolve().parent
REGISTRY_FILENAME = "epp_print_pack_sync_registry.json"


def get_registry_path() -> Path:
	if getattr(frappe.local, "site", None):
		return Path(frappe.get_site_path(REGISTRY_FILENAME))
	return APP_ROOT / "print_pack" / "sync_registry.default.json"


def load_registry() -> dict:
	path = get_registry_path()
	if path.exists():
		return json.loads(path.read_text(encoding="utf-8"))
	return {"version": 1, "formats": {}}


def save_registry(data: dict) -> None:
	path = get_registry_path()
	path.parent.mkdir(parents=True, exist_ok=True)
	path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def get_format_record(name: str) -> dict | None:
	return load_registry().get("formats", {}).get(name)


def set_format_record(
	name: str,
	*,
	slug: str,
	source_checksum: str,
	synced_checksum: str,
	owned: bool = True,
	status: str = "stable",
) -> None:
	data = load_registry()
	data.setdefault("formats", {})[name] = {
		"slug": slug,
		"owned": owned,
		"status": status,
		"source_checksum": source_checksum,
		"last_synced_checksum": synced_checksum,
	}
	save_registry(data)


def remove_format_record(name: str) -> None:
	data = load_registry()
	if name in data.get("formats", {}):
		del data["formats"][name]
		save_registry(data)
