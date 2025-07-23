# Copyright (c) 2025, bharat and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class TotalCompensation(Document):
	# pass

	@frappe.whitelist()
	def get_projects_by_team(work_team):
		project_list = frappe.get_all("Project Setup", 
			filters={"work_team": work_team}, 
			fields=["name", "work_team", "project_name", "project_customer"]
		)
		
		# enrich with sales_order and customer
		for project in project_list:
			project_doc = frappe.get_doc("Project", project["project_customer"])
			project["sales_order"] = project_doc.custom_sales_order_2 if hasattr(project_doc, "custom_sales_order_2") else ""
			project["customer"] = project_doc.customer if hasattr(project_doc, "customer") else ""

		return project_list
