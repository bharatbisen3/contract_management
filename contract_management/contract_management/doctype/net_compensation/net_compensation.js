// // // Copyright (c) 2025, bharat and contributors
// // // For license information, please see license.txt

// // // frappe.ui.form.on("Net Compensation", {
// // // 	refresh(frm) {

// // // 	},
// // // });

// frappe.ui.form.on('Net Compensation', {
//     refresh: function(frm) {
//         // Add button to calculate net compensation
//         frm.add_custom_button(__('Calculate Net Compensation'), function() {
//             frm.events.calculate_net_compensation(frm);
//         }).addClass('btn-primary');
//     },

//     work_team: function(frm) {
//         // Clear compensation table when work team changes
//         frm.set_value('compensation', []);
//     },

//     calculate_net_compensation: function(frm) {
//         if (!frm.doc.work_team || !frm.doc.year || !frm.doc.month) {
//             frappe.msgprint(__('Please select Work Team, Year, and Month first.'));
//             return;
//         }

//         frappe.call({
//             method: 'contract_management.contract_management.doctype.net_compensation.net_compensation.get_employees_by_work_team',
//             args: {
//                 work_team: frm.doc.work_team
//             },
//             callback: function(r) {
//                 if (r.message) {
//                     frm.events.fetch_employee_data(frm, r.message);
//                 }
//             }
//         });
//     },





