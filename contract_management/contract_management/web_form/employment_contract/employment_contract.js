// frappe.ready(function() {
// 	// bind events here
// })





// frappe.ready(function () {
//     console.log("Web form is ready!");


//     // *****************************   Auto Fetch Form  *********************************************
    
//     frappe.web_form.on('verification_id', (field, value) => {
//         console.log("Selected Employee ID:", value);

//         if (value) {
//             frappe.call({
//                 method: "frappe.client.get",
//                 args: {
//                     doctype: "Job Offer",
//                     name: value
//                 },
//                 callback: function (response) {
                    
//                     if (response.message) {
//                         let emp = response.message;
//                         console.log(emp)

//                         // frappe.web_form.set_value("employer", "Ljungan Skogsvård AB");
//                         // frappe.web_form.set_value("address", "Folkethusvägen 40");
//                         // frappe.web_form.set_value("postcode", "841 98");
//                         // frappe.web_form.set_value("city", "LJUNGAVERK");
//                         // frappe.web_form.set_value("organization_number", "559292-9086");
//                         // frappe.web_form.set_value("mobile_phone_number", "+46 727431411");
//                         // frappe.web_form.set_value("country", "Sweden");
//                         // frappe.web_form.set_value("website", "https://www.github.com");
//                         // frappe.web_form.set_value("mobile_phone_number", "+91-9876543210");
//                         // console.log(frappe.web_form.value.phone)
//                         console.log(emp.applicant_name)

