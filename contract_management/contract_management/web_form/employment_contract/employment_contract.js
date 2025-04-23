// frappe.ready(function() {
// 	// bind events here
// })









frappe.ready(function () {
    // console.log("Employment Contract Web Form script loaded!");

    let verification_id = frappe.utils.get_url_arg("verification_id");
    let token = frappe.utils.get_url_arg("token");

    // console.log("Verification ID:", verification_id);
    // console.log("Token:", token);

    if (verification_id && token) {
        frappe.call({
            method: "contract_management.contract_management.web_form.employment_contract.employment_contract.fetch_job_offer",
            args: { verification_id: verification_id, token: token },
            callback: function (response) {

                // function formatTimeTo24Hr(timeStr) {
                //     let date = new Date(`1970-01-01T${timeStr}`);
                //     if (isNaN(date)) return null;
                //     return date.toTimeString().split(' ')[0]; // returns "HH:MM:SS"
                // }



                function formatTimeTo24Hr(timeStr) {
                    if (!timeStr) return null;
                    
                    // Handle cases where time might be in "HH:MM" or "HH:MM:SS" format
                    const parts = timeStr.split(':');
                    if (parts.length < 2) return null;
                    
                    // Ensure hours and minutes are two digits
                    const hours = parts[0].padStart(2, '0');
                    const minutes = parts[1].padStart(2, '0');
                    const seconds = parts.length > 2 ? parts[2].padStart(2, '0') : '00';
                    
                    return `${hours}:${minutes}:${seconds}`;
                }



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
                    
                    frappe.web_form.set_value("estimated_starting_date", data.estimated_starting_date);
                    frappe.web_form.set_value("estimated_finish_date", data.estimated_finish_date);
                    frappe.web_form.set_value("workinghours_per_week_and_time", data.workinghours_per_week_and_time);

                    // frappe.web_form.set_value("time_span_start", data.time_span_start);
                    // frappe.web_form.set_value("time_span_end", data.time_span_end);
                    frappe.web_form.set_value("time_span_start", formatTimeTo24Hr(data.time_span_start));
                    frappe.web_form.set_value("time_span_end", formatTimeTo24Hr(data.time_span_end));

                    console.log("Raw start time:", data.time_span_start);
                    console.log("Formatted start time:", formatTimeTo24Hr(data.time_span_start));
                    console.log("Raw End time:", data.time_span_end);
                    console.log("Formatted End time:", formatTimeTo24Hr(data.time_span_end));

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
            error: function (err) {
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
