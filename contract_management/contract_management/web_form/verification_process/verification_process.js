// frappe.ready(function() {
// 	// bind events here
// })



frappe.ready(function () {
    // console.log("Web form is ready!");

    frappe.web_form.on('candidateid', (field, value) => {
        // console.log("Selected Employee ID:", value);

        if (value) {
            frappe.call({
                method: "frappe.client.get",
                args: {
                    doctype: "Personal Information",
                    name: value
                },
                callback: function (response) {
                    // console.log("Response from Frappe:", response);

                    if (response.message) {
                        let emp = response.message;
                        frappe.web_form.set_value("first_name", emp.first_name);
                        frappe.web_form.set_value("middle_name", emp.middle_name);
                        frappe.web_form.set_value("last_name", emp.last_name);
                        frappe.web_form.set_value("birthday", emp.birthday);
                        frappe.web_form.set_value("citizenship_", emp.citizenship_);
                        frappe.web_form.set_value("country_of_birth", emp.country_of_birth);
                        frappe.web_form.set_value("email", emp.email);
                        frappe.web_form.set_value("address", emp.address);
                        frappe.web_form.set_value("city", emp.city);

                        frappe.web_form.set_value("state__province", emp.state__province);
                        frappe.web_form.set_value("zip__postal_code", emp.zip__postal_code);
                        frappe.web_form.set_value("country", emp.country);
                        frappe.web_form.set_value("mobile__phone_number", emp.mobile_phone_number);
                        frappe.web_form.set_value("email", emp.email);
                        frappe.web_form.set_value("bank_information", emp.bank);
                        frappe.web_form.set_value("name_of_other_bank", emp.name_the_other_bank);
                        frappe.web_form.set_value("bic_code", emp.bic_code);
                        frappe.web_form.set_value("your_bank_account_number", emp.account_number);
                        frappe.web_form.set_value("please_attach_your_valid_id_or_passport", emp.please_attach_your_valid_id_or_passport);
                        // console.log("Fields updated successfully!");
                    } else {
                        // console.log("No data found for Employee ID:", value);
                    }
                },
                error: function (err) {
                    // console.error("Error fetching Employee Information:", err);
                }
            });
        }
    });
});
