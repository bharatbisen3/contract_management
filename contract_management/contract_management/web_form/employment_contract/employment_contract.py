# import frappe

# def get_context(context):
# 	# do your magic here
# 	pass



# import frappe

# def get_context(context):
# 	# do your magic here
# 	pass





import frappe
from frappe import _

def get_context(context):
    """Fetch job offer data using token if available in the request."""
    token = frappe.form_dict.get("token")
    verification_id = frappe.form_dict.get("verification_id")

    if token and verification_id:
        try:
            job_offer = fetch_job_offer(verification_id, token)
            context.prefill_data = job_offer
        except frappe.AuthenticationError as e:
            context.token_error = str(e)
        except frappe.DoesNotExistError:
            context.token_error = _("Invalid Job Offer ID")
        except Exception as e:
            frappe.log_error(f"Error fetching job offer: {str(e)}", "Employment Contract Error")
            context.token_error = _("An unexpected error occurred.")

@frappe.whitelist(allow_guest=True)
def fetch_job_offer(verification_id, token):
    """Fetch job offer details securely if the token is valid."""
    job_offer = frappe.get_doc("Job Offer", verification_id)

    if not job_offer.custom_public_access_token or job_offer.custom_public_access_token != token:
        frappe.throw(_("Invalid or expired token"), frappe.AuthenticationError)

    return {
        "verification_id": verification_id,
        "first_name": job_offer.applicant_name,
        "middle_name": job_offer.custom_middle_name,
        "last_name": job_offer.custom_last_name,
        "gender": job_offer.custom_gender,
        "date_of_birth": str(job_offer.custom_date_of_birth),  # Convert date to string
        "country_of_birth": job_offer.custom_country_of_birth_,
        "citizenship": job_offer.custom_citizenship_,
        "applicant_contact_number": job_offer.custom_applicant_contact_number,
        "applicant_email": job_offer.applicant_email,
		
		"applicant_address": job_offer.custom_applicant_address_a1,
		"address2": job_offer.custom_address_2,
     	"zip__postal_code": job_offer.custom_zippostal_code_,
     	"city_emp": job_offer.custom_city_a1,
     	"state__province": job_offer.custom_stateprovince,
     	"country_emp": job_offer.custom_country_a,
     	"bank": job_offer.custom_bank,
     	"bic_code": job_offer.custom_bic_code,
     	"please_attach_a_picture_your_valid_id_or_passport": job_offer.custom_please_attach_your_valid_id_or_passport,
     	"name_the_other_bank": job_offer.custom_name_the_other_bank,
     	"your_bank_account_number": job_offer.custom_your_bank_account_number,

        # "the_work_includes_the_following": job_offer.custom_the_work_includes_the_following,
        "forest_clearing": job_offer.custom_forest_clearing,
        "forest_planting": job_offer.custom_forest_planting,
        "forest_planning": job_offer.custom_forest_planning,
        "work_report": job_offer.custom_work_report,
        # "the_work_includes_the_following": job_offer.custom_the_work_includes_the_following,
        
        "the_main_rule": job_offer.custom_the_main_rule,
        "the_alternative_rule": job_offer.custom_the_alternative_rule,
        "the_exception_rule": job_offer.custom_the_exception_rule,

        "probationary_employment": job_offer.custom_probationary_employment,
        "probationary_employment_period_in_month": job_offer.custom_probationary_employment_period_in_month,
        "special_fixed_term_employment": job_offer.custom_special_fixed_term_employment,
        "seasonal_work": job_offer.custom_seasonal_work,
        "estimated_starting_date": job_offer.custom_estimated_starting_date,
        "estimated_finish_date": job_offer.custom_estimated_finish_date,
        "workinghours_per_week_and_time": job_offer.custom_hours_per_week,
        "time_span_start": job_offer.custom_time_span_start,
        "time_span_end": job_offer.custom_time_span_end,
        "only_ordered_overtime_or_moretime": job_offer.custom_only_ordered_overtime_or_moretime,
        "according_to_the_applicable_collective_agreement": job_offer.custom_according_to_the_applicable_collective_agreement_,
        "hourly_salary_in_sek_gross_salary": job_offer.custom_hourly_salary_in_sek_gross_salary,
        "piecework_pay_according_to_a_separate_agreement": job_offer.custom_plecework_pay_according_to_separate_agreement_,
        "the_salary_is_paid_the_month_after_earning": job_offer.custom_the_salary_is_paid_the_month_after_earning,
        "the_salary_is_paid_on_the_25th_of_each_month": job_offer.custom_the_salary_is_paid_on_the_25th_of_each_month,
        "by_law": job_offer.custom_by_law,
        "according_to_collective_agreement_and_law": job_offer.custom_according_to_collective_agreement_and_law,
        "any_training_provided_by_the_employer": job_offer.custom_any_training_provided_by_the_employer,
        "by_law_emp": job_offer.custom_by_law_a,
        "according_to_collective_agreement_and_law_emp": job_offer.custom_according_to_collective_agreement_and_law_a,
        "the_employment_protection_act": job_offer.custom_the_employment_protection_act,
        "collective_agreement": job_offer.custom_collective_agreement,
        "other_conditions": job_offer.custom_other_conditions
        
    }
