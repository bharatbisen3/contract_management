# # Copyright (c) 2025, bharat and contributors
# # For license information, please see license.txt

# # import frappe
# from frappe.model.document import Document


# class ProjectSetup(Document):
# 	pass








import frappe
from frappe import _
from frappe.model.document import Document
# from frappe.utils import get_url

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


# import frappe
# from frappe.utils import get_url
@frappe.whitelist()
def send_open_project_reminders():
    open_projects = frappe.get_all(
        "Project Setup",
        filters={"status": "Open"},
        fields=["name", "team_leader", "object"]
    )

    for project in open_projects:
        if not project.team_leader:
            continue

        subject = f"Reminder: Attendance for Project '{project.name}'"
        message = f"""
        Dear Team Leader,<br><br>
        
        Kindly log attendance upto last week for the project you have been assigned<br>
        Thank You!<br><br>

        HR Department<br>
        Ljunganforestry
        """

        frappe.sendmail(
            recipients=project.team_leader,
            subject=subject,
            message=message,
            delayed=False

        )





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


