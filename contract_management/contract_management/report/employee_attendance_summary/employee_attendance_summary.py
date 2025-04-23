# Copyright (c) 2025, bharat and contributors
# For license information, please see license.txt

# import frappe


# def execute(filters=None):
# 	columns, data = [], []
# 	return columns, data








import frappe
from frappe import _

def execute(filters=None):
    # Define columns
    columns = [
        # {"fieldname": "project", "label": _("Project"), "fieldtype": "Link", "options": "Project Setup", "width": 150},
        {"fieldname": "project_name", "label": _("Project Name"), "fieldtype": "Data", "width": 150},
        {"fieldname": "object", "label": _("Object"), "fieldtype": "Link", "options": "Objects", "width": 150},
        # {"fieldname": "team_leader", "label": _("Team Leader ID"), "fieldtype": "Link", "options": "User", "width": 150},
        {"fieldname": "tl_name", "label": _("Team Leader Name"), "fieldtype": "Data", "width": 150},
        # {"fieldname": "employee", "label": _("Employee ID"), "fieldtype": "Link", "options": "Employee", "width": 150},
        {"fieldname": "full_name", "label": _("Employee Name"), "fieldtype": "Data", "width": 150},
        {"fieldname": "total_days", "label": _("Total Days"), "fieldtype": "Int", "width": 120},
        {"fieldname": "total_hours", "label": _("Total Hours"), "fieldtype": "Float", "width": 120},
        {"fieldname": "allowance", "label": _("Allowance"), "fieldtype": "Select", "options": "Yes\nNo", "width": 120}
    ]

    # Fetch data based on filters
    data = get_data(filters)
    
    return columns, data

def get_data(filters):
    conditions = "1=1"  # Default condition
    values = {}

    # Apply filters
    if filters.get("project"):
        conditions += " AND eam.project = %(project)s"
        values["project"] = filters["project"]

    if filters.get("employee"):
        conditions += " AND eam.employee = %(employee)s"
        values["employee"] = filters["employee"]

    if filters.get("team_leader"):
        conditions += " AND eam.team_leader = %(team_leader)s"
        values["team_leader"] = filters["team_leader"]

    if filters.get("from_date") and filters.get("to_date"):
        conditions += " AND eam.date BETWEEN %(from_date)s AND %(to_date)s"
        values["from_date"] = filters["from_date"]
        values["to_date"] = filters["to_date"]

    if filters.get("allowance"):
        conditions += " AND eam.allowance = %(allowance)s"
        values["allowance"] = filters["allowance"]

    # Query to fetch summarized data with additional fields
    data = frappe.db.sql(f"""
        SELECT
            eam.project,
            eam.project_name,
            eam.object,
            eam.team_leader,
            eam.tl_name,
            eam.employee,
            eam.full_name,
            COUNT(DISTINCT eam.date) AS total_days,
            SUM(CAST(eam.duration AS DECIMAL)) AS total_hours,
            eam.allowance
        FROM
            `tabEmployee Attendance Master` eam
        WHERE
            eam.present = 'Yes' AND {conditions}
        GROUP BY
            eam.project, eam.employee
        ORDER BY
            eam.project, eam.employee
    """, values, as_dict=True)

    return data
