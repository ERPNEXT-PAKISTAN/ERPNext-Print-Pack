"""Regional & colorful invoice layouts — Saudi, UAE, Pakistan, India, USA, ME."""

from __future__ import annotations

from erpnext_print_pack.detail_blocks import remarks_block
from erpnext_print_pack.doctype_profiles import DocTypeProfile
from erpnext_print_pack.layout_engine import _base_wrap, _items_table, _meta_header, _totals_block


def _regional_wrap(profile: DocTypeProfile, key: str, css: str, body: str) -> str:
	items = _items_table(profile)
	totals = _totals_block(profile)
	in_words = (
		'{% if doc.in_words %}<div class="epp-words words">{{ doc.in_words }}</div>{% endif %}'
		if profile.has_in_words
		else ""
	)
	terms = (
		'{% if doc.terms %}<div class="epp-terms terms"><strong>Terms</strong><br>{{ doc.terms }}</div>{% endif %}'
		if profile.has_terms
		else ""
	)
	remarks = remarks_block(profile)
	sig = '<div class="epp-sig sig">Authorized Signature _________________________</div>'
	footer = '<div class="epp-footer footer">Thank you for your business</div>'
	# Ensure remarks render above the footer; _base_wrap fills {{REMARKS}}.
	if "{{REMARKS}}" not in body and "{{FOOTER}}" in body:
		body = body.replace("{{FOOTER}}", "{{REMARKS}}{{FOOTER}}")
	elif "{{REMARKS}}" not in body:
		body = body + "{{REMARKS}}"
	html = _base_wrap(profile, key, css, body)
	return (
		html.replace("{{ITEMS}}", items)
		.replace("{{TOTALS}}", totals)
		.replace("{{META}}", _meta_header(profile))
		.replace("{{IN_WORDS}}", in_words)
		.replace("{{TERMS}}", terms)
		.replace("{{REMARKS}}", remarks)
		.replace("{{SIG}}", sig)
		.replace("{{FOOTER}}", footer)
	)


def render_saudi_zatca(profile: DocTypeProfile) -> str:
	css = """
.root { font-family: Arial, sans-serif; font-size: 10px; color: #1a1a1a; }
.sa-band { background: linear-gradient(90deg, #006c35 0%, #004d26 100%); color: #fff; padding: 16px 20px; }
.sa-band .en { font-size: 18px; font-weight: 700; }
.sa-band .ar { direction: rtl; font-size: 16px; opacity: 0.95; }
.sa-vat { background: #f0fdf4; border: 2px solid #006c35; padding: 8px 12px; margin: 12px 0; border-radius: 4px; }
.sa-grid td { width: 50%; vertical-align: top; padding: 8px; border: 1px solid #bbf7d0; }
.sa-qr { width: 100px; height: 100px; border: 2px dashed #006c35; text-align: center; line-height: 100px; color: #006c35; font-size: 9px; border-radius: 4px; }
.items { width: 100%; border-collapse: collapse; margin-top: 10px; }
.items th { background: #006c35; color: #fff; padding: 7px; border: 1px solid #004d26; }
.items td { border: 1px solid #bbf7d0; padding: 6px; }
.totals { width: 46%; margin-left: auto; margin-top: 10px; }
.totals .grand td { background: #006c35; color: #fff; font-weight: 700; }
.epp-sig { margin-top: 20px; font-size: 9px; color: #666; }
.epp-footer { margin-top: 12px; text-align: center; color: #006c35; font-size: 9px; }
"""
	body = """
<div class="sa-band"><table style="width:100%"><tr>
<td><div class="en">TAX INVOICE · {{ title }}</div><div class="ar">فاتورة ضريبية</div></td>
<td style="text-align:right"><div>{{ doc.company or "" }}</div><div>{{ doc.name }}</div></td>
</tr></table></div>
<div class="sa-vat">
	VAT Reg: {{ doc.company_tax_id or "" }} &nbsp;|&nbsp; Customer VAT: {{ doc.tax_id or "" }}
	{% if doc.get("custom_company_cr_number") %} &nbsp;|&nbsp; CR: {{ doc.custom_company_cr_number }}{% endif %}
</div>
<table class="sa-grid" style="width:100%"><tr>
<td><strong>Seller / البائع</strong><br>{{ doc.company or "" }}<br>{{ doc.company_address_display or "" }}</td>
<td style="text-align:right"><strong>Buyer / المشتري</strong><br>{{ party_name }}<br>{{ party_address }}<br>{{META}}</td>
</tr></table>
<div style="float:right" class="sa-qr epp-qr qr">{% set qr = doc.get("ksa_einv_qr") or doc.get("custom_qr_code") or "" %}{% if qr %}<img src="{{ qr }}" style="width:96px;height:96px">{% else %}ZATCA QR{% endif %}</div>
<div style="clear:both">{{ITEMS}}{{TOTALS}}{{IN_WORDS}}{{SIG}}{{TERMS}}{{FOOTER}}</div>
"""
	return _regional_wrap(profile, "saudi_zatca", css, body)


