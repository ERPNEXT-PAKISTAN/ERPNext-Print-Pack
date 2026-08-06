"""Robust Print Format synchronization for erpnext_print_pack."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from pathlib import Path

import frappe

from erpnext_print_pack.sync_registry import get_format_record, set_format_record

APP_ROOT = Path(__file__).resolve().parent
PRINT_FORMAT_ROOT = APP_ROOT / "print_pack" / "print_format"
MANIFEST_PATH = APP_ROOT / "print_pack" / "manifest.json"
APP_MODULE = "Print Pack"
SKIP_FIELDS = {"creation", "modified", "modified_by", "owner", "docstatus", "doctype"}


@dataclass
class SyncResult:
	discovered: int = 0
	eligible: int = 0
	created: list[str] = field(default_factory=list)
	updated: list[str] = field(default_factory=list)
	unchanged: list[str] = field(default_factory=list)
	skipped_draft: list[str] = field(default_factory=list)
	skipped_missing_doctype: list[str] = field(default_factory=list)
	skipped_locally_modified: list[str] = field(default_factory=list)
	skipped_name_conflict: list[str] = field(default_factory=list)
	skipped_unmanaged: list[str] = field(default_factory=list)
	failed_validation: list[tuple[str, str]] = field(default_factory=list)
	failed: list[tuple[str, str]] = field(default_factory=list)

	def summary(self) -> dict:
		return {
			"discovered": self.discovered,
			"eligible": self.eligible,
			"created": len(self.created),
			"updated": len(self.updated),
			"unchanged": len(self.unchanged),
			"skipped_draft": len(self.skipped_draft),
			"skipped_missing_doctype": len(self.skipped_missing_doctype),
			"skipped_locally_modified": len(self.skipped_locally_modified),
			"skipped_name_conflict": len(self.skipped_name_conflict),
			"skipped_unmanaged": len(self.skipped_unmanaged),
			"failed_validation": len(self.failed_validation),
			"failed": len(self.failed),
			"details": {
				"created": self.created[:25],
				"updated": self.updated[:25],
				"unchanged": self.unchanged[:25],
				"skipped_draft": self.skipped_draft[:10],
				"skipped_missing_doctype": self.skipped_missing_doctype[:25],
				"skipped_locally_modified": self.skipped_locally_modified[:25],
				"skipped_name_conflict": self.skipped_name_conflict[:25],
				"skipped_unmanaged": self.skipped_unmanaged[:25],
				"failed_validation": self.failed_validation[:25],
				"failed": self.failed[:25],
			},
		}


def _checksum(value: str) -> str:
	return hashlib.sha256((value or "").encode("utf-8")).hexdigest()


def _validate_manifest() -> None:
	if not MANIFEST_PATH.exists():
		frappe.throw(f"Missing core manifest: {MANIFEST_PATH}")
	try:
		json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
	except json.JSONDecodeError as exc:
		frappe.throw(f"Corrupted manifest JSON: {exc}")


def _iter_format_dirs():
	if not PRINT_FORMAT_ROOT.is_dir():
		return
	for path in sorted(PRINT_FORMAT_ROOT.iterdir()):
		if not path.is_dir():
			continue
		candidates = [p for p in path.glob("*.json") if p.name != "metadata.json"]
		if candidates and list(path.glob("*.html")):
			yield path


def _load_format(format_dir: Path) -> tuple[dict, dict, str, Path]:
	slug = format_dir.name
	pf_json = format_dir / f"{slug}.json"
	if not pf_json.exists():
		candidates = [p for p in format_dir.glob("*.json") if p.name != "metadata.json"]
		if not candidates:
			raise FileNotFoundError(f"No print format JSON in {format_dir}")
		pf_json = candidates[0]
	html_path = format_dir / f"{slug}.html"
	if not html_path.exists():
		html_candidates = list(format_dir.glob("*.html"))
		if not html_candidates:
			raise FileNotFoundError(f"No HTML in {format_dir}")
		html_path = html_candidates[0]

	row = json.loads(pf_json.read_text(encoding="utf-8"))
	html = html_path.read_text(encoding="utf-8")
	meta_path = format_dir / "metadata.json"
	metadata = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else {}

	row.setdefault("doctype", "Print Format")
	row.setdefault("module", APP_MODULE)
	row.setdefault("custom_format", 1)
	row.setdefault("print_format_type", "Jinja")
	row.setdefault("standard", "No")
	row.setdefault("disabled", 0 if metadata.get("status", "stable") == "stable" else 1)
	row["html"] = html
	return row, metadata, slug, html_path


def _validate_jinja(html: str, name: str) -> str | None:
	try:
		from frappe.utils.jinja import validate_template

		validate_template(html)
		return None
	except Exception as exc:
		return str(exc)


def _doctype_exists(doc_type: str) -> bool:
	try:
		return bool(frappe.db.exists("DocType", doc_type))
	except Exception:
		return False


def _decide_action(
	name: str,
	slug: str,
	source_checksum: str,
	exists: bool,
	force: bool,
) -> tuple[str, str | None]:
	"""Return action: create|update|unchanged|skip_* and reason."""
	if not exists:
		return "create", None

	record = get_format_record(name)
	db_html = frappe.db.get_value("Print Format", name, "html") or ""
	db_checksum = _checksum(db_html)
	module = frappe.db.get_value("Print Format", name, "module")

	if record:
		if not record.get("owned", True):
			return "skip_name_conflict", "user duplicate (owned=false)"
		last_synced = record.get("last_synced_checksum", "")
		if db_checksum != last_synced and not force:
			return "skip_locally_modified", "database HTML differs from last synced checksum"
		if source_checksum == last_synced and db_checksum == last_synced and not force:
			return "unchanged", None
		if source_checksum == db_checksum and not force:
			return "unchanged", None
		return "update", None

	# No registry record
	if module != APP_MODULE:
		return "skip_unmanaged", f"existing format module={module}"
	if db_checksum != source_checksum and not force:
		# Existing app module format never synced via registry — treat edit as local
		return "skip_locally_modified", "no registry record and DB differs from source"
	return "update", None


def sync_all(
	dry_run: bool = False,
	doc_type: str | None = None,
	theme: str | None = None,
	print_format_name: str | None = None,
	statuses: tuple[str, ...] | None = None,
	include_draft: bool = False,
	force: bool = False,
	fail_fast: bool = False,
) -> dict:
	_validate_manifest()
	if statuses is None:
		statuses = ("stable",) if not include_draft else ("stable", "draft")

	result = SyncResult()
	format_dirs = list(_iter_format_dirs())
	result.discovered = len(format_dirs)

	for format_dir in format_dirs:
		try:
			row, metadata, slug, html_path = _load_format(format_dir)
		except Exception as exc:
			result.failed.append((format_dir.name, str(exc)))
			if fail_fast:
				break
			continue

		name = row.get("name") or slug
		status = metadata.get("status", "stable")

		if print_format_name and name != print_format_name:
			continue
		if doc_type and row.get("doc_type") != doc_type:
			continue
		if theme and metadata.get("theme") != theme:
			continue
		if status not in statuses:
			result.skipped_draft.append(name)
			continue

		target_doc_type = row.get("doc_type")
		if not target_doc_type:
			result.failed_validation.append((name, "missing doc_type"))
			continue
		if not _doctype_exists(target_doc_type):
			result.skipped_missing_doctype.append(name)
			continue

		source_checksum = metadata.get("checksum") or _checksum(row.get("html", ""))
		jinja_error = _validate_jinja(row["html"], name)
		if jinja_error:
			result.failed_validation.append((name, jinja_error))
			if fail_fast:
				break
			continue

		result.eligible += 1
		exists = bool(frappe.db.exists("Print Format", name))
		action, reason = _decide_action(name, slug, source_checksum, exists, force)

		if action == "skip_locally_modified":
			result.skipped_locally_modified.append(name)
			continue
		if action == "skip_unmanaged":
			result.skipped_unmanaged.append(name)
			continue
		if action == "skip_name_conflict":
			result.skipped_name_conflict.append(name)
			continue
		if action == "unchanged":
			result.unchanged.append(name)
			continue

		if dry_run:
			if action == "create":
				result.created.append(name)
			elif action == "update":
				result.updated.append(name)
			continue

		try:
			if exists:
				doc = frappe.get_doc("Print Format", name)
			else:
				doc = frappe.new_doc("Print Format")
				doc.name = name

			for key, value in row.items():
				if key in SKIP_FIELDS:
					continue
				setattr(doc, key, value)

			doc.flags.ignore_permissions = True
			if doc.is_new():
				doc.insert(ignore_permissions=True)
				result.created.append(name)
			else:
				doc.save(ignore_permissions=True)
				result.updated.append(name)

			synced_html = frappe.db.get_value("Print Format", name, "html") or row["html"]
			set_format_record(
				name,
				slug=slug,
				source_checksum=source_checksum,
				synced_checksum=_checksum(synced_html),
				owned=True,
				status=status,
			)
		except Exception as exc:
			result.failed.append((name, str(exc)))
			if fail_fast:
				break

	if not dry_run:
		frappe.db.commit()
		frappe.clear_cache(doctype="Print Format")

	return result.summary()


def sync_one(print_format_name: str, **kwargs) -> dict:
	return sync_all(print_format_name=print_format_name, **kwargs)


def sync_print_formats_from_files(include_draft: bool = False):
	return sync_all(include_draft=include_draft)


def _safe_slug(name: str) -> str:
	slug = (name or "format").lower().replace(" ", "_").replace("-", "_")
	return "".join(ch if ch.isalnum() or ch == "_" else "_" for ch in slug)


def _resolve_export_dir(slug: str) -> Path:
	if ".." in slug or slug.startswith("/"):
		raise ValueError("Invalid export slug")
	base = PRINT_FORMAT_ROOT.resolve()
	target = (PRINT_FORMAT_ROOT / slug).resolve()
	if not str(target).startswith(str(base)):
		raise ValueError("Invalid export path (path traversal blocked)")
	return target


def _atomic_write(path: Path, content: str) -> None:
	path.parent.mkdir(parents=True, exist_ok=True)
	tmp = path.with_suffix(path.suffix + ".tmp")
	tmp.write_text(content, encoding="utf-8")
	tmp.replace(path)


def export_print_format(
	name: str,
	target_dir: Path | None = None,
	overwrite: bool = False,
	dry_run: bool = False,
	allow_standard: bool = False,
	allow_unmanaged: bool = False,
) -> dict:
	doc = frappe.get_doc("Print Format", name)
	record = get_format_record(name)

	if doc.standard == "Yes" and not allow_standard:
		frappe.throw(f"Refusing to export standard Print Format: {name}")
	if doc.module != APP_MODULE and not allow_unmanaged and not (record and record.get("owned")):
		frappe.throw(f"Refusing to export unmanaged Print Format: {name}")

	slug = _safe_slug(doc.name)
	format_dir = target_dir or _resolve_export_dir(slug)
	if target_dir:
		format_dir = Path(target_dir).resolve()
		if not str(format_dir).startswith(str(PRINT_FORMAT_ROOT.resolve())):
			frappe.throw("Export target outside print_format directory")

	exists = format_dir.exists() and any(format_dir.iterdir()) if format_dir.exists() else False
	if exists and not overwrite:
		frappe.throw(f"Target exists: {format_dir}. Pass overwrite=True to replace.")

	html_content = doc.html or ""
	files = {
		"html": format_dir / f"{slug}.html",
		"json": format_dir / f"{slug}.json",
		"metadata": format_dir / "metadata.json",
		"readme": format_dir / "README.md",
	}

	if dry_run:
		return {"dry_run": True, "slug": slug, "target": str(format_dir), "files": [str(v) for v in files.values()]}

	format_dir.mkdir(parents=True, exist_ok=True)
	pf_meta = {
		k: v
		for k, v in doc.as_dict().items()
		if not k.startswith("_") and k not in SKIP_FIELDS and k != "html" and v not in (None, "")
	}
	pf_meta["doctype"] = "Print Format"
	pf_meta.setdefault("standard", "No")
	pf_meta.setdefault("custom_format", 1)
	pf_meta.setdefault("print_format_type", "Jinja")

	_atomic_write(files["html"], html_content)
	_atomic_write(files["json"], json.dumps(pf_meta, indent=1, default=str) + "\n")
	metadata = {
		"name": doc.name,
		"slug": slug,
		"doc_type": doc.doc_type,
		"theme": "exported",
		"category": "custom",
		"orientation": "portrait",
		"paper_size": "A4",
		"languages": ["en"],
		"features": [],
		"source_type": "exported",
		"source_url": None,
		"source_license": "MIT",
		"attribution_required": False,
		"erpnext_versions": ["15", "16"],
		"status": "draft",
		"checksum": _checksum(html_content),
	}
	_atomic_write(files["metadata"], json.dumps(metadata, indent=2) + "\n")
	_atomic_write(files["readme"], f"# {doc.name}\n\nExported from site.\n")

	return {"slug": slug, "target": str(format_dir), "files": [str(v) for v in files.values()]}
