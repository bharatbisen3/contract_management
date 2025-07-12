# Copyright (c) 2025, bharat and contributors
# For license information, please see license.txt

# import frappe


# def execute(filters=None):
# 	columns, data = [], []
# 	return columns, data






import frappe

def execute(filters=None):
    columns = [
        {"fieldname": "project", "label": "Project", "fieldtype": "Link", "options": "Project Setup", "width": 200},
        {"fieldname": "project_name", "label": "Project Name", "fieldtype": "Data", "width": 200},
        {"fieldname": "attendance_count", "label": "Attendance Count", "fieldtype": "Int", "width": 150}
    ]

    conditions = "WHERE ea.present = 'Yes'"
    values = {}

    if filters.get("project"):
        conditions += " AND ea.project = %(project)s"
        values["project"] = filters.get("project")

    if filters.get("from_date") and filters.get("to_date"):
        conditions += " AND ea.date BETWEEN %(from_date)s AND %(to_date)s"
        values["from_date"] = filters.get("from_date")
        values["to_date"] = filters.get("to_date")

    data = frappe.db.sql(f"""
        SELECT 
            ea.project, 
            ea.project_name,
            COUNT(ea.name) AS attendance_count
        FROM `tabEmployee Attendance Master` ea
        {conditions}
        GROUP BY ea.project, ea.project_name
        ORDER BY ea.project ASC
    """, values, as_dict=True)

    return columns, data
