// Copyright (c) 2025, bharat and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Work Team", {
// 	refresh(frm) {

// 	},
// });



frappe.ui.form.on('Work Team', {
    after_save: function(frm) {
        if (frm.doc.team_leader) {
            frappe.call({
                method: 'contract_management.contract_management.doctype.work_team.work_team.create_team_leader_user_permission',
                args: {
                    doc_name: frm.doc.name
                },
                callback: function (r) {
                    if (!r.exc) {
                        // frappe.msgprint(__('User Permission set for Team Leader.'));
                        console.log("User Permission set for Team Leader")
                    }else{
                        console.log("Unable to set User Permission for Team Leader")
                    }
                }
            });
        }
    }
});
