// Copyright (c) 2025, bharat and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Prospect Applicant", {
// 	refresh(frm) {

// 	},
// });


frappe.ui.form.on('Prospect Applicant', {
    refresh: function(frm) {
        frm.add_custom_button('Send Email', function() {
            frappe.call({
                method: "contract_management.contract_management.doctype.prospect_applicant.prospect_applicant.trigger_send_email",
                args: {
                    docname: frm.doc.name
                },
                callback: function(response) {
                    frappe.msgprint(response.message || "Email sent successfully.");
                }
            });
            console.log(frm.doc.name);
        });
    },
    first_name: function(frm) {
        set_full_name(frm);
    },
    last_name: function(frm) {
        set_full_name(frm);
    }
});


function set_full_name(frm) {
    let full_name = [frm.doc.first_name, frm.doc.last_name]
        // .filter(name => name) // Removes empty values
        .join(' '); // Joins names with space

    frm.set_value('full_name', full_name);
}