// frappe.pages['employee-fetch'].on_page_load = function(wrapper) {
// 	var page = frappe.ui.make_app_page({
// 		parent: wrapper,
// 		title: 'Get All Employees',
// 		single_column: true
// 	});
// }








frappe.pages['employee-fetch'].on_page_load = function(wrapper) {
    const page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'Import Employees',
        single_column: true
    });
 
    // Append responsive card layout
	$(page.body).append(`
	    <div class="flex flex-wrap justify-center gap-4 my-6 w-full margin: auto;" >
	        <div class="flex-1 min-w-[250px] max-w-sm rounded-xl shadow border p-4 bg-white text-center mx-5 my-3">
	            <div class="text-gray-500 text-sm mb-2">Total Fetched</div>
	            <div id="total-fetched" class="text-2xl font-bold text-blue-600">0</div>
	        </div>
	        <div class="flex-1 min-w-[250px] max-w-sm rounded-xl shadow border p-4 bg-white text-center mx-5 my-3">
	            <div class="text-gray-500 text-sm mb-2">Already Exist</div>
	            <div id="already-exist" class="text-2xl font-bold text-yellow-600">0</div>
	        </div>
	        <div class="flex-1 min-w-[250px] max-w-sm rounded-xl shadow border p-4 bg-white text-center mx-5 my-3">
	            <div class="text-gray-500 text-sm mb-2">Newly Added</div>
	            <div id="newly-added" class="text-2xl font-bold text-green-600">0</div>
	        </div>
	    </div>
	`);
 
    // Set Import Button
    function importEmployees() {
        // Disable button while processing
        page.clear_primary_action();
 
        frappe.call({
            method: "contract_management.CustomEmployee.insert_employee_from_json",
            freeze: true,
            freeze_message: "Importing employees, please wait...",
            callback: function(r) {
                const result = r.message || {};
 
                // Update the cards
                $('#total-fetched').text(result.total_fetched || 0);
                $('#already-exist').text(result.already_exist || 0);
                $('#newly-added').text(result.newly_added || 0);
 
                // Success message
                frappe.msgprint({
                    title: "Import Complete",
                    message: result.message || "Employee import completed.",
                    indicator: "green"
                });
 
                // Re-enable button
                page.set_primary_action('Import Employees', importEmployees);
            },
            error: function() {
                frappe.msgprint({
                    title: "Error",
                    message: "Something went wrong during import.",
                    indicator: "red"
                });
 
                // Re-enable button
                page.set_primary_action('Import Employees', importEmployees);
            }
        });
    }
 
    // Initial binding of primary action button
    page.set_primary_action('Import Employees', importEmployees);
};