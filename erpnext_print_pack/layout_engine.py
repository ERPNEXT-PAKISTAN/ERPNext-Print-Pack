"""Premium layout engine — distinct invoice designs (Google-style variety)."""

from __future__ import annotations

from erpnext_print_pack.doctype_profiles import DocTypeProfile
from erpnext_print_pack.print_snippets import DOC_BARCODE_SNIPPET

LAYOUT_REGISTRY: dict[str, dict] = {
	"vertex_classic": {
		"label": "Vertex Classic",
		"description": "Light blue headers, thin borders — Excel/Word professional",
		"sectors": ["general", "business", "trading"],
	},
	"dark_header_pro": {
		"label": "Dark Header Pro",
		"description": "Solid navy header bar, white INVOICE title",
		"sectors": ["corporate", "enterprise"],
	},
	"zoho_professional": {
		"label": "Zoho Professional",
		"description": "Clean blue theme, summary balance box",
		"sectors": ["saas", "services", "corporate"],
	},
	"orange_accent": {
		"label": "Orange Accent",
		"description": "Bold orange total bar, signature area",
		"sectors": ["retail", "wholesale", "distribution"],
	},
	"purple_tax": {
		"label": "Purple Tax Invoice",
		"description": "Formal tax invoice, purple accent, signature",
		"sectors": ["tax", "compliance", "vat"],
	},
	"modern_qr": {
		"label": "Modern QR",
		"description": "Minimal grid, QR payment block",
		"sectors": ["digital", "e-invoice", "modern"],
	},
	"yellow_sidebar": {
		"label": "Yellow Sidebar",
		"description": "Yellow accent stripe, structured metadata",
		"sectors": ["construction", "logistics", "general"],
	},
	"stripe_clean": {
		"label": "Stripe Clean",
		"description": "Zebra rows, no vertical borders, airy modern",
		"sectors": ["agency", "consulting", "professional"],
	},
}

COMMERCIAL_CATEGORIES = {"sales", "purchasing", "payments", "projects", "hr", "stock", "manufacturing"}


def format_display_name(profile: DocTypeProfile, layout_key: str) -> str:
	return f"{LAYOUT_REGISTRY[layout_key]['label']} {profile.title}"


def format_slug(profile: DocTypeProfile, layout_key: str) -> str:
	return f"{profile.slug}_{layout_key}"


def _party_vars(profile: DocTypeProfile) -> str:
	if profile.has_party_customer:
		return """
{% set party_label = "Bill To" %}
{% set ship_label = "Ship To" %}
{% set party_name = doc.customer_name or doc.customer or doc.party_name or "" %}
{% set party_address = doc.address_display or "" %}
{% set ship_address = doc.shipping_address or doc.shipping_address_display or "" %}
"""
	if profile.has_party_supplier:
		return """
{% set party_label = "Supplier" %}
{% set ship_label = "Deliver To" %}
{% set party_name = doc.supplier_name or doc.supplier or "" %}
{% set party_address = doc.address_display or doc.supplier_address or "" %}
{% set ship_address = doc.shipping_address_display or "" %}
"""
	if profile.party_field == "employee":
		return """
{% set party_label = "Employee" %}
{% set ship_label = "" %}
{% set party_name = doc.employee_name or doc.employee or "" %}
{% set party_address = "" %}
{% set ship_address = "" %}
"""
	return """
{% set party_label = "Party" %}
{% set ship_label = "" %}
{% set party_name = doc.party_name or doc.party or "" %}
{% set party_address = doc.address_display or "" %}
{% set ship_address = "" %}
"""


def _items_table(profile: DocTypeProfile) -> str:
	if not profile.has_items:
		return ""
	return """
{% if doc.items %}
<table class="items">
<thead><tr><th>#</th><th>Description</th><th class="r">Qty</th><th class="r">Rate</th><th class="r">Amount</th></tr></thead>
<tbody>
{% for row in doc.items %}
<tr>
<td>{{ loop.index }}</td>
<td><strong>{{ row.item_name or row.item_code or row.description or "" }}</strong>{% if row.description and row.description != (row.item_name or row.item_code) %}<br><small>{{ row.description }}</small>{% endif %}</td>
<td class="r">{{ row.get_formatted("qty", doc) if row.get_formatted is defined else row.qty or "" }}</td>
<td class="r">{{ row.get_formatted("rate", doc) if row.get_formatted is defined else row.rate or "" }}</td>
<td class="r">{{ row.get_formatted("amount", doc) if row.get_formatted is defined else row.amount or "" }}</td>
</tr>
{% endfor %}
</tbody>
</table>
{% endif %}
"""


