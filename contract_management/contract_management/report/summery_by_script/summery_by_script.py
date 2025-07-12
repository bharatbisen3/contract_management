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
        {"fieldname": "project", "label": _("Project"), "fieldtype": "Link", "options": "Project Setup", "width": 150},
        {"fieldname": "employee", "label": _("Employee"), "fieldtype": "Link", "options": "Employee", "width": 150},
        {"fieldname": "total_days", "label": _("Total Days"), "fieldtype": "Int", "width": 120},
        {"fieldname": "total_hours", "label": _("Total Hours"), "fieldtype": "Float", "width": 120}
    ]

    # Fetch data
    data = get_data(filters)
    return columns, data

def get_data(filters):
    # Query to fetch summarized data
    data = frappe.db.sql("""
        SELECT
            project,
            employee,
            COUNT(DISTINCT date) AS total_days,
            SUM(CAST(duration AS DECIMAL)) AS total_hours
        FROM
            `tabEmployee Attendance Master`
        WHERE
            present = 'Yes'
        GROUP BY
            project, employee
        ORDER BY
            project, employee
    """, as_dict=True)

    return data