def render_uae_vat(profile: DocTypeProfile) -> str:
	css = """
.root { font-family: 'Segoe UI', Arial, sans-serif; font-size: 10px; color: #333; }
.uae-stripe { height: 6px; background: linear-gradient(90deg, #00732f 33%, #fff 33%, #fff 66%, #ff0000 66%); margin-bottom: 12px; }
.uae-head { border-bottom: 3px solid #00732f; padding-bottom: 12px; margin-bottom: 14px; }
.uae-head h1 { margin: 0; color: #00732f; font-size: 22px; }
.uae-trn { background: #ecfdf5; border-left: 4px solid #00732f; padding: 8px 12px; margin-bottom: 12px; }
.uae-cols td { width: 50%; padding: 10px; vertical-align: top; background: #f8fafc; border: 1px solid #e2e8f0; }
.items { width: 100%; border-collapse: collapse; }
.items th { background: #00732f; color: #fff; padding: 8px; }
.items td { padding: 7px; border-bottom: 1px solid #e2e8f0; }
.totals { width: 44%; margin-left: auto; margin-top: 12px; background: #00732f; color: #fff; padding: 12px; border-radius: 4px; }
.totals td { color: #fff; padding: 4px 0; border: none; }
.totals .grand td { font-size: 14px; font-weight: 700; border-top: 1px solid rgba(255,255,255,0.3); padding-top: 8px; }
"""
	body = """
<div class="uae-stripe"></div>
<div class="uae-head"><h1>Tax Invoice — {{ title }}</h1><div>{{ doc.company or "" }} · {{ doc.name }}</div></div>
<div class="uae-trn"><strong>TRN:</strong> {{ doc.company_tax_id or "" }} &nbsp; <strong>Customer TRN:</strong> {{ doc.tax_id or "" }}</div>
<table style="width:100%"><tr class="uae-cols">
<td><strong>Supplier</strong><br>{{ doc.company_address_display or "" }}</td>
<td><strong>{{ party_label }}</strong><br>{{ party_name }}<br>{{ party_address }}</td>
</tr></table>
{{ITEMS}}
<table class="totals"><tr class="grand"><td>Total incl. VAT</td><td class="r">{{ doc.get_formatted("grand_total") if doc.get_formatted is defined else doc.grand_total or "" }}</td></tr></table>
{{IN_WORDS}}{{SIG}}{{TERMS}}{{FOOTER}}
"""
	return _regional_wrap(profile, "uae_vat", css, body)


