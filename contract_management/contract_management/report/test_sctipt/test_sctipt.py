# # Copyright (c) 2025, bharat and contributors
# # For license information, please see license.txt

# # import frappe


# def execute(filters=None):
# 	columns, data = [], []
# 	return columns, data





# Copyright (c) 2025, bharat and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"fieldname": "name", "label": _("Project ID"), "fieldtype": "Link", "options": "Project Setup", "width": 120},
        {"fieldname": "project_name", "label": _("Project Name"), "fieldtype": "Data", "width": 200},
        {"fieldname": "work_team", "label": _("Work Team"), "fieldtype": "Link", "options": "Work Team", "width": 120},
        {"fieldname": "team_leader", "label": _("Team Leader"), "fieldtype": "Link", "options": "User", "width": 120},
        {"fieldname": "status", "label": _("Status"), "fieldtype": "Data", "width": 100},
        {"fieldname": "completion_date", "label": _("Completion Date"), "fieldtype": "Date", "width": 100},
        {"fieldname": "completion_month", "label": _("Completion Month"), "fieldtype": "Data", "width": 120}
    ]

def get_data(filters):
    conditions = get_conditions(filters)
    
    query = """
        SELECT
            ps.name,
            ps.project_name,
            ps.work_team,
            ps.team_leader,
            ps.status,
            ps.completion_date,
            CONCAT(MONTHNAME(ps.completion_date), ' ', YEAR(ps.completion_date)) AS completion_month
        FROM
            `tabProject Setup` ps
        WHERE
            ps.status = 'Completed'
            AND ps.name NOT IN (
                SELECT col.object
                FROM `tabCompleted Objects List` col
                INNER JOIN `tabTotal Compensation` tc
                ON col.parent = tc.name
                WHERE tc.docstatus = 1
            )
            AND {conditions}
        ORDER BY ps.completion_date DESC
    """.format(conditions=conditions)
    
    data = frappe.db.sql(query, as_dict=1)
    return data

def get_conditions(filters):
    conditions = []
    
    # Base condition for completed projects not in compensation
    conditions.append("ps.status = 'Completed'")
    
    # Month filter condition
    if filters and filters.get('completion_month'):
        completion_month = filters.get('completion_month')
        conditions.append(f"MONTHNAME(ps.completion_date) = '{completion_month}'")
    else:
        # Default to previous month
        conditions.append("""
            MONTH(ps.completion_date) = MONTH(DATE_SUB(CURDATE(), INTERVAL 1 MONTH))
            AND YEAR(ps.completion_date) = YEAR(DATE_SUB(CURDATE(), INTERVAL 1 MONTH))
        """)
    
    return " AND ".join(conditions)