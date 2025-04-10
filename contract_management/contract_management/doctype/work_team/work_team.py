# # Copyright (c) 2025, bharat and contributors
# # For license information, please see license.txt

# # import frappe
# from frappe.model.document import Document


# class WorkTeam(Document):
# 	pass





# Copyright (c) 2025, bharat and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _

class WorkTeam(Document):
    pass

@frappe.whitelist()
def create_team_leader_user_permission(doc_name):
    doc = frappe.get_doc("Work Team", doc_name)

    if not doc.team_leader:
        frappe.throw(_("Team Leader is mandatory to assign user permission."))

    user_permission_exists = frappe.db.exists("User Permission", {
        "user": doc.team_leader,
        "allow": "Work Team",
        "for_value": doc.name,
    })

    if not user_permission_exists:
        user_permission = frappe.get_doc({
            "doctype": "User Permission",
            "user": doc.team_leader,
            "allow": "Work Team",
            "for_value": doc.name,
            "apply_to_all_doctypes": 1
        })
        user_permission.insert(ignore_permissions=True)
        # frappe.msgprint(_("User Permission created successfully for Work Team {0}").format(doc.name))
        return True
    else:
        # frappe.msgprint(_("User Permission already exists for Work Team {0}").format(doc.name))
        return False













# @frappe.whitelist()
# def create_team_leader_user_permission(user, doctype, docname):
#     # Avoid duplicates
#     if not frappe.db.exists("User Permission", {
#         "user": user,
#         "allow": doctype,
#         "for_value": docname
#     }):
#         add_user_permission(user=user, doctype=doctype, name=docname, applicable_for=doctype, apply_to_all_doctypes=0)
#         return {"status": "success"}
#     else:
#         return {"status": "exists"}

