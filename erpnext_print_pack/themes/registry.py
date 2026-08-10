"""Theme registry for erpnext_print_pack."""

from __future__ import annotations

from pathlib import Path

from erpnext_print_pack.page_fit_css import with_page_fit

THEMES_DIR = Path(__file__).resolve().parent

THEME_REGISTRY = {
	"minimal": {"label": "Minimal", "primary": "#333333", "accent": "#666666", "header_bg": "#ffffff"},
	"modern": {"label": "Modern", "primary": "#2563eb", "accent": "#1d4ed8", "header_bg": "#eff6ff"},
	"corporate": {"label": "Corporate", "primary": "#1e3a5f", "accent": "#0f766e", "header_bg": "#f8fafc"},
	"executive": {"label": "Executive", "primary": "#111827", "accent": "#b45309", "header_bg": "#f9fafb"},
	"material": {"label": "Material", "primary": "#1976d2", "accent": "#00897b", "header_bg": "#e3f2fd"},
	"elegant": {"label": "Elegant", "primary": "#4a3728", "accent": "#9a7b4f", "header_bg": "#faf7f2"},
	"compact": {"label": "Compact", "primary": "#374151", "accent": "#6b7280", "header_bg": "#ffffff", "font_size": "8px"},
	"clean": {"label": "Clean", "primary": "#0ea5e9", "accent": "#0284c7", "header_bg": "#f0f9ff"},
	"technical": {"label": "Technical", "primary": "#334155", "accent": "#64748b", "header_bg": "#f1f5f9", "font_family": "Consolas, monospace"},
	"industrial": {"label": "Industrial", "primary": "#44403c", "accent": "#ea580c", "header_bg": "#fafaf9"},
	"manufacturing": {"label": "Manufacturing", "primary": "#57534e", "accent": "#ca8a04", "header_bg": "#fffbeb"},
	"retail": {"label": "Retail", "primary": "#be123c", "accent": "#e11d48", "header_bg": "#fff1f2"},
	"wholesale": {"label": "Wholesale", "primary": "#0369a1", "accent": "#0891b2", "header_bg": "#ecfeff"},
	"professional_blue": {"label": "Professional Blue", "primary": "#075daa", "accent": "#0369a1", "header_bg": "#e0f2fe"},
	"professional_green": {"label": "Professional Green", "primary": "#166534", "accent": "#15803d", "header_bg": "#ecfdf5"},
	"monochrome": {"label": "Monochrome", "primary": "#000000", "accent": "#404040", "header_bg": "#ffffff"},
	"soft_gray": {"label": "Soft Gray", "primary": "#4b5563", "accent": "#9ca3af", "header_bg": "#f3f4f6"},
	"premium": {"label": "Premium", "primary": "#312e81", "accent": "#7c3aed", "header_bg": "#f5f3ff"},
	"landscape": {"label": "Landscape", "primary": "#1e40af", "accent": "#3b82f6", "header_bg": "#eff6ff", "orientation": "landscape"},
	"thermal": {"label": "Thermal", "primary": "#111827", "accent": "#374151", "header_bg": "#ffffff", "paper": "80mm", "font_size": "9px"},
	"bilingual": {"label": "Bilingual", "primary": "#075daa", "accent": "#bd852c", "header_bg": "#ffffff", "bilingual": True},
	"tax_focused": {"label": "Tax Focused", "primary": "#075daa", "accent": "#0f766e", "header_bg": "#f0fdfa", "tax_focused": True},
	"qr_enabled": {"label": "QR Enabled", "primary": "#075daa", "accent": "#0369a1", "header_bg": "#ffffff", "qr": True},
	"barcode_enabled": {"label": "Barcode Enabled", "primary": "#111827", "accent": "#374151", "header_bg": "#ffffff", "barcode": True},
}


def _theme_base_css(theme_key: str, theme: dict) -> str:
	font_size = theme.get("font_size", "9px")
	font_family = theme.get("font_family", "Arial, Helvetica, sans-serif")
	orientation = theme.get("orientation", "portrait")
	paper = theme.get("paper", "A4")
	margin = "4mm" if theme_key == "thermal" else "8mm"

	return f"""
@page {{
	size: {paper} {orientation};
	margin: {margin};
}}
.epp-root {{
	font-family: {font_family};
	font-size: {font_size};
	color: #111;
	line-height: 1.25;
}}
.epp-primary {{ color: {theme['primary']}; }}
.epp-accent {{ color: {theme['accent']}; }}
.epp-header {{
	background: {theme['header_bg']};
	border-bottom: 2px solid {theme['primary']};
	padding: 8px 10px;
	margin-bottom: 8px;
}}
.epp-box {{
	border: 1px solid {theme['primary']};
	border-radius: 3px;
	padding: 6px 8px;
	margin-bottom: 4px;
}}
.epp-table {{
	width: 100%;
	border-collapse: collapse;
	table-layout: fixed;
}}
.epp-table th {{
	background: {theme['header_bg']};
	color: {theme['primary']};
	border: 1px solid {theme['primary']};
	padding: 4px;
	font-size: 8px;
	text-align: center;
}}
.epp-table td {{
	border: 1px solid {theme['primary']};
	padding: 4px;
	vertical-align: top;
	word-wrap: break-word;
	overflow-wrap: anywhere;
}}
.epp-totals td {{
	border: 1px solid {theme['primary']};
	padding: 4px 6px;
}}
.epp-footer {{
	margin-top: 10px;
	font-size: 8px;
	color: {theme['accent']};
}}
"""


def get_theme_css(theme_key: str) -> str:
	theme = THEME_REGISTRY.get(theme_key, THEME_REGISTRY["minimal"])
	css_path = THEMES_DIR / f"{theme_key}.css"
	if css_path.exists():
		base = css_path.read_text(encoding="utf-8")
	else:
		base = _theme_base_css(theme_key, theme)
	return with_page_fit(base)
