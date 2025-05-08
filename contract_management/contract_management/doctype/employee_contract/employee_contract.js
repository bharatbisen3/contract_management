// Copyright (c) 2025, bharat and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Employee Contract", {
// 	refresh(frm) {

// 	},
// });





frappe.ui.form.on("Employee Contract", {
    refresh: function (frm) {
        frm.add_custom_button(__("Create Employee"), function () {
            frappe.call({
                method: "contract_management.contract_management.doctype.employee_contract.employee_contract.check_existing_employee",
                args: {
                    select_candidate: frm.doc.name
                },
                callback: function (r) {
                    if (r.message) {
                        frappe.throw(__("An Employee record already exists for this contract."));
                    } else {
                        frappe.new_doc("Employee", {
                            select_candidate: frm.doc.name,
                            first_name: frm.doc.first_name,
                            middle_name: frm.doc.middle_name,
                            last_name: frm.doc.last_name,  
                            date_of_birth: frm.doc.date_of_birth,
                            country_of_birth: frm.doc.country_of_birth,
                            contact_number: frm.doc.applicant_contact_number,  
                            email_address: frm.doc.applicant_email,
                            gender: frm.doc.gender,
                            citizenship: frm.doc.citizenship,
                            custom_address: frm.doc.applicant_address,
                            custom_city: frm.doc.city_emp,
                            state__province: frm.doc.state__province, // Ensure this field exists in the form
                            zip__postal_code: frm.doc.zip__postal_code, // Ensure this field exists in the form
                            country: frm.doc.country_emp,
                            bank: frm.doc.bank,
                            bic_code: frm.doc.bic_code,
                            id_or_passport: frm.doc.please_attach_your_valid_id_or_passport, // Adjust field name
                            other_bank_name: frm.doc.name_the_other_bank, 
                            your_bank_account_number: frm.doc.your_bank_account_number, // Ensure this field exists in the form
                            // bank_account_number: frm.doc.your_bank_account_number,
                            // personal_email: frm.doc.applicant_email
                        });
                    }
                }
            });
        });
    }
});
