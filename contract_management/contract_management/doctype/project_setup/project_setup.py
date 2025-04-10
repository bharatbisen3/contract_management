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
