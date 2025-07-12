# Copyright (c) 2025, bharat and contributors
# For license information, please see license.txt

# import frappe


# def execute(filters=None):
# 	columns, data = [], []
# 	return columns, data




import frappe

def execute(filters=None):
    # Get total number of teams
    total_teams = frappe.db.count("Work Team")

    # Get team-wise member count
    team_data = frappe.db.sql("""
        SELECT 
            wt.name AS team_name,
            COUNT(tm.name) AS member_count
        FROM `tabWork Team` wt
        LEFT JOIN `tabTeam Members List` tm ON tm.parent = wt.name
        GROUP BY wt.name
        ORDER BY wt.name ASC
    """, as_dict=True)

    # Calculate total members
    total_members = sum(team["member_count"] for team in team_data)

    # Define columns
    columns = [
        {"fieldname": "team_name", "label": "Team Name", "fieldtype": "Data", "width": 200},
        {"fieldname": "member_count", "label": "Number of Members", "fieldtype": "Int", "width": 150}
    ]

    # Add total row at the top
    data = [{"team_name": "Total Work Teams", "member_count": total_teams}]
    data.extend(team_data)
    # data.append({"team_name": "Total", "member_count": total_members})

    return columns, data
