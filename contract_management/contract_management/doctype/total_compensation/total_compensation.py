# # # # Copyright (c) 2025, bharat and contributors
# # # # For license information, please see license.txt

# # # # import frappe
# # # from frappe.model.document import Document


# # # class TotalCompensation(Document):
# # # 	pass









# import frappe
# from frappe.model.document import Document
# from frappe.utils import get_first_day, get_last_day


# # ✅ Reuse your already-working logic from Net Compensation
# from contract_management.contract_management.doctype.net_compensation.net_compensation import (
#     get_employee_attendance,
# )

# class TotalCompensation(Document):

#     @frappe.whitelist()
#     def generate_net_compensation(self):
#         """
#         Fill the 'net_compensation' child table by reusing the existing calculation
#         from Net Compensation (get_employee_attendance). No JS needed; this is
#         called by your button via run_doc_method.
#         """

#         if not (self.year and self.month):
#             frappe.throw("Please set Fiscal Year and Month before generating Net Compensation.")

#         # Start fresh to avoid duplicates on re-run
#         self.set("net_compensation", [])

#         # Iterate the already-aggregated per-employee piecework rows
#         # (employee_compensetion_summery -> Emp Summery child table on this Doc)
#         for row in (self.employee_compensetion_summery or []):
#             emp = row.employee_id

#             # 🔁 Reuse your working server logic; it already:
#             # - handles FY like "2025-2026"
#             # - computes unique attendance days, total_hours
#             # - fetches Daily Allowance (year) and Emp Summery piecework
#             # - calculates 13%, 3.62%, gross, tax(30%), totals
#             data = get_employee_attendance(emp, self.month, self.year) or {}

#             # Append to the Net Compensation Item child table (same schema you use elsewhere)
#             self.append("net_compensation", {
#                 "employee": emp,
#                 "attendance": data.get("attendance", 0),
#                 "total_hours": data.get("total_hours", 0),
#                 "daily_allowance_rate_sek": data.get("daily_allowance_rate", 0),
#                 "daily_allowance_total_sek": data.get("daily_allowance_total_sek", 0),
#                 "piecework_compensation": data.get("piecework_compensation", 0),
#                 "holiday_compensation_13": data.get("holiday_compensation_13", 0),
#                 "reduction_in_working_hours_362": data.get("reduction_in_working_hours_362", 0),
#                 "gross_salary_total": data.get("gross_salary_total", 0),
#                 # keep tax % aligned with your existing calc (30%)
#                 "tax_percentage": 30,
#                 "tax_amount": data.get("tax_amount", 0),
#                 "net_compensation_excluding_daily_allowance": data.get("net_compensation_excluding_daily_allowance", 0),
#                 "total_net_compensation": data.get("total_net_compensation", 0),
#             })

#         self.save()
#         frappe.msgprint("Net Compensation calculated and filled successfully.")



#     def on_submit(self):
#         self.generate_payroll_slips()

#     def generate_payroll_slips(self):
#         for item in self.net_compensation:  # use Net Compensation Item table
#             payroll_slip = frappe.new_doc("Payroll Slip")
#             payroll_slip.total_compensation = self.name
#             payroll_slip.employee = item.employee
#             payroll_slip.employee_name = frappe.db.get_value("Employee", item.employee, "employee_name")
#             payroll_slip.work_team = self.work_team
#             payroll_slip.team_leader = self.team_leader
#             payroll_slip.month = self.month
#             payroll_slip.year = self.year

#             # Earnings breakdown
#             payroll_slip.append("earnings_table", {
#                 "description": "Piecework",
#                 "number_of_units": item.total_hours or 0,
#                 "total_amount": item.piecework_compensation
#             })

#             payroll_slip.append("earnings_table", {
#                 "description": "Holiday Comp. 13 %",
#                 "total_amount": item.holiday_compensation_13 or 0
#             })

#             payroll_slip.append("earnings_table", {
#                 "description": "Red. in Working Hours 3,62 %",
#                 "total_amount": item.reduction_in_working_hours_362 or 0
#             })

#             payroll_slip.append("earnings_table", {
#                 "description": "Daily Allowance",
#                 "number_of_units": item.attendance or 0,
#                 "rate_sek": item.daily_allowance_rate_sek or 0,
#                 "total_amount": item.daily_allowance_total_sek or 0
#             })

#             # Totals
#             payroll_slip.gross_salary = item.gross_salary_total or 0
#             payroll_slip.tax = item.tax_amount or 0
#             payroll_slip.tax_free_compensation = item.daily_allowance_total_sek or 0
#             payroll_slip.payment = item.total_net_compensation or 0

#             payroll_slip.insert(ignore_permissions=True)

#         frappe.db.commit()














# # # Copyright (c) 2025, bharat and contributors
# # # For license information, please see license.txt

# # # import frappe
# # from frappe.model.document import Document


# # class TotalCompensation(Document):
# # 	pass









import frappe
from frappe.model.document import Document
from frappe.utils import get_first_day, get_last_day


# ✅ Reuse your already-working logic from Net Compensation
from contract_management.contract_management.doctype.net_compensation.net_compensation import (
    get_employee_attendance,
)

