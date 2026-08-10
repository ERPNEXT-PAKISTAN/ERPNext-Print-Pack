frappe.pages["print-format-browser"].on_page_load = function (wrapper) {
	const page = frappe.ui.make_app_page({
		parent: wrapper,
		title: __("Print Format Browser"),
		single_column: true,
	});

	new erpnext_print_pack.PrintFormatBrowser(page);
};

frappe.provide("erpnext_print_pack");

erpnext_print_pack.PrintFormatBrowser = class PrintFormatBrowser {
	constructor(page) {
		this.page = page;
		this.wrapper = $(page.body);
		this.formats = [];
		this.selected_format = null;
		this.current_doc = null;
		this._preview_req = null;
		this.view_toggles = {
			words: 1,
			sig: 1,
			terms: 1,
			footer: 1,
			qr: 1,
		};
		this.make();
		this.load_doctypes();
	}

	make() {
		this.wrapper.html(`
			<div class="epp-browser-layout">
				<div class="epp-browser-toolbar"></div>
				<div class="epp-browser-body">
					<div class="epp-format-list">
						<div class="epp-format-list-header">${__("Print Formats")}</div>
						<div class="epp-format-items"></div>
					</div>
					<div class="epp-preview-panel">
						<div class="epp-preview-actions"></div>
						<div class="epp-preview-message"></div>
						<div class="epp-preview-frame-wrap">
							<iframe class="epp-preview-iframe" frameborder="0" scrolling="auto"></iframe>
						</div>
					</div>
				</div>
			</div>
		`);

		this.$toolbar = this.wrapper.find(".epp-browser-toolbar");
		this.$format_items = this.wrapper.find(".epp-format-items");
		this.$format_header = this.wrapper.find(".epp-format-list-header");
		this.$preview_actions = this.wrapper.find(".epp-preview-actions");
		this.$preview_message = this.wrapper.find(".epp-preview-message");
		this.$iframe = this.wrapper.find(".epp-preview-iframe");

		this.setup_toolbar();
		this.setup_actions();
		this.setup_iframe();
	}

	setup_toolbar() {
		this.doc_type_field = frappe.ui.form.make_control({
			parent: this.$toolbar.get(0),
			df: {
				fieldtype: "Select",
				fieldname: "doc_type",
				label: __("Document Type"),
				options: [],
				change: () => this.on_doctype_change(),
			},
			render_input: true,
		});

		this.document_field = frappe.ui.form.make_control({
			parent: this.$toolbar.get(0),
			df: {
				fieldtype: "Link",
				fieldname: "document",
				label: __("Sample Document"),
				options: "Sales Invoice",
				get_query: () => {
					const doc_type = this.doc_type_field.get_value();
					return {
						doctype: doc_type,
						filters: { docstatus: ["!=", 2] },
					};
				},
				change: () => this.on_document_change(),
			},
			render_input: true,
		});

		this.show_field = frappe.ui.form.make_control({
			parent: this.$toolbar.get(0),
			df: {
				fieldtype: "Select",
				fieldname: "show",
				label: __("Show"),
				options: "enabled\nall\ndisabled",
				default: "all",
				change: () => this.load_formats(),
			},
			render_input: true,
		});

		this.layout_filter_field = frappe.ui.form.make_control({
			parent: this.$toolbar.get(0),
			df: {
				fieldtype: "Select",
				fieldname: "layout_filter",
				label: __("Layout Type"),
				options: [
					{ value: "all", label: __("All formats (old + new)") },
					{ value: "hide_legacy", label: __("New designs only (hide old color-only)") },
					{ value: "premium", label: __("Premium layouts only") },
					{ value: "regional", label: __("Regional (SA/UAE/PK/IN/US/ME)") },
					{ value: "colorful", label: __("Colorful designs") },
					{ value: "proforma", label: __("Proforma invoices") },
					{ value: "thermal", label: __("Thermal / POS receipts (80mm)") },
				],
				default: "all",
				change: () => this.load_formats(),
			},
			render_input: true,
		});

		this.region_field = frappe.ui.form.make_control({
			parent: this.$toolbar.get(0),
			df: {
				fieldtype: "Select",
				fieldname: "region",
				label: __("Region"),
				options: [
					{ value: "ALL", label: __("All regions") },
					{ value: "SA", label: __("Saudi Arabia") },
					{ value: "AE", label: __("UAE") },
					{ value: "PK", label: __("Pakistan") },
					{ value: "IN", label: __("India") },
					{ value: "US", label: __("USA") },
					{ value: "ME", label: __("Middle East / Gulf") },
				],
				default: "ALL",
				change: () => this.load_formats(),
			},
			render_input: true,
		});

		this.search_field = frappe.ui.form.make_control({
			parent: this.$toolbar.get(0),
			df: {
				fieldtype: "Data",
				fieldname: "search",
				label: __("Search"),
				placeholder: __("Pakistan, ZATCA, Gradient, Dark Header..."),
				change: () => this.load_formats(),
			},
			render_input: true,
		});

		this.page.set_secondary_action(__("Refresh"), () => this.refresh_all(), "refresh");
		this.page.add_menu_item(__("Sync HTML (Stable)"), () => this.sync_formats(false));
		this.page.add_menu_item(__("Sync HTML (All)"), () => this.sync_formats(true));
	}

	setup_actions() {
		this.btn_default = this.page.add_button(__("Set as Default"), () => this.set_default(), {
			icon: "star",
		});
		this.btn_print = this.page.add_button(__("Print"), () => this.print_document(), {
			icon: "printer",
		});
		this.btn_pdf = this.page.add_button(__("PDF"), () => this.download_pdf(), {
			icon: "small-file",
		});
		this.btn_toggle = this.page.add_button(__("Enable"), () => this.toggle_format(), {
			icon: "tick",
		});
		this.btn_open = this.page.add_button(__("Open Format"), () => this.open_format(), {
			icon: "edit",
		});
		this.btn_full = this.page.add_button(__("Full Page"), () => this.open_full_page(), {
			icon: "full-page",
		});

		this.page.set_primary_action(__("Use & Print"), () => this.use_and_print(), "printer");
		this.setup_view_toggles();
	}

	setup_view_toggles() {
		this.$preview_actions.html(`
			<div class="epp-view-toggles">
				<span class="epp-toggle-label">${__("Show in preview")}:</span>
				<label><input type="checkbox" data-key="words" checked> ${__("Amount in Words")}</label>
				<label><input type="checkbox" data-key="sig" checked> ${__("Signature")}</label>
				<label><input type="checkbox" data-key="terms" checked> ${__("Terms")}</label>
				<label><input type="checkbox" data-key="footer" checked> ${__("Footer")}</label>
				<label><input type="checkbox" data-key="qr" checked> ${__("QR Code")}</label>
			</div>
		`);
		this.$preview_actions.find("input[type=checkbox]").on("change", (e) => {
			const key = $(e.target).data("key");
			this.view_toggles[key] = e.target.checked ? 1 : 0;
			this.apply_view_toggles();
		});
	}

	setup_iframe() {
		const skeleton = `<!DOCTYPE html><html><head><meta charset="UTF-8"></head><body></body></html>`;
		this.$iframe.get(0).srcdoc = skeleton;
		this.$iframe_body = null;
	}

	load_doctypes() {
		frappe.call({
			method: "erpnext_print_pack.print_pack.page.print_format_browser.print_format_browser.get_doctypes",
			callback: (r) => {
				if (!r.message) return;
				this.doctypes = r.message;
				const options = r.message.map((row) => row.doc_type).join("\n");
				this.doc_type_field.df.options = options;
				this.doc_type_field.refresh();

				const route = frappe.get_route();
				const preferred = route[1] || "Sales Invoice";
				const exists = r.message.find((o) => o.doc_type === preferred);
				this.doc_type_field.set_value(exists ? preferred : r.message[0]?.doc_type);
			},
		});
	}

	on_doctype_change() {
		const doc_type = this.doc_type_field.get_value();
		if (!doc_type) return;

		this.document_field.df.options = doc_type;
		this.document_field.refresh();
		this.document_field.set_value("");

		frappe.call({
			method: "erpnext_print_pack.print_pack.page.print_format_browser.print_format_browser.get_sample_document",
			args: { doc_type },
			callback: (r) => {
				if (r.message?.name) {
					this.document_field.set_value(r.message.name);
				} else {
					this.current_doc = null;
					this.load_formats();
					frappe.show_alert({
						message: r.message?.message || __("No sample document found"),
						indicator: "orange",
					});
				}
			},
		});
	}

	on_document_change() {
		const doc_type = this.doc_type_field.get_value();
		const name = this.document_field.get_value();
		if (!doc_type || !name) {
			this.current_doc = null;
			this.load_formats();
			return;
		}

		frappe.call({
			method: "erpnext_print_pack.print_pack.page.print_format_browser.print_format_browser.get_document",
			args: { doc_type, name },
			callback: (r) => {
				this.current_doc = r.message || null;
				this.load_formats();
			},
		});
	}

	load_formats() {
		const doc_type = this.doc_type_field.get_value();
		if (!doc_type) return;

		const show = this.show_field.get_value() || "all";
		let show_disabled = 1;
		if (show === "enabled") show_disabled = 0;
		if (show === "disabled") show_disabled = 2;

		frappe.call({
			method: "erpnext_print_pack.print_pack.page.print_format_browser.print_format_browser.get_formats",
			args: {
				doc_type,
				show_disabled,
				search: this.search_field.get_value() || null,
				layout_filter: this.layout_filter_field.get_value() || "all",
				region: this.region_field.get_value() || "ALL",
			},
			callback: (r) => {
				let formats = r.message || [];
				this.formats = formats;
				this.render_format_list();

				if (formats.length) {
					const current = this.selected_format?.name;
					const keep = formats.find((f) => f.name === current);
					this.select_format(keep || formats[0]);
				} else {
					this.selected_format = null;
					this.render_preview_empty(__("No print formats match your filters."));
				}
			},
		});
	}

	render_format_list() {
		const legacy = this.formats.filter((f) => f.is_legacy).length;
		const premium = this.formats.filter((f) => f.is_premium).length;
		this.$format_header.text(
			__("{0} formats ({1} new designs, {2} legacy)", [this.formats.length, premium, legacy])
		);

		if (!this.formats.length) {
			this.$format_items.html(
				`<div class="epp-empty-state">${__("No formats found")}</div>`
			);
			return;
		}

		this.$format_items.html(
			this.formats
				.map((fmt) => {
					const badges = [];
					if (fmt.is_default) badges.push(`<span class="badge default">${__("Default")}</span>`);
					if (fmt.disabled) badges.push(`<span class="badge draft">${__("Disabled")}</span>`);
					else if (fmt.status === "draft") badges.push(`<span class="badge draft">${__("Draft")}</span>`);
					if (!fmt.has_html) badges.push(`<span class="badge no-html">${__("No HTML")}</span>`);
					if (fmt.theme) badges.push(`<span class="badge">${frappe.utils.escape_html(fmt.theme)}</span>`);
					if (fmt.layout_family) badges.push(`<span class="badge default">${frappe.utils.escape_html(fmt.layout_family)}</span>`);
					if (fmt.is_legacy) badges.push(`<span class="badge draft">${__("Legacy")}</span>`);
					if (fmt.region && fmt.region !== "ALL") badges.push(`<span class="badge">${frappe.utils.escape_html(fmt.region)}</span>`);

					return `
						<div class="epp-format-item ${fmt.disabled ? "disabled-format" : ""} ${
						this.selected_format?.name === fmt.name ? "active" : ""
					}" data-name="${frappe.utils.escape_html(fmt.name)}">
							<div class="format-name">${frappe.utils.escape_html(fmt.name)}</div>
							<div class="format-meta">${badges.join("")}</div>
						</div>
					`;
				})
				.join("")
		);

		this.$format_items.find(".epp-format-item").on("click", (e) => {
			const name = $(e.currentTarget).data("name");
			const fmt = this.formats.find((f) => f.name === name);
			if (fmt) this.select_format(fmt);
		});
	}

	select_format(fmt) {
		this.selected_format = fmt;
		this.$format_items.find(".epp-format-item").removeClass("active");
		this.$format_items.find(`.epp-format-item[data-name="${CSS.escape(fmt.name)}"]`).addClass("active");
		this.update_action_buttons();
		this.load_preview();
	}

	update_action_buttons() {
		const fmt = this.selected_format;
		if (!fmt) return;

		const can_preview = this.current_doc && fmt.has_html && !fmt.disabled;
		this.btn_default.toggle(!fmt.is_default);
		this.btn_toggle.text(fmt.disabled ? __("Enable") : __("Disable"));
		this.btn_print.prop("disabled", !can_preview);
		this.btn_pdf.prop("disabled", !can_preview);
		this.page.btn_primary.prop("disabled", !can_preview);
	}

	load_preview() {
		const fmt = this.selected_format;
		if (!fmt) return;

		if (!this.current_doc) {
			this.render_preview_empty(__("Select a sample document to preview."));
			return;
		}

		if (!fmt.has_html) {
			this.render_preview_empty(
				__(
					"No HTML loaded for this format. Click Enable (auto-syncs HTML) or use Sync HTML from the menu."
				)
			);
			return;
		}

		if (fmt.disabled) {
			this.render_preview_empty(
				__("Format is disabled. Click Enable — HTML will be loaded if missing.")
			);
			return;
		}

		if (this._preview_req) {
			this._preview_req.abort();
		}

		this.$preview_message.text(__("Loading preview..."));

		this._preview_req = frappe.call({
			method: "frappe.www.printview.get_html_and_style",
			args: {
				doc: this.current_doc,
				print_format: fmt.name,
				no_letterhead: 1,
				letterhead: __("No Letterhead"),
			},
			callback: (r) => {
				this._preview_req = null;
				if (r.exc) {
					this.render_preview_empty(__("Preview failed. Check format HTML."));
					return;
				}
				this.render_preview_html(r.message);
				this.$preview_message.text("");
			},
		});
	}

	render_preview_html(out) {
		if (!out?.html) {
			this.render_preview_empty(__("No Preview Available"));
			return;
		}

		const iframe = this.$iframe.get(0);
		const doc = iframe.contentDocument || iframe.contentWindow.document;
		const base_url = frappe.urllib.get_base_url();
		const print_css = frappe.assets.bundled_asset("print.bundle.css");

		// Sandbox preview frame: allow same-origin CSS/fonts, block scripts/forms.
		this.$iframe.attr(
			"sandbox",
			"allow-same-origin allow-popups allow-modals"
		);

		doc.open();
		doc.write(`<!DOCTYPE html>
			<html lang="${frappe.boot.lang || "en"}">
			<head>
				<meta charset="UTF-8">
				<meta http-equiv="Content-Security-Policy" content="default-src 'none'; img-src data: blob: *; style-src 'unsafe-inline' ${base_url}; font-src ${base_url} data:;">
				<style>${out.style || ""}</style>
				<link href="${base_url}${print_css}" rel="stylesheet">
			</head>
			<body>
				<div class="print-format print-format-preview">${out.html}</div>
			</body>
			</html>`);
		doc.close();

		setTimeout(() => {
			const height = Math.max(doc.body.scrollHeight, 600);
			this.$iframe.css("height", `${height}px`);
			this.apply_view_toggles();
		}, 300);
	}

	apply_view_toggles() {
		const iframe = this.$iframe.get(0);
		if (!iframe?.contentDocument) return;
		const doc = iframe.contentDocument;
		let style = doc.getElementById("epp-view-toggle-style");
		if (!style) {
			style = doc.createElement("style");
			style.id = "epp-view-toggle-style";
			doc.head.appendChild(style);
		}
		const hide = (cls, on) => (on ? "" : `.${cls}, .epp-${cls} { display: none !important; }\n`);
		style.textContent =
			hide("words", this.view_toggles.words) +
			hide("sig", this.view_toggles.sig) +
			hide("terms", this.view_toggles.terms) +
			hide("footer", this.view_toggles.footer) +
			hide("qr", this.view_toggles.qr);
	}

	render_preview_empty(message) {
		this.$preview_message.text(message || "");
		const iframe = this.$iframe.get(0);
		const doc = iframe.contentDocument || iframe.contentWindow.document;
		doc.open();
		doc.write(`<!DOCTYPE html><html><body><div class="epp-empty-state">${message || ""}</div></body></html>`);
		doc.close();
		this.$iframe.css("height", "200px");
	}

	set_default() {
		if (!this.selected_format) return;
		frappe.call({
			method: "frappe.printing.doctype.print_format.print_format.make_default",
			args: { name: this.selected_format.name },
			callback: () => {
				this.load_formats();
				frappe.show_alert({ message: __("Default print format updated"), indicator: "green" });
			},
		});
	}

	toggle_format() {
		if (!this.selected_format) return;
		const disabled = this.selected_format.disabled ? 0 : 1;
		frappe.call({
			method: "erpnext_print_pack.print_pack.page.print_format_browser.print_format_browser.toggle_disabled",
			args: { name: this.selected_format.name, disabled },
			callback: () => {
				frappe.show_alert({
					message: disabled ? __("Format disabled") : __("Format enabled"),
					indicator: "green",
				});
				const doc_type = this.doc_type_field.get_value();
				frappe.call({
					method: "erpnext_print_pack.print_pack.page.print_format_browser.print_format_browser.get_doctypes",
					callback: (r) => {
						if (r.message) {
							this.doctypes = r.message;
							const options = r.message.map((row) => row.doc_type).join("\n");
							this.doc_type_field.df.options = options;
							this.doc_type_field.refresh();
							this.doc_type_field.set_value(doc_type);
							this.load_formats();
						}
					},
				});
			},
		});
	}

	print_document() {
		this.open_print_view(true);
	}

	download_pdf() {
		if (!this.current_doc || !this.selected_format) return;
		const w = window.open(
			frappe.urllib.get_full_url(
				"/api/method/frappe.utils.print_format.download_pdf?" +
					"doctype=" +
					encodeURIComponent(this.current_doc.doctype) +
					"&name=" +
					encodeURIComponent(this.current_doc.name) +
					"&format=" +
					encodeURIComponent(this.selected_format.name) +
					"&no_letterhead=1"
			)
		);
		if (!w) frappe.msgprint(__("Please enable pop-ups to download PDF"));
	}

	use_and_print() {
		this.open_print_view(true);
	}

	open_print_view(trigger_print = false) {
		if (!this.current_doc || !this.selected_format) return;
		const url =
			"/printview?doctype=" +
			encodeURIComponent(this.current_doc.doctype) +
			"&name=" +
			encodeURIComponent(this.current_doc.name) +
			"&format=" +
			encodeURIComponent(this.selected_format.name) +
			"&no_letterhead=1" +
			(trigger_print ? "&trigger_print=1" : "");
		window.open(url);
	}

	open_full_page() {
		this.open_print_view(false);
	}

	open_format() {
		if (!this.selected_format) return;
		frappe.set_route("Form", "Print Format", this.selected_format.name);
	}

	refresh_all() {
		this.load_formats();
		if (this.selected_format) this.load_preview();
	}

	sync_formats(include_draft) {
		frappe.call({
			method: "erpnext_print_pack.print_pack.page.print_format_browser.print_format_browser.sync_formats",
			args: { include_draft: include_draft ? 1 : 0 },
			freeze: true,
			freeze_message: __("Syncing print format HTML..."),
			callback: (r) => {
				const summary = r.message || {};
				frappe.show_alert({
					message: __("Synced: {0} updated, {1} failed", [
						summary.updated || 0,
						summary.failed || 0,
					]),
					indicator: summary.failed ? "orange" : "green",
				});
				this.refresh_all();
			},
		});
	}
};
