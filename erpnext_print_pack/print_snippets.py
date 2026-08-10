"""Reusable Jinja snippets injected into generated print templates."""

DOC_BARCODE_SNIPPET = """
{% set _epp_doc_bc = get_doc_barcode_data_uri(doc.name) if doc.name and get_doc_barcode_data_uri is defined else "" %}
{% if _epp_doc_bc %}<div class="epp-voucher-barcode" style="margin-top:6px;text-align:right"><img src="{{ _epp_doc_bc }}" alt="{{ doc.name }}" style="max-width:180px;height:14mm;display:inline-block"></div>{% endif %}
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