def _totals_block(profile: DocTypeProfile) -> str:
	if not profile.has_items and profile.doc_type == "Payment Entry":
		return """
<table class="totals"><tr><td>Received Amount</td><td class="r">{{ doc.get_formatted("paid_amount") if doc.get_formatted is defined else doc.paid_amount or "" }}</td></tr></table>
"""
	if not profile.has_taxes:
		return """
<table class="totals">
<tr><td>Total</td><td class="r">{{ doc.get_formatted("grand_total") if doc.get_formatted is defined else doc.grand_total or doc.total or "" }}</td></tr>
</table>
"""
	return """
<table class="totals">
<tr><td>Net Total</td><td class="r">{{ doc.get_formatted("net_total") if doc.get_formatted is defined else doc.net_total or "" }}</td></tr>
{% for tax in doc.taxes or [] %}<tr><td>{{ tax.description or tax.account_head or "Tax" }}</td><td class="r">{{ tax.get_formatted("tax_amount") if tax.get_formatted is defined else tax.tax_amount or "" }}</td></tr>{% endfor %}
<tr class="grand"><td>Grand Total</td><td class="r">{{ doc.get_formatted("grand_total") if doc.get_formatted is defined else doc.grand_total or "" }}</td></tr>
</table>
"""


def _meta_header(profile: DocTypeProfile) -> str:
	due = '{% if doc.due_date %}<tr><td>Due Date</td><td class="r">{{ frappe.utils.formatdate(doc.due_date) }}</td></tr>{% endif %}' if profile.has_due_date else ""
	return f"""
<table class="meta">
<tr><td>Document</td><td class="r bold">{{{{ doc.name }}}}</td></tr>
<tr><td>Date</td><td class="r">{{{{ frappe.utils.formatdate(doc.get("{profile.date_field}")) if doc.get("{profile.date_field}") else "" }}}}</td></tr>
{due}
<tr><td>Currency</td><td class="r">{{{{ doc.currency or "" }}}}</td></tr>
</table>
"""


def render_layout(profile: DocTypeProfile, layout_key: str) -> str:
	renderers = {
		"vertex_classic": _render_vertex_classic,
		"dark_header_pro": _render_dark_header_pro,
		"zoho_professional": _render_zoho_professional,
		"orange_accent": _render_orange_accent,
		"purple_tax": _render_purple_tax,
		"modern_qr": _render_modern_qr,
		"yellow_sidebar": _render_yellow_sidebar,
		"stripe_clean": _render_stripe_clean,
	}
	return renderers[layout_key](profile)


def _base_wrap(profile: DocTypeProfile, layout_key: str, css: str, body: str) -> str:
	party = _party_vars(profile)
	items = _items_table(profile)
	totals = _totals_block(profile)
	in_words = (
		'{% if doc.in_words %}<div class="words">{{ doc.in_words }}</div>{% endif %}'
		if profile.has_in_words
		else ""
	)
	terms = (
		'{% if doc.terms %}<div class="terms"><strong>Terms</strong><br>{{ doc.terms }}</div>{% endif %}'
		if profile.has_terms
		else ""
	)
	return f"""{{# Premium layout: {layout_key} · {profile.doc_type} #}}
{{% set title = "{profile.title}" %}}
{{% set date_field = "{profile.date_field}" %}}
{party}
<style>
@page {{ size: A4 portrait; margin: 10mm; }}
.r {{ text-align: right; }}
.bold {{ font-weight: 700; }}
small {{ color: #666; font-size: 9px; }}
{css}
.print-format table > tbody > tr > td {{ padding: 5px 6px !important; }}
</style>
<div class="root print-format">
{body.replace("{{ITEMS}}", items).replace("{{TOTALS}}", totals).replace("{{META}}", _meta_header(profile)).replace("{{IN_WORDS}}", in_words).replace("{{TERMS}}", terms)}
{DOC_BARCODE_SNIPPET}
</div>
"""


