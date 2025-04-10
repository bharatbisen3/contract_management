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

    if not job_offer.public_access_token or job_offer.public_access_token != token:
        frappe.throw(_("Invalid or expired token"), frappe.AuthenticationError)

    return {
        "verification_id": verification_id,
        "first_name": job_offer.applicant_name,
        "middle_name": job_offer.middle_name,
        "last_name": job_offer.last_name,
        "gender": job_offer.gender,
        "date_of_birth": str(job_offer.date_of_birth),  # Convert date to string
        "country_of_birth": job_offer.country_of_birth,
        "citizenship": job_offer.citizenship_,
        "applicant_contact_number": job_offer.applicant_contact_number,
        "applicant_email": job_offer.applicant_email_address,
		
		"applicant_address": job_offer.applicant_address,
     	"city_emp": job_offer.city_a,
     	"state__province": job_offer.state__province,
     	"zip__postal_code": job_offer.zip__postal_code,
     	"country_emp": job_offer.country_a,
     	"bank": job_offer.bank,
     	"bic_code": job_offer.bic_code,
     	"please_attach_a_picture_your_valid_id_or_passport": job_offer.please_attach_your_valid_id_or_passport,
     	"name_the_other_bank": job_offer.name_the_other_bank,
     	"your_bank_account_number": job_offer.your_bank_account_number,

        "the_work_includes_the_following": job_offer.the_work_includes_the_following,
        "the_main_rule": job_offer.the_main_rule,
        "the_alternative_rule": job_offer.the_alternative_rule,
        "the_exception_rule": job_offer.the_exception_rule,

        "probationary_employment": job_offer.probationary_employment,
        "special_fixed_term_employment": job_offer.special_fixed_term_employment,
        "seasonal_work": job_offer.seasonal_work,
        "estimated_starting_date": job_offer.estimated_starting_date,
        "estimated_finish_date": job_offer.estimated_finish_date,
        "workinghours_per_week_and_time": job_offer.workinghours_per_week_and_time,
        "time_span_start": job_offer.time_span_start,
        "time_span_end": job_offer.time_span_end,
        "only_ordered_overtime_or_moretime": job_offer.only_ordered_overtime_or_moretime,
        "according_to_the_applicable_collective_agreement": job_offer.according_to_the_applicable_collective_agreement,
        "hourly_salary_in_sek_gross_salary": job_offer.hourly_salary_in_sek_gross_salary,
        "piecework_pay_according_to_a_separate_agreement": job_offer.piecework_pay_according_to_a_separate_agreement,
        "the_salary_is_paid_the_month_after_earning": job_offer.the_salary_is_paid_the_month_after_earning,
        "the_salary_is_paid_on_the_25th_of_each_month": job_offer.the_salary_is_paid_on_the_25th_of_each_month,
        "by_law": job_offer.by_law,
        "according_to_collective_agreement_and_law": job_offer.according_to_collective_agreement_and_law,
        "any_training_provided_by_the_employer": job_offer.any_training_provided_by_the_employer,
        "by_law_emp": job_offer.by_law_inc,
        "according_to_collective_agreement_and_law_emp": job_offer.according_to_collective_agreement_and_law_inc,
        "the_employment_protection_act": job_offer.the_employment_protection_act,
        "collective_agreement": job_offer.collective_agreement,
        "other_conditions": job_offer.other_conditions
        
    }
