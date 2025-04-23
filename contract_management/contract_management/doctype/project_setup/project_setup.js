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











// frappe.ui.form.on("Project Setup", {
//     onload: function(frm) {
//         if (!frm.is_new()) {
//             frappe.db.get_list("Project Attendance", {
//                 fields: ["area_completed_for_this_submission"],
//                 filters: {
//                     docstatus: 1,
//                     project__client: frm.doc.name
//                 }
//             }).then(records => {
//                 let total = 0;
//                 records.forEach(rec => {
//                     total += rec.area_completed_for_this_submission;
//                     console.log("For Each Total: ", total);
//                 });

//                 // Visually update field in the form
//                 frm.set_value("total_compleated_work_till_now", total);

//                 // Save it in the database too
//                 frappe.db.set_value('Project Setup', frm.doc.name, 'total_compleated_work_till_now', total)
//                     .then(() => {
//                         console.log("Auto-updated in DB:", total);
//                         frappe.msgprint(__('Total completed work auto-updated'));
//                     });
//             });
//         }
//     }
// });
