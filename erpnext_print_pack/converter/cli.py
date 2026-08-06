from erpnext_print_pack.converter import convert


def run(input_path: str, doc_type: str, name: str, source_url: str | None = None, source_license: str = "MIT"):
	result = convert(input_path, doc_type, name, source_url, source_license)
	print("Conversion completed")
	print(f"Status: {result.status}")
	print("Warnings:", *result.warnings[:20], sep="\n- ")
	print(f"Generated folder: {result.output_dir}")
	print("Required manual checks:")
	for check in result.manual_checks:
		print(f"- {check}")
	return result
