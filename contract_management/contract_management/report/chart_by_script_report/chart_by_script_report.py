import frappe

def execute(filters=None):
    columns = [
        {"label": "Project", "fieldname": "project", "fieldtype": "Link", "options": "Project Setup", "width": 150},
        {"label": "Project Name", "fieldname": "project_name", "fieldtype": "Data", "width": 200},
        {"label": "Employee", "fieldname": "employee", "fieldtype": "Link", "options": "Employee", "width": 150},
        {"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data", "width": 200},
        {"label": "Total Days Present", "fieldname": "total_days", "fieldtype": "Int", "width": 100},
        {"label": "Team Leader", "fieldname": "team_leader", "fieldtype": "Link", "options": "User", "width": 150},
        {"label": "Team Leader Name", "fieldname": "tl_name", "fieldtype": "Data", "width": 200}
    ]

    conditions = "eam.present = 'Yes'"
    if filters.get("month") and filters.get("year"):
        conditions += f" AND MONTH(eam.date) = {filters['month']} AND YEAR(eam.date) = {filters['year']}"

    data = frappe.db.sql(f"""
        SELECT 
            eam.project AS project,
            ps.project__object_name AS project_name,
            eam.employee AS employee,
            eam.full_name AS employee_name,
            COUNT(eam.name) AS total_days,
            eam.team_leader AS team_leader,
            eam.tl_name AS tl_name
        FROM `tabEmployee Attendance Master` eam
        LEFT JOIN `tabProject Setup` ps ON eam.project = ps.name
        WHERE {conditions}
        GROUP BY eam.project, ps.project__object_name, eam.employee, eam.full_name, eam.team_leader, eam.tl_name
        ORDER BY eam.project, COUNT(eam.name) DESC
    """, as_dict=True)

    return columns, data