def render_pakistan_fbr(profile: DocTypeProfile) -> str:
	css = """
.root { font-family: Arial, sans-serif; font-size: 10px; color: #1a1a1a; }
.pk-flag { background: linear-gradient(180deg, #01411c 0%, #01411c 40%, #fff 40%, #fff 60%, #01411c 60%); height: 8px; margin-bottom: 10px; border-radius: 2px; }
.pk-title { color: #01411c; font-size: 20px; font-weight: 800; border-bottom: 3px solid #01411c; padding-bottom: 6px; }
.pk-tax { background: #f0fdf4; border: 1px solid #86efac; padding: 8px; margin: 10px 0; border-radius: 4px; }
.pk-tax td { padding: 3px 10px; font-size: 9px; }
.items { width: 100%; border-collapse: collapse; }
.items th { background: #01411c; color: #fff; padding: 7px; }
.items td { border: 1px solid #bbf7d0; padding: 6px; }
.totals { width: 45%; margin-left: auto; margin-top: 10px; }
.totals .grand td { background: #01411c; color: #fff; font-weight: 700; font-size: 12px; }
"""
	body = """
<div class="pk-flag"></div>
<div class="pk-title">{{ title }} — Sales Tax Invoice</div>
<table class="pk-tax" style="width:100%"><tr>
<td><strong>NTN:</strong> {{ doc.company_tax_id or "" }}</td>
<td><strong>STRN:</strong> {{ doc.tax_id or "" }}</td>
<td><strong>Invoice #:</strong> {{ doc.name }}</td>
</tr></table>
<table style="width:100%;margin-bottom:10px"><tr>
<td style="width:50%"><strong>Seller:</strong> {{ doc.company or "" }}<br>{{ doc.company_address_display or "" }}</td>
<td style="width:50%"><strong>Buyer:</strong> {{ party_name }}<br>{{ party_address }}{{META}}</td>
</tr></table>
{{ITEMS}}{{TOTALS}}{{IN_WORDS}}{{SIG}}{{TERMS}}{{FOOTER}}
"""
	return _regional_wrap(profile, "pakistan_fbr", css, body)


def render_india_gst(profile: DocTypeProfile) -> str:
	css = """
.root { font-family: Arial, sans-serif; font-size: 10px; color: #333; }
.in-head { background: linear-gradient(135deg, #ff9933 0%, #fff 50%, #138808 100%); padding: 3px; margin-bottom: 12px; border-radius: 4px; }
.in-inner { background: #fff; padding: 12px 16px; border-radius: 3px; }
.in-title { font-size: 18px; font-weight: 700; color: #138808; }
.in-gst { background: #fff7ed; border: 1px solid #fdba74; padding: 8px; margin: 10px 0; font-size: 9px; }
.items { width: 100%; border-collapse: collapse; font-size: 9px; }
.items th { background: #138808; color: #fff; padding: 6px 4px; }
.items td { border: 1px solid #ddd; padding: 5px 4px; }
.totals { width: 48%; margin-left: auto; margin-top: 10px; }
.totals .grand td { background: #ff9933; color: #fff; font-weight: 700; }
"""
	body = """
<div class="in-head"><div class="in-inner">
<div class="in-title">GST {{ title }}</div>
<div>{{ doc.company or "" }} · {{ doc.name }} · {{ frappe.utils.formatdate(doc.get(date_field)) if doc.get(date_field) else "" }}</div>
</div></div>
<div class="in-gst">
	<strong>Supplier GSTIN:</strong> {{ doc.company_tax_id or "" }} &nbsp;|&nbsp;
	<strong>Customer GSTIN:</strong> {{ doc.tax_id or "" }} &nbsp;|&nbsp;
	<strong>Place of Supply:</strong> {{ doc.place_of_supply or "" }}
</div>
<table style="width:100%;margin-bottom:8px"><tr>
<td><strong>Bill To:</strong> {{ party_name }}<br>{{ party_address }}</td>
<td style="text-align:right">{{META}}</td>
</tr></table>
{% if doc.items %}<table class="items"><thead><tr><th>#</th><th>Item</th><th>HSN</th><th class="r">Qty</th><th class="r">Rate</th><th class="r">Tax</th><th class="r">Amount</th></tr></thead><tbody>
{% for row in doc.items %}<tr><td>{{ loop.index }}</td><td>{{ row.item_name or row.item_code or "" }}</td><td>{{ row.gst_hsn_code or row.custom_hsn_code or "" }}</td><td class="r">{{ row.qty or "" }}</td><td class="r">{{ row.rate or "" }}</td><td class="r">{{ row.item_tax_rate or "" }}</td><td class="r">{{ row.amount or "" }}</td></tr>{% endfor %}
</tbody></table>{% endif %}
{{TOTALS}}{{IN_WORDS}}{{SIG}}{{TERMS}}{{FOOTER}}
"""
	return _regional_wrap(profile, "india_gst", css, body.replace("{{ITEMS}}", ""))


