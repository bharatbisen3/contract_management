frappe.pages['employee-fetch'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Get All Employees',
		single_column: true
	});
}