def _render_vertex_classic(profile: DocTypeProfile) -> str:
	css = """
.root { font-family: Calibri, Arial, sans-serif; font-size: 10px; color: #333; }
.vx-top { width: 100%; margin-bottom: 16px; }
.vx-top td { vertical-align: top; padding: 4px; }
.vx-title { font-size: 28px; color: #2f75b5; font-weight: 700; }
.vx-co { font-size: 12px; font-weight: 700; color: #2f75b5; }
.party-box { background: #d9e2f3; border: 1px solid #9dc3e6; padding: 8px; margin-bottom: 10px; }
.party-grid td { width: 50%; vertical-align: top; padding: 4px; }
.items { width: 100%; border-collapse: collapse; margin-top: 8px; }
.items th { background: #2f75b5; color: #fff; border: 1px solid #2f75b5; padding: 6px; font-size: 9px; }
.items td { border: 1px solid #9dc3e6; padding: 5px; }
.totals { width: 42%; margin-left: auto; margin-top: 10px; border-collapse: collapse; }
.totals td { border: 1px solid #9dc3e6; padding: 5px 8px; }
.totals .grand td { background: #d9e2f3; font-weight: 700; }
.meta td { padding: 2px 0; font-size: 9px; }
.words { margin-top: 10px; font-style: italic; font-size: 9px; }
"""
	body = """
<table class="vx-top"><tr>
<td><div class="vx-co">{{ doc.company or "" }}</div><div>{{ doc.company_address_display or "" }}</div></td>
<td style="text-align:right"><div class="vx-title">{{ title }}</div>{{META}}</td>
</tr></table>
<table class="party-grid"><tr>
<td><div class="party-box"><strong>{{ party_label }}</strong><br>{{ party_name }}<br>{{ party_address }}</div></td>
<td>{% if ship_label %}<div class="party-box"><strong>{{ ship_label }}</strong><br>{{ ship_address }}</div>{% endif %}</td>
</tr></table>
{{ITEMS}}{{TOTALS}}{{IN_WORDS}}{{TERMS}}
"""
	return _base_wrap(profile, "vertex_classic", css, body)


def _render_dark_header_pro(profile: DocTypeProfile) -> str:
	css = """
.root { font-family: Arial, sans-serif; font-size: 10px; color: #333; }
.dh-band { background: #1e3a8a; color: #fff; padding: 20px 24px; margin: -2px -2px 16px; }
.dh-band .doc-title { font-size: 32px; font-weight: 300; letter-spacing: 3px; }
.dh-band .co { font-size: 11px; opacity: 0.9; margin-top: 4px; }
.dh-band .ref { text-align: right; font-size: 11px; }
.party-row td { width: 50%; padding: 8px 12px 16px 0; vertical-align: top; }
.party-row .lbl { font-size: 9px; text-transform: uppercase; color: #64748b; margin-bottom: 4px; }
.items { width: 100%; border-collapse: collapse; }
.items th { background: #1e3a8a; color: #fff; padding: 8px 6px; text-align: left; font-size: 9px; }
.items td { padding: 8px 6px; border-bottom: 1px solid #e2e8f0; }
.items tbody tr:nth-child(even) { background: #f8fafc; }
.totals { width: 40%; margin-left: auto; margin-top: 12px; }
.totals .grand td { background: #1e3a8a; color: #fff; font-size: 12px; font-weight: 700; padding: 8px; }
.totals td { padding: 5px 8px; border-bottom: 1px solid #e2e8f0; }
"""
	body = """
<div class="dh-band"><table style="width:100%"><tr>
<td><div class="doc-title">{{ title|upper }}</div><div class="co">{{ doc.company or "" }}</div></td>
<td class="ref"><div>{{ doc.name }}</div><div>{{ frappe.utils.formatdate(doc.get(date_field)) if doc.get(date_field) else "" }}</div></td>
</tr></table></div>
<table class="party-row"><tr>
<td><div class="lbl">{{ party_label }}</div><strong>{{ party_name }}</strong><br>{{ party_address }}</td>
<td>{% if ship_label %}<div class="lbl">{{ ship_label }}</div>{{ ship_address }}{% endif %}</td>
</tr></table>
{{ITEMS}}{{TOTALS}}{{IN_WORDS}}{{TERMS}}
"""
	return _base_wrap(profile, "dark_header_pro", css, body)


