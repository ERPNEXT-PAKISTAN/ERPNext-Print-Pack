import json
import re
from pathlib import Path

import pytest

from conftest import FORBIDDEN_PATTERNS, iter_formats, load_manifest


ALL_FORMATS = list(iter_formats())
ALL_SLUGS = [slug for slug, _, _ in ALL_FORMATS]
STABLE_FORMATS = [(s, m, h) for s, m, h in ALL_FORMATS if m.get("status") == "stable"]
DRAFT_FORMATS = [(s, m, h) for s, m, h in ALL_FORMATS if m.get("status") == "draft"]


@pytest.mark.parametrize("slug,meta,html_path", ALL_FORMATS, ids=ALL_SLUGS)
def test_metadata_required_fields(slug, meta, html_path):
	required = {
		"name", "slug", "doc_type", "theme", "category", "orientation",
		"paper_size", "languages", "features", "source_type", "source_license",
		"attribution_required", "erpnext_versions", "status",
	}
	assert required.issubset(meta.keys()), slug


@pytest.mark.parametrize("slug,meta,html_path", ALL_FORMATS, ids=ALL_SLUGS)
def test_html_exists_and_non_empty(slug, meta, html_path):
	content = html_path.read_text(encoding="utf-8")
	assert content.strip(), slug


@pytest.mark.parametrize("slug,meta,html_path", ALL_FORMATS, ids=ALL_SLUGS)
def test_forbidden_markup(slug, meta, html_path):
	content = html_path.read_text(encoding="utf-8").lower()
	for pattern in FORBIDDEN_PATTERNS:
		assert pattern not in content, f"{slug}: found {pattern}"


@pytest.mark.parametrize("slug,meta,html_path", ALL_FORMATS, ids=ALL_SLUGS)
def test_jinja_balance(slug, meta, html_path):
	content = html_path.read_text(encoding="utf-8")
	for token in ("if", "for", "macro", "block"):
		opens = len(re.findall(rf"\{{%-?\s*{token}\b", content))
		closes = len(re.findall(rf"\{{%-?\s*end{token}\b", content))
		assert opens == closes, f"{slug}: {token}"


@pytest.mark.parametrize("slug,meta,html_path", ALL_FORMATS, ids=ALL_SLUGS)
def test_print_format_json_values(slug, meta, html_path):
	pf_json = next(p for p in html_path.parent.glob("*.json") if p.name != "metadata.json")
	pf = json.loads(pf_json.read_text(encoding="utf-8"))
	assert pf.get("standard") == "No", slug
	assert pf.get("custom_format") == 1, slug
	assert pf.get("print_format_type") == "Jinja", slug
	if meta.get("status") == "draft":
		assert pf.get("disabled") == 1, slug


def test_unique_slugs():
	slugs = [meta["slug"] for _, meta, _ in ALL_FORMATS]
	assert len(slugs) == len(set(slugs))


def test_unique_names():
	names = [meta["name"] for _, meta, _ in ALL_FORMATS]
	assert len(names) == len(set(names))


def test_manifest_matches_disk():
	manifest = load_manifest()
	assert len(manifest["formats"]) == len(ALL_FORMATS)


def test_stable_draft_counts():
	manifest = load_manifest()
	stable = sum(1 for f in manifest["formats"] if f["status"] == "stable")
	draft = sum(1 for f in manifest["formats"] if f["status"] == "draft")
	assert stable == len(STABLE_FORMATS)
	assert draft == len(DRAFT_FORMATS)


def test_component_registry():
	from erpnext_print_pack.components.registry import COMPONENT_REGISTRY, COMPONENTS_DIR

	assert len(COMPONENT_REGISTRY) >= 50
	for rel in COMPONENT_REGISTRY.values():
		assert (COMPONENTS_DIR / rel).exists(), rel


def test_theme_registry():
	from erpnext_print_pack.themes.registry import THEME_REGISTRY, THEMES_DIR

	assert len(THEME_REGISTRY) >= 20
	for key in THEME_REGISTRY:
		assert (THEMES_DIR / f"{key}.css").exists(), key


def test_converter_path_traversal_blocked():
	from erpnext_print_pack.converter import _resolve_output_dir

	with pytest.raises(ValueError):
		_resolve_output_dir("../outside")


def test_converter_rejects_unsafe_html(tmp_path):
	from erpnext_print_pack.converter import convert

	inp = tmp_path / "bad.html"
	inp.write_text('<html><body><script>alert(1)</script><a href="javascript:alert(1)">x</a></body></html>')
	result = convert(str(inp), "Sales Invoice", "Traversal Test Format", source_license="MIT")
	out = Path(result.output_dir)
	assert out.exists()
	html = (out / "traversal_test_format.html").read_text(encoding="utf-8").lower()
	assert "<script" not in html
	assert "javascript:" not in html
	# cleanup generated test format
	import shutil
	shutil.rmtree(out, ignore_errors=True)


def test_export_slug_deterministic():
	from erpnext_print_pack.print_format_sync import _safe_slug

	assert _safe_slug("Modern Sales Invoice") == "modern_sales_invoice"


def test_export_path_traversal_blocked():
	from erpnext_print_pack.print_format_sync import _resolve_export_dir

	with pytest.raises(Exception):
		_resolve_export_dir("../evil")
