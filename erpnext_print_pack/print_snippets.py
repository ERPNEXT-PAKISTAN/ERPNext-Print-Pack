"""Reusable Jinja snippets injected into generated print templates."""

DOC_BARCODE_SNIPPET = """
{% set _epp_doc_bc = get_doc_barcode_data_uri(doc.name) if doc.name and get_doc_barcode_data_uri is defined else "" %}
{% if _epp_doc_bc %}<div class="epp-voucher-barcode" style="margin-top:6px;text-align:center;max-width:100%;overflow:hidden"><img src="{{ _epp_doc_bc }}" alt="{{ doc.name }}" style="max-width:100%;width:auto;max-height:12mm;height:12mm;object-fit:contain;display:inline-block"></div>{% endif %}
"""

THERMAL_DOC_BARCODE_SNIPPET = """
{% set _th_bc = get_doc_barcode_data_uri(doc.name, compact=1) if doc.name and get_doc_barcode_data_uri is defined else "" %}
{% if _th_bc %}<div class="th-bc epp-voucher-barcode"><img src="{{ _th_bc }}" alt="{{ doc.name }}"></div>{% endif %}
"""

FBR_QR_SETUP = """
{% set qr_data_uri = "" %}
{% set bc_data_uri = "" %}
{% if doc.custom_fbr_invoice_no %}
  {% set payload = frappe.call("erpnext_print_pack.print_barcodes.get_qr_and_barcode_data_uri", value=doc.custom_fbr_invoice_no, include_fbr_url=1, fbr_base_url="https://fbr.gov.pk/verify") %}
  {% if payload %}
    {% set qr_data_uri = payload.get("qr") or "" %}
    {% set bc_data_uri = payload.get("barcode") or "" %}
  {% endif %}
{% endif %}
"""

FBR_DI_LOGO = "/assets/erpnext_print_pack/images/fbr_di_badge.svg"
