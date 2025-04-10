import frappe

@frappe.whitelist()
def create_user_permission(project_name, user):
    if not frappe.db.exists("User Permission", {
        # "user": user,
        # "allow": "Project Setup",
        "for_value": project_name
    }):
        try:
            user_permission = frappe.get_doc({
                "doctype": "User Permission",
                "user": user,
                "allow": "Work Team",
                "for_value": project_name,
                "apply_to_all_doctypes": 1
            })
            user_permission.insert(ignore_permissions=True)
            return {"status": "success", "message": f"User Permission created for {user} on project {project_name}"}
        except Exception as e:
            frappe.log_error(f"Error creating User Permission: {str(e)}", "User Permission Error")
            return {"status": "error", "message": str(e)}
