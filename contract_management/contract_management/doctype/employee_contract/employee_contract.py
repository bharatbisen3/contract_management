# Copyright (c) 2025, bharat and contributors
# For license information, please see license.txt

# # import frappe
# from frappe.model.document import Document

# class EmployeeContract(Document):
# 	pass





# import frappe
# from frappe.model.document import Document
# from frappe.model.mapper import get_mapped_doc  # ✅ Ensure correct import

# class EmployeeContract(Document):
#     def onload(self):
#         if self.applicant_email:
#             self.set_onload("employee", self.applicant_email)  # ✅ Ensure employee is loaded properly


# @frappe.whitelist()
# def make_employee(source_name, target_doc=None):
#     def set_missing_values(source, target):
#         target.personal_email = source.applicant_email  # ✅ Ensure correct field mapping
#         # target.status = "Active"

#     doc = get_mapped_doc(
#         "Employee Contract",
#         source_name,
#         {
#             "Employee Contract": {
#                 "doctype": "Employee",
#                 "field_map": {
#                     "applicant_email": "personal_email",  # ✅ Ensure correct field mapping contract:emp
#                 },
#             }
#         },
#         target_doc,
#         set_missing_values,
#     )

#     doc.insert(ignore_permissions=True)  # ✅ Ensure it inserts without permission issues
#     return doc


import frappe
from frappe.model.document import Document

class EmployeeContract(Document):
    pass  # No changes required in class

@frappe.whitelist()
def check_existing_employee(select_candidate):
    """Checks if an Employee record already exists for the given contract."""
    existing_employee = frappe.db.exists("Employee", {"select_candidate": select_candidate})
    
    if existing_employee:
        return True  # Employee already exists
    return False  # No employee exists
