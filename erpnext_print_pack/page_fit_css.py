"""Shared A4 page-fit rules so print tables/sections stay within page width."""

PAGE_FIT_CSS = """
.root, .epp-root, .sp-root, .print-format {
	box-sizing: border-box;
	max-width: 100%;
	overflow-x: hidden;
	word-wrap: break-word;
	overflow-wrap: anywhere;
}
.root *, .epp-root *, .sp-root *, .print-format * {
	box-sizing: border-box;
	max-width: 100%;
}
table.items, table.epp-table, table.sp-table, table.meta, table.totals, table.epp-totals,
table.party-grid, table.vx-top {
	width: 100% !important;
	max-width: 100% !important;
	table-layout: fixed;
	border-collapse: collapse;
}
table.totals, table.epp-totals {
	width: 48% !important;
	margin-left: auto;
}
table.items th, table.items td,
table.epp-table th, table.epp-table td,
table.sp-table th, table.sp-table td {
	word-wrap: break-word;
	overflow-wrap: anywhere;
	white-space: normal;
	vertical-align: top;
	padding: 4px 5px !important;
	font-size: 9px;
}
table.items th, table.epp-table th, table.sp-table th {
	font-size: 8px;
	line-height: 1.2;
}
.party-box, .epp-box, .sp-card {
	max-width: 100%;
	overflow-wrap: anywhere;
	word-wrap: break-word;
}
img {
	max-width: 100%;
	height: auto;
}
"""
