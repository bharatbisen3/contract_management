# Copyright (c) 2025, bharat and contributors
# For license information, please see license.txt

# import frappe
# from frappe.model.document import Document

# class ProspectApplicant(Document):

#     @frappe.whitelist()
#     def send_prospect_email(self):
#         if not self.email:
#             frappe.throw("Email not found!")

#         subject = "Please Fillout this Form"
#         message = f"""
#         Dear {self.first_name},<br><br>
#         Thank you for applying.<br>
#         Please click on the following link to fill your form: <br>
#         <a href='http://23.94.61.169:8000/personal-information/new'>Click here</a>.
#         """

#         frappe.sendmail(
#             recipients=self.email,
#             subject=subject,
#             message=message
#         )

#         frappe.msgprint("Email sent successfully")



#     # message = f"Dear {applicant_name},<br><br>Thank you for applying. We have received your application."




import frappe
from frappe.model.document import Document

class ProspectApplicant(Document):
    """Custom methods for the Prospect Applicant Doctype"""

    def send_email(self):
        """Send an email to the Prospect Applicant with a form link."""
        
        if not self.email:
            frappe.throw("No email address found for this applicant.")

        # Generate dynamic form link
        # form_link = f"{frappe.utils.get_url()}/personal-information/new"
        # form_link = f"{frappe.utils.get_url()}/application-form/new"
        form_link = f"{frappe.utils.get_url()}/application-form/new"


        # Email message
        message = f"""
        Dear {self.first_name},<br><br>
        Thank you for applying.<br> 
        Please click on the following link to fill your form: <br> 
        <a href="{form_link}">Click Here</a><br>
        """
        # <a href='{form_link}'>Click here</a>.

        try:
            # Send email asynchronously
            frappe.enqueue(
                method=frappe.sendmail,
                queue="long",
                recipients=[self.email],
                subject="Complete Your Application Form",
                message=message,
                sender="yash@algoware.in"
            )
            frappe.msgprint(f"Email sent successfully to {self.email}.")
        
        except Exception as e:
            frappe.log_error(f"Email sending failed for {self.email}: {str(e)}")
            frappe.throw("Failed to send email. Please check logs.")

# ✅ Whitelisted function for manual API calls
@frappe.whitelist()
def trigger_send_email(docname):
    """Function that can be called via API to send an email."""
    doc = frappe.get_doc("Prospect Applicant", docname)
    doc.send_email()
    return "Email sent successfully."

# ✅ Hook function for automatic email sending
def send_email_on_creation(doc, after_insert):
    """Function triggered automatically when a new Prospect Applicant is created."""
    doc.send_email()

