// frappe.ready(function() {
// 	// bind events here
// })


frappe.ready(function() {
    // frappe.web_form.after_load = function() {
        frappe.web_form.on("first_name", (field, value) => {
            set_full_name();
        });
        frappe.web_form.on("middle_name", (field, value) => {
            set_full_name();
        });
        frappe.web_form.on("last_name", (field, value) => {
            set_full_name();
        });

        function set_full_name() {
            let first_name = frappe.web_form.get_value("first_name") || "";
            // let middle_name = frappe.web_form.get_value("middle_name") || "";
            let last_name = frappe.web_form.get_value("last_name") || "";

            let full_name = [first_name, last_name].filter(Boolean).join(" ");
            frappe.web_form.set_value("full_name", full_name);
            console.log(full_name);
        }
    // };
});