def _render_zoho_professional(profile: DocTypeProfile) -> str:
	css = """
.root { font-family: 'Segoe UI', sans-serif; font-size: 10px; color: #333; }
.zh { border-bottom: 3px solid #0891b2; padding-bottom: 12px; margin-bottom: 16px; }
.zh .t { font-size: 22px; color: #0891b2; font-weight: 600; }
.cards td { padding: 6px; vertical-align: top; }
.card { background: #f0fdfa; border: 1px solid #99f6e4; border-radius: 4px; padding: 10px; min-height: 60px; }
.card .lbl { font-size: 8px; color: #0d9488; text-transform: uppercase; font-weight: 600; }
.items { width: 100%; border-collapse: collapse; margin-top: 12px; }
.items th { background: #ecfeff; color: #0e7490; border-bottom: 2px solid #0891b2; padding: 8px; text-align: left; }
.items td { padding: 8px; border-bottom: 1px solid #e0f2f1; }
.summary { background: #0891b2; color: #fff; border-radius: 6px; padding: 14px 18px; width: 44%; margin-left: auto; margin-top: 14px; }
.summary table { width: 100%; color: #fff; }
.summary td { padding: 3px 0; }
.summary .bal { font-size: 16px; font-weight: 700; border-top: 1px solid rgba(255,255,255,0.3); padding-top: 8px; margin-top: 4px; }
"""
	body = """
<div class="zh"><table style="width:100%"><tr><td><div class="t">{{ title }}</div><div>{{ doc.company or "" }}</div></td><td style="text-align:right">{{META}}</td></tr></table></div>
<table class="cards" style="width:100%"><tr>
<td style="width:50%"><div class="card"><div class="lbl">{{ party_label }}</div>{{ party_name }}<br>{{ party_address }}</div></td>
<td style="width:50%"><div class="card"><div class="lbl">Company</div>{{ doc.company_address_display or "" }}{% if doc.company_tax_id %}<br>VAT: {{ doc.company_tax_id }}{% endif %}</div></td>
</tr></table>
{{ITEMS}}
<div class="summary"><table>
<tr><td>Sub Total</td><td class="r">{{ doc.get_formatted("net_total") if doc.get_formatted is defined else doc.net_total or "" }}</td></tr>
{% for tax in doc.taxes or [] %}<tr><td>{{ tax.description or "Tax" }}</td><td class="r">{{ tax.get_formatted("tax_amount") if tax.get_formatted is defined else tax.tax_amount or "" }}</td></tr>{% endfor %}
<tr class="bal"><td>Balance Due</td><td class="r">{{ doc.get_formatted("grand_total") if doc.get_formatted is defined else doc.grand_total or "" }}</td></tr>
</table></div>
{{IN_WORDS}}{{TERMS}}
"""
	return _base_wrap(profile, "zoho_professional", css, body)


