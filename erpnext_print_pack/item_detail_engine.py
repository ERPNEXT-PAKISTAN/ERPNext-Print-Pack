"""Item detail sheet print layout — image, valuation, barcode, purchase history."""

from __future__ import annotations

from erpnext_print_pack.print_snippets import DOC_BARCODE_SNIPPET


def render_item_detail(accent: str = "#6366f1", title: str = "Item Detail Report") -> str:
	return f"""{{# Item detail report #}}
{{% set title = "{title}" %}}
<style>
@page {{ size: A4 portrait; margin: 10mm; }}
.id-root {{ font-family: 'Segoe UI', Arial, sans-serif; font-size: 10px; color: #1f2937; }}
.id-head {{ display: flex; gap: 16px; margin-bottom: 14px; align-items: flex-start; }}
.id-img {{ width: 120px; height: 120px; border: 1px solid #e5e7eb; border-radius: 10px; object-fit: contain; background: #f9fafb; }}
.id-title {{ font-size: 26px; font-weight: 800; margin: 0 0 6px; color: {accent}; }}
.id-meta {{ color: #6b7280; line-height: 1.6; }}
.id-meta b {{ color: #111827; }}
.id-grid {{ display: flex; gap: 12px; margin: 12px 0; }}
.id-box {{ flex: 1; background: #f9fafb; border: 1px solid #e5e7eb; border-radius: 10px; padding: 10px 12px; }}
.id-box .lbl {{ font-weight: 700; color: {accent}; margin-bottom: 6px; }}
.id-table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
.id-table th {{ background: {accent}; color: #fff; padding: 7px 6px; text-align: left; font-size: 9px; }}
.id-table td {{ padding: 7px 6px; border-bottom: 1px solid #e5e7eb; font-size: 9px; }}
.r {{ text-align: right; }}
.id-bc {{ font-family: monospace; letter-spacing: 1px; font-size: 11px; }}
</style>
<div class="id-root print-format">
<div class="id-head">
  <div>
    {{% if doc.image %}}<img class="id-img" src="{{{{ doc.image }}}}" alt="{{{{ doc.item_name or doc.name }}}}">{{% else %}}<div class="id-img" style="display:flex;align-items:center;justify-content:center;color:#9ca3af">No image</div>{{% endif %}}
  </div>
  <div style="flex:1">
    <div class="id-title">{{{{ doc.item_name or doc.name }}}}</div>
    <div class="id-meta">
      Item Code <b>{{{{ doc.name }}}}</b><br>
      Item Group <b>{{{{ doc.item_group or "" }}}}</b><br>
      Stock UOM <b>{{{{ doc.stock_uom or "" }}}}</b><br>
      Standard Rate <b>{{{{ frappe.utils.fmt_money(doc.standard_rate) if doc.standard_rate else "—" }}}}</b>
    </div>
  </div>
</div>
<div class="id-grid">
  <div class="id-box"><div class="lbl">Valuation Method</div>{{{{ doc.valuation_method or "—" }}}}</div>
  <div class="id-box"><div class="lbl">Barcode</div><div class="id-bc">{{{{ doc.barcode or "" }}}}</div></div>
  <div class="id-box"><div class="lbl">Brand / Description</div>{{{{ doc.brand or "" }}}}{{% if doc.description %}}<br><span style="color:#6b7280">{{{{ doc.description }}}}</span>{{% endif %}}</div>
</div>
{{% set purchases = get_item_last_purchases(doc.name, 2) %}}
<div class="id-box" style="margin-top:4px">
  <div class="lbl">Last Two Purchases</div>
  {{% if purchases %}}
  <table class="id-table">
    <thead><tr><th>Date</th><th>Supplier</th><th class="r">Qty</th><th class="r">Rate</th></tr></thead>
    <tbody>
    {{% for row in purchases %}}
    <tr>
      <td>{{{{ frappe.utils.formatdate(row.posting_date) if row.posting_date else "" }}}}</td>
      <td>{{{{ row.supplier_name or row.supplier or "" }}}}</td>
      <td class="r">{{{{ row.qty or "" }}}} {{% if row.stock_uom %}}{{{{ row.stock_uom }}}}{{% endif %}}</td>
      <td class="r">{{{{ frappe.utils.fmt_money(row.rate) if row.rate else "" }}}}</td>
    </tr>
    {{% endfor %}}
    </tbody>
  </table>
  {{% else %}}
  <span style="color:#6b7280">No purchase history found.</span>
  {{% endif %}}
</div>
{DOC_BARCODE_SNIPPET}
</div>
"""
