"""Shared A4 page-fit rules so print tables/sections stay within page width.

Avoids letter-stacking (vertical one-char lines) by not forcing max-width on every
descendant and by wrapping on word boundaries only.
"""

PAGE_FIT_MARKER = "/* epp-page-fit */"

PAGE_FIT_CSS = """
/* epp-page-fit */
.root, .epp-root, .sp-root, .print-format {
	box-sizing: border-box;
	max-width: 100%;
	overflow-x: hidden;
	word-wrap: break-word;
	overflow-wrap: break-word;
	word-break: normal;
}
.root *, .epp-root *, .sp-root *, .print-format * {
	box-sizing: border-box;
}
img, svg, video, canvas {
	max-width: 100%;
	height: auto;
}
table.items, table.epp-table, table.sp-table,
table.party-grid, table.vx-top {
	width: 100% !important;
	max-width: 100% !important;
	table-layout: fixed;
	border-collapse: collapse;
}
table.meta {
	width: auto !important;
	max-width: 100% !important;
	table-layout: auto;
	border-collapse: collapse;
}
table.meta td {
	white-space: nowrap;
	padding: 2px 6px !important;
	word-break: normal;
	overflow-wrap: normal;
}
table.meta td.r, table.meta td:last-child {
	white-space: normal;
	word-break: normal;
	overflow-wrap: break-word;
}
table.totals, table.epp-totals {
	width: 48% !important;
	max-width: 100% !important;
	margin-left: auto;
	table-layout: auto;
	border-collapse: collapse;
}
table.items th, table.items td,
table.epp-table th, table.epp-table td,
table.sp-table th, table.sp-table td {
	word-wrap: break-word;
	overflow-wrap: break-word;
	word-break: normal;
	white-space: normal;
	vertical-align: top;
	padding: 4px 5px !important;
	font-size: 9px;
	hyphens: manual;
}
table.items th, table.epp-table th, table.sp-table th {
	font-size: 8px;
	line-height: 1.25;
	white-space: normal;
	word-break: normal;
}
.party-box, .epp-box, .sp-card, .ys-meta, .dh-band, .vx-title, .ys-title {
	max-width: 100%;
	overflow-wrap: break-word;
	word-wrap: break-word;
	word-break: normal;
}
.epp-voucher-barcode, .th-bc {
	max-width: 100%;
	overflow: hidden;
	text-align: center;
}
.epp-voucher-barcode img {
	max-width: 100% !important;
	width: auto !important;
	max-height: 12mm;
	height: 12mm;
	object-fit: contain;
}
"""


def strip_page_fit(css: str) -> str:
	"""Remove previously appended page-fit blocks (old or marked)."""
	if PAGE_FIT_MARKER in css:
		return css.split(PAGE_FIT_MARKER, 1)[0].rstrip()
	# Legacy block started with this selector trio after first page-fit ship.
	legacy = "\n.root, .epp-root, .sp-root, .print-format {"
	if legacy in css and "overflow-wrap: anywhere" in css:
		return css.split(legacy, 1)[0].rstrip()
	if "overflow-wrap: anywhere" in css and ".root, .epp-root, .sp-root, .print-format" in css:
		idx = css.find(".root, .epp-root, .sp-root, .print-format")
		if idx > 0:
			return css[:idx].rstrip()
	return css.rstrip()


def with_page_fit(css: str) -> str:
	return f"{strip_page_fit(css)}\n{PAGE_FIT_CSS}"