//                         frappe.web_form.set_value("first_name", emp.applicant_name);
//                         frappe.web_form.set_value("middle_name", emp.middle_name);
//                         frappe.web_form.set_value("last_name", emp.last_name);
//                         frappe.web_form.set_value("date_of_birth", emp.date_of_birth);
//                         frappe.web_form.set_value("country_of_birth", emp.country_of_birth);
//                         frappe.web_form.set_value("citizenship", emp.citizenship_);
//                         frappe.web_form.set_value("country_of_birth", emp.country_of_birth);
//                         frappe.web_form.set_value("applicant_contact_number", emp.applicant_contact_number);
//                         frappe.web_form.set_value("applicant_email", emp.applicant_email_address);
//                         frappe.web_form.set_value("applicant_address", emp.applicant_address);
//                         frappe.web_form.set_value("city_emp", emp.city_a);
//                         frappe.web_form.set_value("state__province", emp.state__province);
//                         frappe.web_form.set_value("zip__postal_code", emp.zip__postal_code);
//                         frappe.web_form.set_value("country_emp", emp.country_a);
//                         frappe.web_form.set_value("bank", emp.bank);
//                         frappe.web_form.set_value("name_the_other_bank", emp.name_the_other_bank);
//                         frappe.web_form.set_value("bic_code", emp.bic_code);
//                         frappe.web_form.set_value("your_bank_account_number", emp.your_bank_account_number);
//                         frappe.web_form.set_value("please_attach_a_picture_your_valid_id_or_passport", emp.please_attach_your_valid_id_or_passport);
//                         frappe.web_form.set_value("the_work_includes_the_following", emp.the_work_includes_the_following);
//                         frappe.web_form.set_value("the_main_rule", emp.the_main_rule);
//                         frappe.web_form.set_value("the_alternative_rule", emp.the_alternative_rule);
//                         frappe.web_form.set_value("the_exception_rule", emp.the_exception_rule);
//                         frappe.web_form.set_value("probationary_employment", emp.probationary_employment);
//                         frappe.web_form.set_value("special_fixed_term_employment", emp.special_fixed_term_employment);
//                         frappe.web_form.set_value("seasonal_work", emp.seasonal_work);
//                         frappe.web_form.set_value("estimated_starting_date", emp.estimated_finish_date);
//                         frappe.web_form.set_value("estimated_finish_date", emp.estimated_starting_date);
//                         frappe.web_form.set_value("workinghours_per_week_and_time", emp.workinghours_per_week_and_time);
//                         // frappe.web_form.set_value("time_span_start", emp.time_span_start);
//                         // frappe.web_form.set_value("time_span_end", emp.time_span_end);
//                         frappe.web_form.set_value("only_ordered_overtime_or_moretime", emp.only_ordered_overtime_or_moretime);
//                         frappe.web_form.set_value("according_to_the_applicable_collective_agreement", emp.according_to_the_applicable_collective_agreement);
//                         frappe.web_form.set_value("hourly_salary_in_sek_gross_salary", emp.hourly_salary_in_sek_gross_salary);
//                         frappe.web_form.set_value("piecework_pay_according_to_a_separate_agreement", emp.piecework_pay_according_to_a_separate_agreement);
//                         frappe.web_form.set_value("the_salary_is_paid_the_month_after_earning", emp.the_salary_is_paid_the_month_after_earning);
//                         frappe.web_form.set_value("the_salary_is_paid_on_the_25th_of_each_month", emp.the_salary_is_paid_on_the_25th_of_each_month);
//                         frappe.web_form.set_value("by_law", emp.by_law);
//                         frappe.web_form.set_value("according_to_collective_agreement_and_law", emp.according_to_collective_agreement_and_law);
//                         frappe.web_form.set_value("any_training_provided_by_the_employer", emp.any_training_provided_by_the_employer);
//                         frappe.web_form.set_value("by_law_emp", emp.by_law_inc);
//                         frappe.web_form.set_value("according_to_collective_agreement_and_law_copy", emp.according_to_collective_agreement_and_law_inc);
//                         frappe.web_form.set_value("the_employment_protection_act", emp.the_employment_protection_act);
//                         frappe.web_form.set_value("collective_agreement", emp.collective_agreement);
//                         frappe.web_form.set_value("other_conditions", emp.other_conditions);
//                         frappe.web_form.set_value("language", emp.language);
//                         // frappe.web_form.set_value("english", emp.english);
//                         // frappe.web_form.set_value("romanian", emp.romanian);
//                         // frappe.web_form.set_value("thai", emp.thai);
//                         frappe.web_form.set_value("place", emp.place);
//                         frappe.web_form.set_value("date", emp.date);
//                         frappe.web_form.set_value("signature_from_employer", emp.signature_from_employer);
//                         // frappe.web_form.set_value("please_attach_your_valid_id_or_passport", emp.custom_please_attach_your_valid_id_or_passport);
//                         console.log("Fields updated successfully!");
//                     } else {
//                         console.log("No data found for Employee ID:", value);
//                     }
//                 },
//                 error: function (err) {
//                     console.error("Error fetching Employee Information:", err);
//                 }
//             });
//         }
//     });
//     // *****************************   Auto Fetch Form ended here ****************************************
    
// });









