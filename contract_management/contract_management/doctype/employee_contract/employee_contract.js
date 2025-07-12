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
                            custom_contact_number: frm.doc.applicant_contact_number,
                            custom_email_address: frm.doc.applicant_email,
                            gender: frm.doc.gender,
                            citizenship: frm.doc.citizenship,
                            custom_address: frm.doc.applicant_address,
                            custom_address_2: frm.doc.address2,
                            custom_zip__postal_code: frm.doc.zip__postal_code,
                            custom_city: frm.doc.city_emp,
                            custom_stateprovince: frm.doc.state__province, 
                            custom_country: frm.doc.country_emp,
                            custom_bank: frm.doc.bank,
                            custom_bic_code: frm.doc.bic_code,
                            custom_please_attach_your_valid_id_or_passport: frm.doc.please_attach_your_valid_id_or_passport, 
                            custom_name_the_other_bank: frm.doc.name_the_other_bank, 
                            custom_your_bank_account_number_a: frm.doc.your_bank_account_number
                            // personal_email: frm.doc.applicant_email
                        });
                    }
                }
            });
        });
    }
});
