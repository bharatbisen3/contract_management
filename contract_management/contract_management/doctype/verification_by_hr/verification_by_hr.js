// Copyright (c) 2025, bharat and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Verification By HR", {
// 	refresh(frm) {

// 	},
// });






// frappe.ui.form.on('Verification By HR', {
//     refresh: function(frm) {
//         // frm.add_custom_button(__('Create Employee'), function() {
//         //     if (frm.doc.status === 'Approve') {
//         //         frappe.route_options = {
//         //             first_name: frm.doc.first_name,
//         //             last_name: frm.doc.last_name
//         //         };
//         //         frappe.set_route("Form", "Employee", "new-employee");
//         //     } else {
//         //         frappe.msgprint(__('The status must be "Approve" to create a new employee.'));
//         //     }
//         // }, __('Action'));

//         frm.add_custom_button(__('Create Contract'), function() {
//             if (frm.doc.status === 'Approve') {
//                 frappe.route_options = {
//                     // employee_name: frm.doc.first_name + ' ' + frm.doc.last_name,
//                     verification_id: frm.doc.name
//                 };
//                 frappe.set_route("Form", "Employment Contract", "new-employment-contract");
//             } else {
//                 frappe.msgprint(__('The status must be "Approve" to create an employment contract.'));
//             }
//         }, __('Action'));


//         frm.add_custom_button('Send Email', function() {

//             frappe.call({
//                 method: "contract_management.contract_management.doctype.verification_by_hr.verification_by_hr.send_email_api",
//                 args: {
//                     docname: frm.doc.name
//                 },
//                 callback: function(response) {
//                     if (response.message) {
//                         frappe.msgprint(response.message);
//                     } else {
//                         frappe.msgprint(__('Email sent successfully.'));
//                     }
//                 }
//             });

//         }, __('Action'));




//     }
// });



// contract_management/contract_management/contract_management/doctype/verification_by_hr/verification_by_hr.js









// frappe.ui.form.on('Verification By HR', {
//     refresh: function(frm) {
//         // Ensure the document is saved before allowing email to be sent
//         if (!frm.doc.__islocal) {
//             frm.add_custom_button(__('Create Contract'), function() {
//                 if (frm.doc.status === 'Approve') {
//                     frappe.route_options = {
//                         verification_id: frm.doc.name
//                     };
//                     frappe.set_route("Form", "Employment Contract", "new-employment-contract");
//                 } else {
//                     frappe.msgprint(__('The status must be "Approve" to create an employment contract.'));
//                 }
//             }, __('Action'));

//             frm.add_custom_button(__('Send Email'), function() {
//                 frappe.call({
//                     // method: "contract_management.contract_management.doctype.verification_by_hr.verification_by_hr.send_email_api",
//                     method: "contract_management.contract_management.doctype.verification_by_hr.verification_by_hr.send_email_api",
//                     args: {
//                         docname: frm.doc.name
//                     },
//                     callback: function(response) {
//                         if (response.message) {
//                             frappe.msgprint(response.message);
//                         } else {
//                             frappe.msgprint(__('Email sent successfully.'));
//                         }
//                     },
//                     error: function(err) {
//                         frappe.msgprint(__('An error occurred while sending the email.'));
//                     }
//                 });
//             }, __('Action'));
//         }
//     }
// });





frappe.ui.form.on('Verification By HR', {
    refresh: function(frm) {
        frm.add_custom_button(__('Send Email'), function() {
            
            frappe.call({
                method: "contract_management.contract_management.doctype.verification_by_hr.verification_by_hr.trigger_send_email",
                args: { docname: "VERF-Demo Entry-012" },
                callback: function(response) {
                    console.log("Success:", response.message);
                    frappe.msgprint("Email sent successfully!");
                },
                error: function(err) {
                    console.error("Error:", err);
                    frappe.msgprint("Failed to send email.");
                }
            });
            


        });
    }
});