def render_usa_commercial(profile: DocTypeProfile) -> str:
	css = """
.root { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 10px; color: #1e293b; }
.us-bar { background: #1e3a8a; height: 4px; margin-bottom: 2px; }
.us-bar2 { background: #dc2626; height: 4px; margin-bottom: 16px; }
.us-co { font-size: 24px; font-weight: 700; color: #1e3a8a; }
.us-inv { font-size: 14px; color: #64748b; text-transform: uppercase; letter-spacing: 2px; }
.us-box { background: #f1f5f9; border-radius: 6px; padding: 12px; margin-bottom: 14px; }
.items { width: 100%; border-collapse: collapse; }
.items th { background: #1e3a8a; color: #fff; padding: 8px; text-align: left; }
.items td { padding: 8px; border-bottom: 1px solid #e2e8f0; }
.us-due { background: #dc2626; color: #fff; padding: 14px 20px; border-radius: 6px; width: 46%; margin-left: auto; margin-top: 14px; font-size: 16px; font-weight: 700; text-align: right; }
"""
	body = """
<div class="us-bar"></div><div class="us-bar2"></div>
<table style="width:100%;margin-bottom:14px"><tr>
<td><div class="us-co">{{ doc.company or "" }}</div><div class="us-inv">{{ title }}</div></td>
<td style="text-align:right"><div style="font-size:16px;font-weight:700">{{ doc.name }}</div><div>{{ frappe.utils.formatdate(doc.get(date_field)) if doc.get(date_field) else "" }}</div>{% if doc.due_date %}<div>Due: {{ frappe.utils.formatdate(doc.due_date) }}</div>{% endif %}</td>
</tr></table>
<div class="us-box"><strong>Bill To:</strong> {{ party_name }}<br>{{ party_address }}</div>
{{ITEMS}}
<div class="us-due">Amount Due: {{ doc.get_formatted("grand_total") if doc.get_formatted is defined else doc.grand_total or "" }}</div>
{{IN_WORDS}}{{SIG}}{{TERMS}}{{FOOTER}}
"""
	return _regional_wrap(profile, "usa_commercial", css, body.replace("{{TOTALS}}", ""))


def render_gulf_gold(profile: DocTypeProfile) -> str:
	css = """
.root { font-family: Georgia, serif; font-size: 10px; color: #1a1a1a; }
.gf-frame { border: 3px double #b8860b; padding: 16px; }
.gf-head { text-align: center; border-bottom: 2px solid #b8860b; padding-bottom: 12px; margin-bottom: 14px; }
.gf-head h1 { color: #b8860b; font-size: 22px; margin: 0; letter-spacing: 3px; }
.gf-ar { direction: rtl; color: #8b6914; font-size: 14px; margin-top: 4px; }
.gf-party td { width: 50%; padding: 10px; border: 1px solid #fde68a; background: #fffbeb; vertical-align: top; }
.items { width: 100%; border-collapse: collapse; }
.items th { background: #b8860b; color: #fff; padding: 7px; }
.items td { border: 1px solid #fde68a; padding: 6px; }
.totals { width: 45%; margin-left: auto; margin-top: 10px; }
.totals .grand td { background: #b8860b; color: #fff; font-weight: 700; }
"""
	body = """
<div class="gf-frame">
<div class="gf-head"><h1>{{ title|upper }}</h1><div class="gf-ar">فاتورة</div><div style="margin-top:6px">{{ doc.company or "" }}</div></div>
<table style="width:100%"><tr class="gf-party">
<td><strong>From</strong><br>{{ doc.company_address_display or "" }}<br>VAT: {{ doc.company_tax_id or "" }}</td>
<td><strong>{{ party_label }}</strong><br>{{ party_name }}<br>{{ party_address }}</td>
</tr></table>
{{ITEMS}}{{TOTALS}}{{IN_WORDS}}{{SIG}}{{TERMS}}{{FOOTER}}
</div>
"""
	return _regional_wrap(profile, "gulf_gold", css, body)


