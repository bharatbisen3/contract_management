# Copyright (c) 2025, bharat and contributors
# For license information, please see license.txt

# import frappe
# from frappe.model.document import Document

# class VerificationByHR(Document):



import frappe
from frappe.model.document import Document

class VerificationByHR(Document):
    """Custom methods for the Verification By HR Doctype"""
    
    def send_email(self):
        """Send an email to the applicant with a form link."""

        if not self.email:
            frappe.throw("Email ID is missing.")

        # Validate email format
        frappe.utils.validate_email_address(self.email, throw=True)

        # Generate dynamic form link
        form_link = f"{frappe.utils.get_url()}/employment-contract/new"

        # Email message
        message = f"""
        Dear {getattr(self, 'first_name', 'Applicant')},<br><br>
        Please Click on the link below to sign the contract.<br> 
        <a href='{form_link}'>Click here</a>.  <br>
        """
        # Link: http://23.94.61.169:8000/employment-contract/new  <br> 

        # <a href='{form_link}'>Click here</a>.

        try:
            # Send email asynchronously
            frappe.enqueue(
                method=frappe.sendmail,
                queue="long",
                recipients=[self.email],
                subject="Contract Registration",
                message=message,
                sender="yash@algoware.in"
            )
            frappe.msgprint(f"Email sent successfully to {self.email}.")
        
        except Exception as e:
            frappe.log_error(frappe.get_traceback(), f"Email sending failed for {self.email}")
            frappe.throw("Failed to send email. Please check logs.")



# Whitelisted function for API callsimport frappe
@frappe.whitelist()
def trigger_send_email(docname):
    frappe.logger().info(f"send_email_api called for docname: {docname}")
    doc = frappe.get_doc("Verification By HR", docname)  
    doc.send_email()  
    return f"Email sent successfully ."