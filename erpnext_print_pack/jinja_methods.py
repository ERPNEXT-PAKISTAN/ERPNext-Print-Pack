"""Shared Jinja helpers available in print templates as print_helpers()."""

from __future__ import annotations


def print_helpers():
	return {
		"safe": _safe,
		"money": _money,
	}


def _safe(value, default=""):
	return default if value is None else value


def _money(value, precision=2):
	try:
		return f"{float(value or 0):,.{precision}f}"
	except (TypeError, ValueError):
		return "0.00"