def render_gradient_vivid(profile: DocTypeProfile) -> str:
	css = """
.root { font-family: system-ui, sans-serif; font-size: 10px; color: #333; }
.gv-hero { background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f953c6 100%); color: #fff; padding: 20px 24px; border-radius: 8px; margin-bottom: 16px; }
.gv-hero h1 { margin: 0; font-size: 24px; font-weight: 800; }
.gv-card { background: linear-gradient(180deg, #faf5ff 0%, #fff 100%); border: 1px solid #e9d5ff; border-radius: 8px; padding: 12px; margin-bottom: 12px; }
.items { width: 100%; border-collapse: collapse; }
.items th { background: linear-gradient(90deg, #667eea, #764ba2); color: #fff; padding: 8px; }
.items td { padding: 8px; border-bottom: 1px solid #f3e8ff; }
.gv-total { background: linear-gradient(90deg, #f953c6, #b91cfc); color: #fff; padding: 14px 20px; border-radius: 8px; width: 48%; margin-left: auto; margin-top: 12px; font-size: 16px; font-weight: 800; text-align: right; }
"""
	body = """
<div class="gv-hero"><h1>{{ title }}</h1><div>{{ doc.company or "" }} · {{ doc.name }}</div></div>
<div class="gv-card"><strong>{{ party_label }}:</strong> {{ party_name }}<br>{{ party_address }}{{META}}</div>
{{ITEMS}}
<div class="gv-total">TOTAL {{ doc.get_formatted("grand_total") if doc.get_formatted is defined else doc.grand_total or "" }}</div>
{{IN_WORDS}}{{SIG}}{{TERMS}}{{FOOTER}}
"""
	return _regional_wrap(profile, "gradient_vivid", css, body.replace("{{TOTALS}}", ""))


def render_emerald_fresh(profile: DocTypeProfile) -> str:
	css = """
.root { font-family: Arial, sans-serif; font-size: 10px; }
.em-head { background: #059669; color: #fff; padding: 16px 20px; border-radius: 0 0 20px 20px; margin: -2px -2px 14px; }
.items { width: 100%; border-collapse: collapse; }
.items th { background: #10b981; color: #fff; padding: 7px; }
.items td { padding: 6px; border-bottom: 2px solid #d1fae5; }
.em-total { background: #059669; color: #fff; padding: 12px 18px; border-radius: 20px; width: 44%; margin-left: auto; margin-top: 12px; font-weight: 700; text-align: right; }
"""
	body = """
<div class="em-head"><div style="font-size:20px;font-weight:700">{{ title }}</div><div>{{ doc.company or "" }}</div></div>
<p><strong>{{ party_label }}:</strong> {{ party_name }} — {{ party_address }}</p>
{{ITEMS}}<div class="em-total">Total: {{ doc.get_formatted("grand_total") if doc.get_formatted is defined else doc.grand_total or "" }}</div>
{{IN_WORDS}}{{SIG}}{{TERMS}}{{FOOTER}}
"""
	return _regional_wrap(profile, "emerald_fresh", css, body.replace("{{TOTALS}}", ""))


def render_crimson_shop(profile: DocTypeProfile) -> str:
	css = """
.root { font-family: Impact, Arial Black, sans-serif; font-size: 11px; color: #111; }
.cr-banner { background: #dc2626; color: #fff; text-align: center; padding: 14px; font-size: 22px; letter-spacing: 2px; }
.cr-sub { background: #fef2f2; padding: 10px; text-align: center; border-bottom: 3px solid #dc2626; margin-bottom: 12px; font-family: Arial; font-size: 10px; }
.items { width: 100%; font-family: Arial; border-collapse: collapse; }
.items th { background: #dc2626; color: #fff; padding: 8px; }
.items td { padding: 7px; border-bottom: 1px solid #fecaca; }
.cr-big { background: #991b1b; color: #fff; font-size: 22px; text-align: center; padding: 16px; margin-top: 14px; border-radius: 4px; }
"""
	body = """
<div class="cr-banner">{{ doc.company or "SHOP"|upper }}</div>
<div class="cr-sub">{{ title }} #{{ doc.name }} · {{ frappe.utils.formatdate(doc.get(date_field)) if doc.get(date_field) else "" }} · {{ party_name }}</div>
{{ITEMS}}
<div class="cr-big">PAY {{ doc.get_formatted("grand_total") if doc.get_formatted is defined else doc.grand_total or "" }}</div>
{{IN_WORDS}}{{SIG}}{{FOOTER}}
"""
	return _regional_wrap(profile, "crimson_shop", css, body.replace("{{TOTALS}}", "").replace("{{TERMS}}", ""))


