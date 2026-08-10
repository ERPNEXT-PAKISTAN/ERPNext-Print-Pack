"""Persisted sync ownership and checksum registry (per site)."""

from __future__ import annotations

import json
import os
import tempfile
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
	payload = json.dumps(data, indent=2, sort_keys=True) + "\n"
	fd, tmp_name = tempfile.mkstemp(prefix=".epp_sync_", dir=str(path.parent))
	try:
		with os.fdopen(fd, "w", encoding="utf-8") as handle:
			handle.write(payload)
		os.replace(tmp_name, path)
	except Exception:
		try:
			os.unlink(tmp_name)
		except OSError:
			pass
		raise


def get_format_record(name: str, registry: dict | None = None) -> dict | None:
	data = registry if registry is not None else load_registry()
	return data.get("formats", {}).get(name)


def set_format_record(
	name: str,
	*,
	slug: str,
	source_checksum: str,
	synced_checksum: str,
	owned: bool = True,
	status: str = "stable",
	registry: dict | None = None,
	persist: bool = True,
) -> dict:
	data = registry if registry is not None else load_registry()
	data.setdefault("formats", {})[name] = {
		"slug": slug,
		"owned": owned,
		"status": status,
		"source_checksum": source_checksum,
		"last_synced_checksum": synced_checksum,
	}
	if persist:
		save_registry(data)
	return data


def remove_format_record(name: str) -> None:
	data = load_registry()
	if name in data.get("formats", {}):
		del data["formats"][name]
		save_registry(data)