class TotalCompensation(Document):

    # @frappe.whitelist()
    # def generate_net_compensation(self):
    #     """
    #     Fill the 'net_compensation' child table by reusing the existing calculation
    #     from Net Compensation (get_employee_attendance). No JS needed; this is
    #     called by your button via run_doc_method.
    #     """

    #     if not (self.year and self.month):
    #         frappe.throw("Please set Fiscal Year and Month before generating Net Compensation.")

    #     # Start fresh to avoid duplicates on re-run
    #     self.set("net_compensation", [])

    #     # Iterate the already-aggregated per-employee piecework rows
    #     # (employee_compensetion_summery -> Emp Summery child table on this Doc)
    #     for row in (self.employee_compensetion_summery or []):
    #         emp = row.employee_id

    #         # 🔁 Reuse your working server logic; it already:
    #         # - handles FY like "2025-2026"
    #         # - computes unique attendance days, total_hours
    #         # - fetches Daily Allowance (year) and Emp Summery piecework
    #         # - calculates 13%, 3.62%, gross, tax(30%), totals
    #         data = get_employee_attendance(emp, self.month, self.year) or {}

    #         # Append to the Net Compensation Item child table (same schema you use elsewhere)
    #         self.append("net_compensation", {
    #             "employee": emp,
    #             "attendance": data.get("attendance", 0),
    #             "total_hours": data.get("total_hours", 0),
    #             "daily_allowance_rate_sek": data.get("daily_allowance_rate", 0),
    #             "daily_allowance_total_sek": data.get("daily_allowance_total_sek", 0),
    #             "piecework_compensation": data.get("piecework_compensation", 0),
    #             "holiday_compensation_13": data.get("holiday_compensation_13", 0),
    #             "reduction_in_working_hours_362": data.get("reduction_in_working_hours_362", 0),
    #             "gross_salary_total": data.get("gross_salary_total", 0),
    #             # keep tax % aligned with your existing calc (30%)
    #             "tax_percentage": 30,
    #             "tax_amount": data.get("tax_amount", 0),
    #             "net_compensation_excluding_daily_allowance": data.get("net_compensation_excluding_daily_allowance", 0),
    #             "total_net_compensation": data.get("total_net_compensation", 0),
    #         })

    #     self.save()
    #     frappe.msgprint("Net Compensation calculated and filled successfully.")



    def on_submit(self):
        self.generate_payroll_slips()

    def generate_payroll_slips(self):
        for item in self.net_compensation:  # use Net Compensation Item table
            payroll_slip = frappe.new_doc("Payroll Slip")
            payroll_slip.total_compensation = self.name
            payroll_slip.employee = item.employee
            payroll_slip.employee_name = frappe.db.get_value("Employee", item.employee, "employee_name")
            payroll_slip.work_team = self.work_team
            payroll_slip.team_leader = self.team_leader
            payroll_slip.month = self.month
            payroll_slip.year = self.year

            # Earnings breakdown
            payroll_slip.append("earnings_table", {
                "description": "Piecework",
                "number_of_units": item.total_hours or 0,
                "total_amount": item.piecework_compensation
            })

            payroll_slip.append("earnings_table", {
                "description": "Holiday Comp. 13 %",
                "total_amount": item.holiday_compensation_13 or 0
            })

            payroll_slip.append("earnings_table", {
                "description": "Red. in Working Hours 3,62 %",
                "total_amount": item.reduction_in_working_hours_362 or 0
            })

            payroll_slip.append("earnings_table", {
                "description": "Daily Allowance",
                "number_of_units": item.attendance or 0,
                "rate_sek": item.daily_allowance_rate_sek or 0,
                "total_amount": item.daily_allowance_total_sek or 0
            })

            # Totals
            payroll_slip.gross_salary = item.gross_salary_total or 0
            payroll_slip.tax = item.tax_amount or 0
            payroll_slip.tax_free_compensation = item.daily_allowance_total_sek or 0
            payroll_slip.payment = item.total_net_compensation or 0

            payroll_slip.insert(ignore_permissions=True)

        frappe.db.commit()




# total_compensation.py


@frappe.whitelist()
def get_employee_attendance(from_date=None, to_date=None, employee=None):
    """
    Fetch attendance details from Employee Attendance Master.
    Returns raw rows and aggregated summary per employee.
    """

    filters = {}
    if from_date and to_date:
        filters["date"] = ["between", [from_date, to_date]]
    if employee:
        filters["employee"] = employee

    records = frappe.get_all(
        "Employee Attendance Master",
        filters=filters,
        fields=[
            "employee",
            "full_name",
            "date",
            "duration",
            "present",
            "allowance",
            "project",
            "project_name",
            "team_leader",
            "tl_name"
        ],
        order_by="date asc"
    )

    # Convert Yes/No → boolean
    for r in records:
        r["present"] = 1 if r.get("present") == "Yes" else 0
        r["allowance"] = 1 if r.get("allowance") == "Yes" else 0
        # Cast duration to int
        try:
            r["duration"] = int(r["duration"]) if r.get("duration") else 0
        except:
            r["duration"] = 0

    # Group summary by employee
    summary = {}
    for r in records:
        emp = r["employee"]
        if emp not in summary:
            summary[emp] = {
                "employee": emp,
                "full_name": r["full_name"],
                "total_days": 0,
                "total_hours": 0,
                "allowance_days": 0,
                "attendance_records": []
            }
        summary[emp]["attendance_records"].append(r)
        summary[emp]["total_hours"] += r["duration"] or 0
        if r["present"]:
            summary[emp]["total_days"] += 1
        if r["allowance"]:
            summary[emp]["allowance_days"] += 1

    return {
        "records": records,
        "summary": list(summary.values())
    }