def _render_orange_accent(profile: DocTypeProfile) -> str:
	css = """
.root { font-family: Arial, sans-serif; font-size: 10px; color: #333; }
.oa-head { border-left: 6px solid #ea580c; padding-left: 14px; margin-bottom: 16px; }
.oa-head h1 { margin: 0; font-size: 24px; color: #ea580c; }
.info td { padding: 6px; width: 50%; vertical-align: top; }
.items { width: 100%; border-collapse: collapse; }
.items th { background: #fff7ed; color: #c2410c; border-bottom: 2px solid #ea580c; padding: 8px; text-align: left; }
.items td { padding: 7px 8px; border-bottom: 1px solid #fed7aa; }
.oa-total { background: #ea580c; color: #fff; padding: 14px 20px; margin-top: 14px; width: 48%; margin-left: auto; border-radius: 4px; }
.oa-total table { width: 100%; color: #fff; font-size: 16px; font-weight: 700; }
.sig { margin-top: 28px; border-top: 1px solid #ccc; padding-top: 8px; width: 200px; font-size: 9px; color: #666; }
"""
	body = """
<div class="oa-head"><h1>{{ title }}</h1><div>{{ doc.company or "" }} · {{ doc.name }}</div></div>
<table class="info"><tr>
<td><strong>{{ party_label }}</strong><br>{{ party_name }}<br>{{ party_address }}</td>
<td style="text-align:right">{{META}}</td>
</tr></table>
{{ITEMS}}
<div class="oa-total"><table><tr><td>TOTAL DUE</td><td class="r">{{ doc.get_formatted("grand_total") if doc.get_formatted is defined else doc.grand_total or "" }}</td></tr></table></div>
<div class="sig">Authorized Signature ___________________</div>
{{IN_WORDS}}{{TERMS}}
"""
	return _base_wrap(profile, "orange_accent", css, body)


def _render_purple_tax(profile: DocTypeProfile) -> str:
	css = """
.root { font-family: Arial, sans-serif; font-size: 10px; color: #333; }
.pt-title { text-align: center; font-size: 20px; font-weight: 700; color: #7c3aed; border-bottom: 2px solid #7c3aed; padding-bottom: 8px; margin-bottom: 14px; }
.pt-tax-id { text-align: center; font-size: 9px; color: #666; margin-bottom: 12px; }
.pt-grid td { border: 1px solid #ddd6fe; padding: 8px; vertical-align: top; width: 50%; }
.items { width: 100%; border-collapse: collapse; margin-top: 10px; }
.items th { background: #7c3aed; color: #fff; padding: 7px; border: 1px solid #6d28d9; }
.items td { border: 1px solid #ddd6fe; padding: 6px; }
.totals { width: 45%; margin-left: auto; margin-top: 10px; }
.totals .grand td { background: #ede9fe; color: #5b21b6; font-weight: 700; }
.pt-sig { margin-top: 24px; text-align: right; }
.pt-sig .line { border-top: 1px solid #7c3aed; width: 180px; margin-left: auto; padding-top: 4px; font-size: 9px; color: #7c3aed; }
"""
	body = """
<div class="pt-title">TAX {{ title|upper }}</div>
<div class="pt-tax-id">{% if doc.company_tax_id %}Tax Reg: {{ doc.company_tax_id }}{% endif %} {% if doc.tax_id %} · Customer Tax ID: {{ doc.tax_id }}{% endif %}</div>
<table class="pt-grid" style="width:100%"><tr>
<td><strong>From:</strong> {{ doc.company or "" }}<br>{{ doc.company_address_display or "" }}</td>
<td><strong>{{ party_label }}:</strong> {{ party_name }}<br>{{ party_address }}<br>{{META}}</td>
</tr></table>
{{ITEMS}}{{TOTALS}}{{IN_WORDS}}
<div class="pt-sig"><div class="line">Authorized Signatory</div></div>
{{TERMS}}
"""
	return _base_wrap(profile, "purple_tax", css, body)