def render_ocean_vibrant(profile: DocTypeProfile) -> str:
	css = """
.root { font-family: 'Trebuchet MS', sans-serif; font-size: 10px; color: #0c4a6e; }
.oc-wave { background: linear-gradient(180deg, #0ea5e9 0%, #0284c7 100%); color: #fff; padding: 18px 22px; margin-bottom: 20px; }
.oc-wave h1 { margin: 0; font-size: 26px; }
.oc-bubble { background: #e0f2fe; border-radius: 12px; padding: 12px 16px; margin-bottom: 12px; border: 2px solid #7dd3fc; }
.items { width: 100%; border-collapse: collapse; }
.items th { background: #0284c7; color: #fff; padding: 8px; }
.items td { padding: 8px; background: #f0f9ff; border-bottom: 1px solid #bae6fd; }
.oc-sum { background: #0369a1; color: #fff; border-radius: 12px; padding: 14px 20px; width: 46%; margin-left: auto; margin-top: 14px; text-align: right; font-size: 15px; font-weight: 700; }
"""
	body = """
<div class="oc-wave"><h1>{{ title }}</h1><div>{{ doc.company or "" }}</div></div>
<div class="oc-bubble"><strong>{{ party_label }}:</strong> {{ party_name }}<br>{{ party_address }}{{META}}</div>
{{ITEMS}}{{TOTALS}}
<div class="oc-sum">Balance: {{ doc.get_formatted("grand_total") if doc.get_formatted is defined else doc.grand_total or "" }}</div>
{{IN_WORDS}}{{SIG}}{{TERMS}}{{FOOTER}}
"""
	return _regional_wrap(profile, "ocean_vibrant", css, body.replace("{{TOTALS}}", ""))


REGIONAL_LAYOUT_REGISTRY = {
	"saudi_zatca": {"label": "Saudi ZATCA", "region": "SA", "description": "Saudi tax invoice — green, Arabic, VAT, QR"},
	"uae_vat": {"label": "UAE VAT", "region": "AE", "description": "UAE TRN tax invoice — flag colors"},
	"pakistan_fbr": {"label": "Pakistan FBR", "region": "PK", "description": "Pakistan NTN/STRN sales tax invoice"},
	"india_gst": {"label": "India GST", "region": "IN", "description": "India GSTIN, HSN, tax ready"},
	"usa_commercial": {"label": "USA Commercial", "region": "US", "description": "American red/blue stripe invoice"},
	"gulf_gold": {"label": "Gulf Gold", "region": "ME", "description": "Middle East gold bilingual luxury"},
	"gradient_vivid": {"label": "Gradient Vivid", "region": "ALL", "description": "Colorful purple-pink gradient"},
	"emerald_fresh": {"label": "Emerald Fresh", "region": "ALL", "description": "Bright green modern"},
	"crimson_shop": {"label": "Crimson Shop", "region": "ALL", "description": "Bold red retail"},
	"ocean_vibrant": {"label": "Ocean Vibrant", "region": "ALL", "description": "Bright cyan ocean theme"},
}

REGIONAL_RENDERERS = {
	"saudi_zatca": render_saudi_zatca,
	"uae_vat": render_uae_vat,
	"pakistan_fbr": render_pakistan_fbr,
	"india_gst": render_india_gst,
	"usa_commercial": render_usa_commercial,
	"gulf_gold": render_gulf_gold,
	"gradient_vivid": render_gradient_vivid,
	"emerald_fresh": render_emerald_fresh,
	"crimson_shop": render_crimson_shop,
	"ocean_vibrant": render_ocean_vibrant,
}

REGIONAL_CATEGORIES = {"sales", "purchasing"}

COLORFUL_LAYOUT_KEYS = [
	"gradient_vivid",
	"emerald_fresh",
	"crimson_shop",
	"ocean_vibrant",
]


def render_layout_regional(profile: DocTypeProfile, layout_key: str) -> str:
	return REGIONAL_RENDERERS[layout_key](profile)
