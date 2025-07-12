# Copyright (c) 2025, bharat and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class ProjectAttendance(Document):
	pass





# import frappe
# from frappe.model.document import Document

# class ProjectAttendance(Document):
#     pass

# @frappe.whitelist()
# def get_filtered_options(parent, child_doctype, sla_class=None):
#     filters = {"parent": parent}
#     if child_doctype == "Class Table" and sla_class:
#         filters["sla_class"] = sla_class
    
#     return frappe.get_all(
#         child_doctype,
#         filters=filters,
#         pluck="object_name" if child_doctype == "Object Table" else "class_name"
#     )