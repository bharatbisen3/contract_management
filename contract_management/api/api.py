# import frappe

# @frappe.whitelist(allow_guest=True)
# def get_data(doctype, name):
#     """Fetches data for the given Doctype and document name"""
#     data = frappe.get_doc("Job Offer", name)
#     return data





# import frappe

# @frappe.whitelist(allow_guest=True)
# def get_job_offer(name):
#     """
#     Fetches Job Offer details for a given name (ID)
#     :param name: The Job Offer ID (Verification ID)
#     :return: Job Offer details in JSON format
#     """
#     if not name:
#         return {"error": "Verification ID is required"}

#     try:
#         job_offer = frappe.get_doc("Job Offer", name)
#         return {
#             "applicant_name": job_offer.applicant_name,
#             "middle_name": job_offer.middle_name,
#             "last_name": job_offer.last_name,
#             "date_of_birth": job_offer.date_of_birth,
#             "country_of_birth": job_offer.country_of_birth,
#             "citizenship": job_offer.citizenship_,
#             "applicant_contact_number": job_offer.applicant_contact_number,
#             "applicant_email": job_offer.applicant_email_address,
#             "applicant_address": job_offer.applicant_address,
#             "city_emp": job_offer.city_a,
#             "state__province": job_offer.state__province,
#             "zip__postal_code": job_offer.zip__postal_code,
#             "country_emp": job_offer.country_a,
#             "bank": job_offer.bank,
#             "bic_code": job_offer.bic_code,
#             "your_bank_account_number": job_offer.your_bank_account_number,
#             "work_includes": job_offer.the_work_includes_the_following,
#             "employment_protection_act": job_offer.the_employment_protection_act,
#             "place": job_offer.place,
#             "date": job_offer.date,
#             "signature_from_employer": job_offer.signature_from_employer
#         }
#     except frappe.DoesNotExistError:
#         return {"error": "Job Offer not found"}
#     except Exception as e:
#         return {"error": str(e)}
