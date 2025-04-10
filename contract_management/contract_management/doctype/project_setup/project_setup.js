// Copyright (c) 2025, bharat and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Project Setup", {
// 	refresh(frm) {

// 	},
// });

//  "contract_management.contract_management.doctype.project_setup.project_setup.create_user_permission"



frappe.ui.form.on("Project Setup", {

    after_save: function(frm) {
        frappe.call({
            method: "contract_management.contract_management.doctype.project_setup.project_setup.create_user_permission",
            args: {
                doc_name: frm.doc.name
            },
            callback: function(response) {
                // console.log(response)
                if (response.message) {
                    // frappe.msgprint(response.message);
                    console.log(response.message)
                }
            }
        });
    },
    before_submit: function(frm) {
        if (frm.doc.status !== "Completed") {
            frappe.msgprint(__('You can only submit this document when the Project is "Completed".'));
            frappe.validated = false;  // Prevent submission
        }
    }


});


