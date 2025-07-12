# # # Copyright (c) 2025, bharat and contributors
# # # For license information, please see license.txt

# # # import frappe
# # from frappe.model.document import Document


# # class WorkTeam(Document):
# # 	pass




# import frappe
# from frappe.model.document import Document
# from frappe import _

# class WorkTeam(Document):
#     pass

# @frappe.whitelist()
# def create_team_leader_user_permission(doc_name):
#     doc = frappe.get_doc("Work Team", doc_name)

#     if not doc.team_leader:
#         frappe.throw(_("Team Leader is mandatory to assign user permission."))

#     user_permission_exists = frappe.db.exists("User Permission", {
#         "user": doc.team_leader,
#         "allow": "Work Team",
#         "for_value": doc.name,
#     })

#     if not user_permission_exists:
#         user_permission = frappe.get_doc({
#             "doctype": "User Permission",
#             "user": doc.team_leader,
#             "allow": "Work Team",
#             "for_value": doc.name,
#             "apply_to_all_doctypes": 1
#         })
#         user_permission.insert(ignore_permissions=True)
#         # frappe.msgprint(_("User Permission created successfully for Work Team {0}").format(doc.name))
#         return True
#     else:
#         # frappe.msgprint(_("User Permission already exists for Work Team {0}").format(doc.name))
#         return False



# Copyright (c) 2025, bharat and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _


class WorkTeam(Document):
    def after_insert(self):
        try:
            # frappe.msgprint(_("Running after_insert hook"))
            create_user_permissions_for_team(self)
        except Exception as e:
            frappe.log_error(frappe.get_traceback(), "WorkTeam insert error")
            frappe.msgprint(_("Error Unable to insert work team: ") + str(e))

    def on_update(self):
        try:
            # frappe.msgprint(_("Running on_update hook"))
            create_user_permissions_for_team(self)
        except Exception as e:
            frappe.log_error(frappe.get_traceback(), "WorkTeam update error")
            frappe.msgprint(_("Error unable to update: ") + str(e))


def create_user_permissions_for_team(doc):
    """Create user permissions for each employee under the team leader"""
    if not doc.team_leader:
        frappe.msgprint(_("No team leader set. Skipping permission creation."))
        return

    if not doc.get("team_members_list"):
        frappe.msgprint(_("No team members found."))
        return

    created = 0
    skipped = 0

    for row in doc.team_members_list:
        employee_id = row.employee_id

        if not employee_id:
            skipped += 1
            continue

        try:
            user_permission_exists = frappe.db.exists("User Permission", {
                "user": doc.team_leader,
                "allow": "Employee",
                "for_value": employee_id
            })

            if not user_permission_exists:
                user_permission = frappe.get_doc({
                    "doctype": "User Permission",
                    "user": doc.team_leader,
                    "allow": "Employee",
                    "for_value": employee_id,
                    "apply_to_all_doctypes": 1
                })
                user_permission.insert(ignore_permissions=True)
                created += 1

                # Log and notify
                # frappe.msgprint(
                #     _("User Permission created: Team Leader {0} -> Employee {1}")
                #     .format(doc.team_leader, employee_id)
                # )
            else:
                skipped += 1
        except Exception as e:
            frappe.log_error(frappe.get_traceback(), f"Failed to create permission for Employee {employee_id}")
            frappe.msgprint(_("Error while creating permission for Employee {0}: {1}")
                            .format(employee_id, str(e)))

    # frappe.msgprint(_("{0} User Permissions created. {1} skipped.").format(created, skipped))


# ----- Your existing working code below (kept untouched) -----

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
        return True
    else:
        return False
