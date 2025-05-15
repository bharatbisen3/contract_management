import frappe
from hrms.hr.doctype.job_offer.job_offer import JobOffer
from frappe import _
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from frappe.utils import cint, flt, get_link_to_form
import secrets
import base64
# from Crypto.Cipher import AES
# from Crypto.Random import get_random_bytes

class custom_job_offer(JobOffer):

    # def onload(self):
    #     super().onload()
        # frappe.msgprint("this is custom app method onload")

    # ========== NEW ENCRYPTION METHODS ==========
    def get_encryption_key(self):
        """Fetch or generate AES encryption key."""
        settings = frappe.get_single("Encryption Settings")
        if not settings.encryption_key:
            key = get_random_bytes(32)  # 256-bit key
            settings.encryption_key = base64.urlsafe_b64encode(key).decode()
            settings.save()
            frappe.db.commit()
        return base64.urlsafe_b64decode(settings.encryption_key)

    def encrypt_verification_id(self, verification_id):
        """Encrypt the verification ID using AES-GCM"""
        key = self.get_encryption_key()
        cipher = AES.new(key, AES.MODE_GCM)
        ciphertext, tag = cipher.encrypt_and_digest(verification_id.encode())
        
        # Combine nonce, ciphertext and tag
        encrypted_data = cipher.nonce + ciphertext + tag
        return base64.urlsafe_b64encode(encrypted_data).decode()

    def decrypt_verification_id(self, encrypted_id):
        """Decrypt the verification ID using AES-GCM"""
        try:
            key = self.get_encryption_key()
            encrypted_bytes = base64.urlsafe_b64decode(encrypted_id)
            
            # Extract nonce (16 bytes), ciphertext (remaining bytes minus 16 for tag)
            nonce = encrypted_bytes[:16]
            ciphertext = encrypted_bytes[16:-16]
            tag = encrypted_bytes[-16:]
            
            cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
            return cipher.decrypt_and_verify(ciphertext, tag).decode()
        except Exception as e:
            frappe.throw(_("Invalid or expired link"), frappe.AuthenticationError)
    # ========== END NEW ENCRYPTION METHODS ==========

    # ========== EXISTING TOKEN METHODS (KEEP AS IS) ==========
    def get_context(context):
        context.no_cache = 1
        token = frappe.form_dict.get('token')
        verification_id = frappe.form_dict.get('vid')
        
        if token and verification_id:
            try:
                job_data = get_job_offer_with_token(verification_id, token)
                context.prefill_data = job_data
            except frappe.AuthenticationError as e:
                context.token_error = str(e)
        return context

    def get_job_offer_with_token(verification_id, token):
        """Verify token and return data"""
        job_offer = frappe.get_doc("Job Offer", verification_id)
        
        if not job_offer.custom_public_access_token:
            raise frappe.AuthenticationError(_("No access token exists for this record"))
        
        if job_offer.custom_public_access_token != token:
            raise frappe.AuthenticationError(_("Invalid token"))
        
        return job_offer.as_dict()

    # @frappe.whitelist()
    def generate_reusable_token(verification_id):
        """Generate a persistent token for a Job Offer"""
        token = f"persistent_{secrets.token_urlsafe(24)}"
        
        frappe.db.set_value("Job Offer", verification_id, {
            "custom_public_access_token": token
        })
        
        return token
    # ========== END EXISTING TOKEN METHODS ==========



        # ========== MODIFIED SEND EMAIL METHOD ==========
    def send_email(self):
        if not self.applicant_email:
            frappe.throw("Applicant does not have an email address")
        
        # Generate or retrieve existing token (keep existing token system)
        if not self.custom_public_access_token:
            self.custom_public_access_token = f"persistent_{secrets.token_urlsafe(24)}"
            self.db_set("custom_public_access_token", self.custom_public_access_token)

        # Create both types of links for backward compatibility 
        plain_link = f"{frappe.utils.get_url()}/employment-contract/new?verification_id={self.name}&token={self.custom_public_access_token}"
        # encrypted_link = f"{frappe.utils.get_url()}/employment-contract/new?vid={self.encrypt_verification_id(self.name)}&token={self.custom_public_access_token}"

        subject = "Job Offer Contract"
        message = f"""Dear Applicant,<br><br>
        Thank you for applying.<br>
        Please click on the link below to open your Contract application:<br><br>
        <a href="{plain_link}">Click Here to Access Contract</a><br>
        Please use the above link for signing contract<br><br><br>
        Regards,<br>
        Ove Erikssons"""

        # (For older systems: <a href="{encrypted_link}">Encrypted Link</a>)<br><br>

        frappe.sendmail(
            recipients=self.applicant_email,    
            subject=subject,
            message=message,
            now=True
        )
        
        frappe.msgprint("Email Sent Successfully!")
    # ========== END MODIFIED SEND EMAIL METHOD ==========

        
        
@frappe.whitelist()
def send_email_link(docname):
    """API endpoint to trigger email sending"""
    doc = frappe.get_doc("Job Offer", docname)
    doc.send_email()
    
    return _("Email sent successfully")
    # frappe.msgprint("Email sent successfully")


    # ========== New CUSTOM METHODS ==========

@frappe.whitelist()
def verify_token(verification_id, token):
    doc = frappe.get_doc("Job Offer", verification_id)
    if not doc.custom_public_access_token or doc.custom_public_access_token != token:
        frappe.throw("Invalid or expired link", frappe.AuthenticationError)
    return True

@frappe.whitelist()
def get_applicant_details(verification_id):
    """Returns applicant details for pre-filling form"""
    job_offer = frappe.get_doc("Job Offer", verification_id)
    # frappe.msgprint(job_offer.applicant_name, job_offer.custom_middle_name)
    
    return {
        "verification_id": verification_id,
        "first_name": job_offer.applicant_name,
        "middle_name": job_offer.custom_middle_name,
        "last_name": job_offer.custom_last_name,
        "gender": job_offer.custom_gender,
        "date_of_birth": job_offer.custom_date_of_birth,
        "country_of_birth": job_offer.custom_country_of_birth_,
        "citizenship": job_offer.custom_citizenship_,
        "applicant_contact_number": job_offer.custom_applicant_contact_number,
        "applicant_email": job_offer.applicant_email,
        "applicant_address": job_offer.custom_applicant_address_a1,
        "address2": job_offer.custom_address_2,
        "zip__postal_code": job_offer.custom_zippostal_code_,
        "city_a": job_offer.custom_city_a1,
        "state__province": job_offer.custom_stateprovince,
        "country_a": job_offer.custom_country_a,
        "bank": job_offer.custom_bank,
        "bic_code": job_offer.custom_bic_code,
        "please_attach_your_valid_id_or_passport": job_offer.custom_please_attach_your_valid_id_or_passport,
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
        "by_law_inc": job_offer.custom_by_law_a,
        "according_to_collective_agreement_and_law_inc": job_offer.custom_according_to_collective_agreement_and_law_a,
        "the_employment_protection_act": job_offer.custom_the_employment_protection_act,
        "collective_agreement": job_offer.custom_collective_agreement,
        "other_conditions": job_offer.custom_other_conditions
    }

    # ========== END CUSTOM METHODS ==========
