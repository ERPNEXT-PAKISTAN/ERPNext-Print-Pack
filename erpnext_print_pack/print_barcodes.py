"""QR and barcode helpers for print formats (FBR Pakistan + ERPNext voucher barcodes)."""

from __future__ import annotations

import base64
from io import BytesIO

import frappe


@frappe.whitelist()
def get_qr_and_barcode_data_uri(
	value: str,
	include_fbr_url: int = 0,
	fbr_base_url: str | None = None,
	module_width: float | None = None,
	module_height: float | None = None,
	dpi: int | None = None,
):
	"""Return PDF-safe data URIs for QR and Code128 barcode images."""
	value = (value or "").strip()
	if not value:
		return {"qr": "", "barcode": ""}

	include_fbr_url = int(include_fbr_url or 0)
	if include_fbr_url:
		base = (fbr_base_url or "https://fbr.gov.pk/verify").strip()
		sep = "&" if "?" in base else "?"
		qr_payload = f"{base}{sep}invoice={value}"
	else:
		qr_payload = value

	mw = float(module_width) if module_width is not None else 0.32
	mh = float(module_height) if module_height is not None else 16.0
	d = int(dpi) if dpi is not None else 203

	qr_png = _make_qr_png(qr_payload)
	bc_png = _make_code128_png(value, module_width=mw, module_height=mh, dpi=d)

	return {
		"qr": "data:image/png;base64," + base64.b64encode(qr_png).decode("utf-8"),
		"barcode": "data:image/png;base64," + base64.b64encode(bc_png).decode("utf-8"),
	}


@frappe.whitelist()
def get_doc_barcode_data_uri(value: str, module_width: float | None = None, module_height: float | None = None):
	"""Code128 barcode for ERPNext document name (voucher number)."""
	value = (value or "").strip()
	if not value:
		return ""
	mw = float(module_width) if module_width is not None else 0.28
	mh = float(module_height) if module_height is not None else 12.0
	png = _make_code128_png(value, module_width=mw, module_height=mh, dpi=203)
	return "data:image/png;base64," + base64.b64encode(png).decode("utf-8")


def _make_qr_png(data: str) -> bytes:
	import qrcode
	from PIL import Image

	qr = qrcode.QRCode(
		version=None,
		error_correction=qrcode.constants.ERROR_CORRECT_M,
		box_size=8,
		border=2,
	)
	qr.add_data(data)
	qr.make(fit=True)
	img = qr.make_image(fill_color="black", back_color="white")
	if not isinstance(img, Image.Image):
		img = img.get_image()
	buf = BytesIO()
	img.save(buf, format="PNG")
	return buf.getvalue()


def _make_code128_png(data: str, module_width: float, module_height: float, dpi: int) -> bytes:
	import barcode
	from barcode.writer import ImageWriter

	code128 = barcode.get("code128", data, writer=ImageWriter())
	buf = BytesIO()
	code128.write(
		buf,
		options={
			"module_width": module_width,
			"module_height": module_height,
			"quiet_zone": 2.0,
			"write_text": False,
			"font_size": 0,
			"dpi": dpi,
		},
	)
	return buf.getvalue()
