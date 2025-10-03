// // frappe.pages['employee-fetch'].on_page_load = function(wrapper) {
// // 	var page = frappe.ui.make_app_page({
// // 		parent: wrapper,
// // 		title: 'Get All Employees',
// // 		single_column: true
// // 	});
// // }








// frappe.pages['employee-fetch'].on_page_load = function(wrapper) {
//     const page = frappe.ui.make_app_page({
//         parent: wrapper,
//         title: 'Import Employees',
//         single_column: true
//     });
 
//     // Append responsive card layout
// 	$(page.body).append(`
// 	    <div class="flex flex-wrap justify-center gap-4 my-6 w-full margin: auto;" >
// 	        <div class="flex-1 min-w-[250px] max-w-sm rounded-xl shadow border p-4 bg-white text-center mx-5 my-3">
// 	            <div class="text-gray-500 text-sm mb-2">Total Fetched</div>
// 	            <div id="total-fetched" class="text-2xl font-bold text-blue-600">0</div>
// 	        </div>
// 	        <div class="flex-1 min-w-[250px] max-w-sm rounded-xl shadow border p-4 bg-white text-center mx-5 my-3">
// 	            <div class="text-gray-500 text-sm mb-2">Already Exist</div>
// 	            <div id="already-exist" class="text-2xl font-bold text-yellow-600">0</div>
// 	        </div>
// 	        <div class="flex-1 min-w-[250px] max-w-sm rounded-xl shadow border p-4 bg-white text-center mx-5 my-3">
// 	            <div class="text-gray-500 text-sm mb-2">Newly Added</div>
// 	            <div id="newly-added" class="text-2xl font-bold text-green-600">0</div>
// 	        </div>
// 	    </div>
// 	`);
 
//     // Set Import Button
//     function importEmployees() {
//         // Disable button while processing
//         page.clear_primary_action();
 
//         frappe.call({
//             method: "contract_management.CustomEmployee.insert_employee_from_json",
//             freeze: true,
//             freeze_message: "Importing employees, please wait...",
//             callback: function(r) {
//                 const result = r.message || {};
 
//                 // Update the cards
//                 $('#total-fetched').text(result.total_fetched || 0);
//                 $('#already-exist').text(result.already_exist || 0);
//                 $('#newly-added').text(result.newly_added || 0);
 
//                 // Success message
//                 frappe.msgprint({
//                     title: "Import Complete",
//                     message: result.message || "Employee import completed.",
//                     indicator: "green"
//                 });
 
//                 // Re-enable button
//                 page.set_primary_action('Import Employees', importEmployees);
//             },
//             error: function() {
//                 frappe.msgprint({
//                     title: "Error",
//                     message: "Something went wrong during import.",
//                     indicator: "red"
//                 });
 
//                 // Re-enable button
//                 page.set_primary_action('Import Employees', importEmployees);
//             }
//         });
//     }
 
//     // Initial binding of primary action button
//     page.set_primary_action('Import Employees', importEmployees);
// };

















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
        <div id="status-message" class="text-center my-4"></div>
    `);
 
    // Listen for real-time completion notification
    frappe.realtime.on('msgprint', function(data) {
        if (data && data.message && data.message.includes('Employee Import Completed')) {
            // Parse the notification to extract stats
            const parser = new DOMParser();
            const doc = parser.parseFromString(data.message, 'text/html');
            
            // Try to extract numbers from the message
            const text = doc.body.textContent;
            const totalMatch = text.match(/Total Fetched:\s*(\d+)/);
            const existMatch = text.match(/Already Exist:\s*(\d+)/);
            const addedMatch = text.match(/Newly Added:\s*(\d+)/);
            
            if (totalMatch) $('#total-fetched').text(totalMatch[1]);
            if (existMatch) $('#already-exist').text(existMatch[1]);
            if (addedMatch) $('#newly-added').text(addedMatch[1]);
            
            // Show success indicator
            $('#status-message').html('<span class="text-green-600">✓ Import completed successfully</span>');
            
            // Re-enable button
            page.set_primary_action('Import Employees', importEmployees);
        }
    });
 
    // Set Import Button
    function importEmployees() {
        // Disable button while processing
        page.clear_primary_action();
        
        // Show processing status
        $('#status-message').html('<span class="text-blue-600">⏳ Import queued and processing in background...</span>');
 
        frappe.call({
            method: "contract_management.CustomEmployee.insert_employee_from_json",
            callback: function(r) {
                const result = r.message || {};
                
                if (result.status === 'queued') {
                    frappe.show_alert({
                        message: result.message || "Employee import has been queued.",
                        indicator: 'blue'
                    }, 7);
                    
                    // Keep showing the status message
                    $('#status-message').html('<span class="text-blue-600">⏳ Import running in background. You will be notified when complete.</span>');
                    
                } else {
                    // Fallback for synchronous response (if background job fails to queue)
                    $('#total-fetched').text(result.total_fetched || 0);
                    $('#already-exist').text(result.already_exist || 0);
                    $('#newly-added').text(result.newly_added || 0);
                    $('#status-message').html('<span class="text-green-600">✓ Import completed</span>');
                    
                    frappe.msgprint({
                        title: "Import Complete",
                        message: result.message || "Employee import completed.",
                        indicator: "green"
                    });
                }
                
                // Re-enable button after a short delay
                setTimeout(() => {
                    page.set_primary_action('Import Employees', importEmployees);
                }, 2000);
            },
            error: function() {
                frappe.msgprint({
                    title: "Error",
                    message: "Something went wrong during import.",
                    indicator: "red"
                });
                
                $('#status-message').html('<span class="text-red-600">✗ Import failed</span>');
 
                // Re-enable button
                page.set_primary_action('Import Employees', importEmployees);
            }
        });
    }
 
    // Initial binding of primary action button
    page.set_primary_action('Import Employees', importEmployees);
};