def _render_modern_qr(profile: DocTypeProfile) -> str:
	css = """
.root { font-family: system-ui, sans-serif; font-size: 10px; color: #18181b; }
.mq-top { display: table; width: 100%; margin-bottom: 16px; }
.mq-top > div { display: table-cell; vertical-align: top; }
.mq-qr { width: 90px; height: 90px; border: 2px dashed #a1a1aa; text-align: center; line-height: 90px; color: #a1a1aa; font-size: 9px; border-radius: 4px; }
.items { width: 100%; border-collapse: collapse; }
.items th { text-align: left; border-bottom: 2px solid #18181b; padding: 8px 4px; font-size: 9px; text-transform: uppercase; color: #71717a; }
.items td { padding: 10px 4px; border-bottom: 1px solid #f4f4f5; }
.mq-sum { background: #fafafa; border: 1px solid #e4e4e7; border-radius: 8px; padding: 14px; width: 46%; margin-left: auto; margin-top: 12px; }
.mq-sum .g { font-size: 18px; font-weight: 800; color: #18181b; margin-top: 6px; }
"""
	body = """
<div class="mq-top">
<div><div style="font-size:20px;font-weight:800">{{ title }}</div><div style="color:#71717a">{{ doc.company or "" }}</div><div style="margin-top:8px"><strong>{{ party_label }}:</strong> {{ party_name }}</div></div>
<div style="text-align:right"><div class="mq-qr">QR</div><div style="margin-top:6px;font-size:9px">{{ doc.name }}</div></div>
</div>
{{ITEMS}}
<div class="mq-sum">
<div>Subtotal: {{ doc.get_formatted("net_total") if doc.get_formatted is defined else doc.net_total or "" }}</div>
{% for tax in doc.taxes or [] %}<div>{{ tax.description or "Tax" }}: {{ tax.get_formatted("tax_amount") if tax.get_formatted is defined else tax.tax_amount or "" }}</div>{% endfor %}
<div class="g">Due: {{ doc.get_formatted("grand_total") if doc.get_formatted is defined else doc.grand_total or "" }}</div>
</div>
{{IN_WORDS}}{{TERMS}}
"""
	return _base_wrap(profile, "modern_qr", css, body)


def _render_yellow_sidebar(profile: DocTypeProfile) -> str:
	css = """
.root { font-family: Arial, sans-serif; font-size: 10px; color: #333; padding-left: 12px; border-left: 8px solid #eab308; min-height: 200px; }
.ys-title { font-size: 22px; font-weight: 700; color: #854d0e; margin-bottom: 4px; }
.ys-meta { background: #fefce8; border: 1px solid #fde047; padding: 10px; margin: 12px 0; border-radius: 4px; }
.ys-meta td { padding: 3px 8px; }
.items { width: 100%; border-collapse: collapse; }
.items th { background: #fef9c3; color: #854d0e; border: 1px solid #fde047; padding: 6px; }
.items td { border: 1px solid #fde047; padding: 5px; }
.totals { width: 42%; margin-left: auto; margin-top: 10px; }
.totals .grand td { background: #eab308; color: #fff; font-weight: 700; }
"""
	body = """
<div class="ys-title">{{ title }}</div>
<div>{{ doc.company or "" }}</div>
<div class="ys-meta"><table style="width:100%"><tr>
<td><strong>{{ party_label }}:</strong> {{ party_name }}<br>{{ party_address }}</td>
<td style="text-align:right">{{META}}</td>
</tr></table></div>
{{ITEMS}}{{TOTALS}}{{IN_WORDS}}{{TERMS}}
"""
	return _base_wrap(profile, "yellow_sidebar", css, body)


def _render_stripe_clean(profile: DocTypeProfile) -> str:
	css = """
.root { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 10px; color: #444; }
.sc-h { margin-bottom: 24px; }
.sc-h .t { font-size: 26px; font-weight: 300; color: #111; }
.sc-h .sub { color: #888; margin-top: 4px; }
.sc-party { margin-bottom: 20px; line-height: 1.6; }
.items { width: 100%; border-collapse: collapse; }
.items th { text-align: left; padding: 8px 4px; border-bottom: 2px solid #111; font-size: 9px; text-transform: uppercase; letter-spacing: 0.5px; color: #888; }
.items td { padding: 10px 4px; border-bottom: 1px solid #eee; }
.items tbody tr:nth-child(even) { background: #fafafa; }
.totals { width: 38%; margin-left: auto; margin-top: 16px; }
.totals td { padding: 6px 4px; border: none; }
.totals .grand td { border-top: 2px solid #111; font-size: 14px; font-weight: 700; color: #111; padding-top: 10px; }
"""
	body = """
<div class="sc-h"><div class="t">{{ title }}</div><div class="sub">{{ doc.company or "" }} · {{ doc.name }} · {{ frappe.utils.formatdate(doc.get(date_field)) if doc.get(date_field) else "" }}</div></div>
<div class="sc-party"><strong>{{ party_label }}</strong><br>{{ party_name }}<br>{{ party_address }}</div>
{{ITEMS}}{{TOTALS}}{{IN_WORDS}}{{TERMS}}
"""
	return _base_wrap(profile, "stripe_clean", css, body)
