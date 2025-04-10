// Copyright (c) 2025, bharat and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Personal Information", {
// 	refresh(frm) {

// 	},
// });


frappe.ui.form.on('Personal Information', {
    first_name: function(frm) {
        set_full_name(frm);
    },
    middle_name: function(frm) {
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