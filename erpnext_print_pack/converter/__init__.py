"""HTML to ERPNext Jinja print format converter (untrusted input)."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parent.parent
PRINT_FORMAT_ROOT = (APP_ROOT / "print_pack" / "print_format").resolve()

FORBIDDEN_TAGS = {"script", "iframe", "form", "object", "embed"}
FORBIDDEN_ATTRS = re.compile(r"on\w+\s*=", re.I)
UNSAFE_URL = re.compile(r"(javascript:|vbscript:|data:text/html|file:)", re.I)
META_REFRESH = re.compile(r"<meta[^>]+http-equiv\s*=\s*['\"]refresh", re.I)


@dataclass
class ConversionResult:
	status: str = "draft"
	warnings: list[str] = field(default_factory=list)
	output_dir: str | None = None
	manual_checks: list[str] = field(default_factory=list)


class _Cleaner(HTMLParser):
	def __init__(self):
		super().__init__()
		self.parts: list[str] = []
		self.warnings: list[str] = []

	def handle_starttag(self, tag, attrs):
		tag = tag.lower()
		if tag in FORBIDDEN_TAGS:
			self.warnings.append(f"Removed <{tag}> element")
			return
		if tag in {"html", "head", "body"}:
			return
		attr_str = ""
		for k, v in attrs:
			if FORBIDDEN_ATTRS.search(k):
				self.warnings.append(f"Removed unsafe attribute {k}")
				continue
			if v and UNSAFE_URL.search(v):
				self.warnings.append(f"Removed unsafe URL in {k}")
				continue
			if v is None:
				attr_str += f" {k}"
			else:
				attr_str += f' {k}="{v}"'
		self.parts.append(f"<{tag}{attr_str}>")

	def handle_endtag(self, tag):
		tag = tag.lower()
		if tag in FORBIDDEN_TAGS or tag in {"html", "head", "body"}:
			return
		self.parts.append(f"</{tag}>")

	def handle_data(self, data):
		self.parts.append(data)

	def get_html(self) -> str:
		return "".join(self.parts)


def _safe_slug(name: str) -> str:
	slug = (name or "imported").lower().replace(" ", "_").replace("-", "_")
	slug = "".join(ch if ch.isalnum() or ch == "_" else "_" for ch in slug)
	return slug or "imported_format"


def _resolve_output_dir(slug: str) -> Path:
	target = (PRINT_FORMAT_ROOT / slug).resolve()
	if not str(target).startswith(str(PRINT_FORMAT_ROOT)):
		raise ValueError("Path traversal blocked: output outside print_format directory")
	return target


def clean_html(raw: str) -> tuple[str, list[str]]:
	if META_REFRESH.search(raw):
		raw = META_REFRESH.sub("", raw)
	parser = _Cleaner()
	try:
		parser.feed(raw)
	except Exception as exc:
		return raw, [f"HTML parse warning: {exc}"]
	return parser.get_html(), parser.warnings


def normalize_css(css: str) -> tuple[str, list[str]]:
	warnings = []
	if "@import" in css or re.search(r"url\s*\(\s*['\"]?https?://", css, re.I):
		warnings.append("Remote CSS imports detected; removed/flagged")
	css = re.sub(r"@import[^;]+;", "", css)
	css = re.sub(r"@keyframes[\s\S]*?\}", "", css)
	css = re.sub(r"animation\s*:[^;]+;", "", css)
	return css.strip(), warnings


def validate_jinja_balance(html: str) -> list[str]:
	issues = []
	for token in ("if", "for", "macro", "block"):
		opens = len(re.findall(rf"\{{%-?\s*{token}\b", html))
		closes = len(re.findall(rf"\{{%-?\s*end{token}\b", html))
		if opens != closes:
			issues.append(f"Unbalanced {token}: open={opens} close={closes}")
	return issues


def convert(
	input_path: str,
	doc_type: str,
	name: str,
	source_url: str | None = None,
	source_license: str | None = None,
) -> ConversionResult:
	result = ConversionResult()
	if not source_license:
		result.warnings.append("Missing source_license; defaulting to draft-only import")
		source_license = "UNKNOWN"

	path = Path(input_path).resolve()
	if not path.exists():
		raise FileNotFoundError(input_path)

	raw = path.read_text(encoding="utf-8")
	cleaned, w1 = clean_html(raw)
	result.warnings.extend(w1)

	style_match = re.search(r"<style[^>]*>([\s\S]*?)</style>", raw, re.I)
	css = ""
	if style_match:
		css, w2 = normalize_css(style_match.group(1))
		result.warnings.extend(w2)

	jinja = f"""{{# Converted by erpnext_print_pack · status: draft · review required #}}
<style>
{css}
</style>
<div class="epp-root converted-format">
{cleaned}
</div>
"""
	result.manual_checks.extend(validate_jinja_balance(jinja))
	result.manual_checks.extend([
		"Verify item loops for line items",
		"Verify tax rows mapping",
		"Verify party and address fields",
		"Test PDF output in ERPNext",
	])

	slug = _safe_slug(name)
	out = _resolve_output_dir(slug)
	out.mkdir(parents=True, exist_ok=True)

	(out / f"{slug}.html").write_text(jinja, encoding="utf-8")
	(out / f"{slug}.json").write_text(
		json.dumps(
			{
				"doctype": "Print Format",
				"name": name,
				"doc_type": doc_type,
				"module": "Print Pack",
				"custom_format": 1,
				"print_format_type": "Jinja",
				"standard": "No",
				"disabled": 1,
			},
			indent=1,
		)
		+ "\n",
		encoding="utf-8",
	)
	metadata = {
		"name": name,
		"slug": slug,
		"doc_type": doc_type,
		"theme": "imported",
		"category": "imported",
		"orientation": "portrait",
		"paper_size": "A4",
		"languages": ["en"],
		"features": [],
		"source_type": "converted",
		"source_url": source_url,
		"source_license": source_license,
		"attribution_required": bool(source_url),
		"erpnext_versions": ["15", "16"],
		"status": "draft",
	}
	(out / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
	(out / "README.md").write_text(f"# {name}\n\nConverted draft. Manual review required.\n", encoding="utf-8")

	result.output_dir = str(out)
	return result
