# # Copyright (c) 2025, bharat and contributors
# # For license information, please see license.txt

# # import frappe
# from frappe.model.document import Document


# class ProjectSetup(Document):
# 	pass








import frappe
from frappe import _
from frappe.model.document import Document

class ProjectSetup(Document):
	pass
    # def get_doc_status_label(self):
    #     if self.docstatus == 0:
    #         return frappe._("In Progress")
    #     elif self.docstatus == 1:
    #         return frappe._("Completed")
    #     elif self.docstatus == 2:
    #         return frappe._("Cancelled")    

	# pass





@frappe.whitelist()
def create_user_permission(doc_name):
    doc = frappe.get_doc("Project Setup", doc_name)

    if not doc.work_team:
        frappe.throw(_("Work Team is mandatory to save the Project Setup"))

    user_permission_exists = frappe.db.exists("User Permission", {
        # "user": frappe.session.user,
        "user": doc.team_leader,
        "allow": "Project Setup",
        "for_value": doc.name,
        "project_setup": doc.name
    })

    if not user_permission_exists:
        user_permission = frappe.get_doc({
            "doctype": "User Permission",
            # "user": frappe.session.user,
            "user": doc.team_leader,
            "allow": "Project Setup",
            "for_value": doc.name,
            "project_setup": doc.name,
            "apply_to_all_doctypes": 1
        })
        user_permission.insert(ignore_permissions=True)
        return _("User Permission created successfully for Project {0}").format(doc.name)
    # else:
    #     return _("Thank You Project {0}").format(doc.name)
















# @frappe.whitelist()
# def get_total_completed_work(project_name):
#     try:
#         result = frappe.db.sql("""
#             SELECT SUM(area_completed_for_this_submission)
#             FROM `tabProject Attendance`
#             WHERE docstatus = 1 AND project__client = %s
#         """, (project_name,))

#         print("This is query result ",result)
#         print("This is  result 0 0 : ",result[0][0])

#         # Extract the sum from the result (it will be a tuple)
#         total = result[0][0] if result[0][0] is not None else 0

#         return total
#     except Exception as e:
#         # Log any error to help with debugging
#         frappe.log_error(f"Error in get_total_completed_work for project {project_name}: {str(e)}", "get_total_completed_work")
#         return 0





























# # Copyright (c) 2025, Bharat and contributors
# # For license information, please see license.txt

# import frappe
# from frappe import _
# from frappe.model.document import Document


# class ProjectSetup(Document):

#     def before_save(self):
#         self.set_total_completed_work()

#     def set_total_completed_work(self):
#         try:
#             result = frappe.db.sql("""
#                 SELECT SUM(area_completed_for_this_submission)
#                 FROM `tabProject Attendance`
#                 WHERE docstatus = 1 AND project__client = %s
#             """, (self.name,))

#             total = result[0][0] if result[0][0] is not None else 0
#             self.total_compleated_work_till_now = total

#         except Exception as e:
#             frappe.log_error(f"Error updating total completed work for project {self.name}: {str(e)}", "set_total_completed_work")




#     def get_doc_status_label(self):
#         if self.docstatus == 0:
#             return _("Open")
#         elif self.docstatus == 1:
#             return _("Completed")
#         elif self.docstatus == 2:
#             return _("Cancelled")


# @frappe.whitelist()
# def create_user_permission(doc_name):
#     doc = frappe.get_doc("Project Setup", doc_name)

#     if not doc.work_team:
#         frappe.throw(_("Work Team is mandatory to save the Project Setup"))

#     user_permission_exists = frappe.db.exists("User Permission", {
#         "user": doc.team_leader,
#         "allow": "Project Setup",
#         "for_value": doc.name,
#         "project_setup": doc.name
#     })

#     if not user_permission_exists:
#         user_permission = frappe.get_doc({
#             "doctype": "User Permission",
#             "user": doc.team_leader,
#             "allow": "Project Setup",
#             "for_value": doc.name,
#             "project_setup": doc.name,
#             "apply_to_all_doctypes": 1
#         })
#         user_permission.insert(ignore_permissions=True)
#         return _("User Permission created successfully for Project {0}").format(doc.name)
#     else:
#         return _("User Permission already exists for Project {0}").format(doc.name)








# @frappe.whitelist()
# def update_total_completed_work_for_project(project_name):
#     try:
#         result = frappe.db.sql("""
#             SELECT SUM(area_completed_for_this_submission)
#             FROM `tabProject Attendance`
#             WHERE docstatus = 1 AND project__client = %s
#         """, (project_name,))

#         total = result[0][0] if result[0][0] is not None else 0

#         # Update directly in the DB
#         frappe.db.set_value("Project Setup", project_name, "total_compleated_work_till_now", total)

#         # Optional: commit changes
#         frappe.db.commit()

#         return total
#     except Exception as e:
#         frappe.log_error(f"Error in update_total_completed_work_for_project: {str(e)}")
#         return 0