frappe.ready(function() {
    // console.log("Employment Contract Web Form script loaded!");

    let verification_id = frappe.utils.get_url_arg("verification_id");
    let token = frappe.utils.get_url_arg("token");

    // console.log("Verification ID:", verification_id);
    // console.log("Token:", token);

    if (verification_id && token) {
        frappe.call({
            method: "contract_management.contract_management.web_form.employment_contract.employment_contract.fetch_job_offer",
            args: { verification_id: verification_id, token: token },
            callback: function(response) {
                if (response.message) {
                    let data = response.message;

                    // Autofill only the fields provided by the token
                    frappe.web_form.set_value("verification_id", data.verification_id);
                    frappe.web_form.set_value("first_name", data.first_name);
                    frappe.web_form.set_value("middle_name", data.middle_name);
                    frappe.web_form.set_value("last_name", data.last_name);
                    frappe.web_form.set_value("gender", data.gender);
                    frappe.web_form.set_value("date_of_birth", data.date_of_birth);
                    frappe.web_form.set_value("country_of_birth", data.country_of_birth);
                    frappe.web_form.set_value("citizenship", data.citizenship);
                    frappe.web_form.set_value("applicant_contact_number", data.applicant_contact_number);
                    frappe.web_form.set_value("applicant_email", data.applicant_email);

                    frappe.web_form.set_value("applicant_address", data.applicant_address);
                    frappe.web_form.set_value("city_emp", data.city_emp);
                    frappe.web_form.set_value("state__province", data.state__province);
                    frappe.web_form.set_value("zip__postal_code", data.zip__postal_code);
                    frappe.web_form.set_value("country_emp", data.country_emp);

                    frappe.web_form.set_value("bank", data.bank);
                    frappe.web_form.set_value("bic_code", data.bic_code);
                    frappe.web_form.set_value("please_attach_a_picture_your_valid_id_or_passport", data.please_attach_a_picture_your_valid_id_or_passport);
                    frappe.web_form.set_value("name_the_other_bank", data.name_the_other_bank);
                    frappe.web_form.set_value("your_bank_account_number", data.your_bank_account_number);

                    frappe.web_form.set_value("the_work_includes_the_following", data.the_work_includes_the_following);
                    frappe.web_form.set_value("the_main_rule", data.the_main_rule);
                    frappe.web_form.set_value("the_alternative_rule", data.the_alternative_rule);
                    frappe.web_form.set_value("the_exception_rule", data.the_exception_rule);

                    frappe.web_form.set_value("probationary_employment", data.probationary_employment);
                    frappe.web_form.set_value("special_fixed_term_employment", data.special_fixed_term_employment);
                    frappe.web_form.set_value("seasonal_work", data.seasonal_work);
                    frappe.web_form.set_value("estimated_finish_date", data.estimated_finish_date);
                    frappe.web_form.set_value("workinghours_per_week_and_time", data.workinghours_per_week_and_time);
                    frappe.web_form.set_value("time_span_start", data.time_span_start);
                    frappe.web_form.set_value("time_span_end", data.time_span_end);
                    frappe.web_form.set_value("only_ordered_overtime_or_moretime", data.only_ordered_overtime_or_moretime);
                    frappe.web_form.set_value("according_to_the_applicable_collective_agreement", data.according_to_the_applicable_collective_agreement);
                    frappe.web_form.set_value("hourly_salary_in_sek_gross_salary", data.hourly_salary_in_sek_gross_salary);
                    frappe.web_form.set_value("piecework_pay_according_to_a_separate_agreement", data.piecework_pay_according_to_a_separate_agreement);
                    frappe.web_form.set_value("the_salary_is_paid_the_month_after_earning", data.the_salary_is_paid_the_month_after_earning);
                    frappe.web_form.set_value("the_salary_is_paid_on_the_25th_of_each_month", data.the_salary_is_paid_on_the_25th_of_each_month);
                    frappe.web_form.set_value("by_law", data.by_law);
                    frappe.web_form.set_value("according_to_collective_agreement_and_law", data.according_to_collective_agreement_and_law);
                    frappe.web_form.set_value("any_training_provided_by_the_employer", data.any_training_provided_by_the_employer);
                    frappe.web_form.set_value("by_law_emp", data.by_law_emp);
                    frappe.web_form.set_value("according_to_collective_agreement_and_law_emp", data.according_to_collective_agreement_and_law_emp);
                    frappe.web_form.set_value("the_employment_protection_act", data.the_employment_protection_act);
                    frappe.web_form.set_value("collective_agreement", data.collective_agreement);

                    // Log for debugging
                    // console.log("Job Offer data loaded:", data);
                    console.log("Data successfully set in the form!");
                } else {
                    console.log("No data received from API");
                }
            },
            error: function(err) {
                frappe.msgprint({
                    title: __('Error'),
                    message: __("Invalid or expired link."),
                    indicator: 'red'
                });
                // console.error("Error fetching job offer:", err);
            }
        });
    } else {
        // console.error("Missing verification ID or token in URL");
        frappe.msgprint({
            title: __('Error'),
            message: __("Missing verification ID or token."),
            indicator: 'red'
        });
    }
});
