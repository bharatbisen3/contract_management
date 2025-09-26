# # # Copyright (c) 2025, bharat and contributors
# # # For license information, please see license.txt

# # # import frappe
# # from frappe.model.document import Document


# # class TotalCompensation(Document):
# # 	pass











import frappe
from frappe.model.document import Document
from frappe.utils import get_first_day, get_last_day
import calendar


# # ✅ Reuse your already-working logic from Net Compensation
# from contract_management.contract_management.doctype.net_compensation.net_compensation import (
#     get_employee_attendance,
# )

class TotalCompensation(Document):



    def on_submit(self):
        self.generate_payroll_slips()


    def generate_payroll_slips(self):

        month_num, year_val = self.get_month_year()

        from_date = get_first_day(f"{year_val}-{month_num:02d}-01")
        to_date = get_last_day(f"{year_val}-{month_num:02d}-01")


        for item in self.net_compensation:  # each Net Compensation Item = one slip
            payroll_slip = frappe.new_doc("Payroll Slip")
            payroll_slip.total_compensation = self.name
            payroll_slip.employee = item.employee
            payroll_slip.employee_name = frappe.db.get_value("Employee", item.employee, "employee_name")
            payroll_slip.work_team = self.work_team
            payroll_slip.team_leader = self.team_leader
            payroll_slip.month = self.month
            payroll_slip.year = self.year
            payroll_slip.from_date = from_date
            payroll_slip.to_date = to_date

            # --- Earnings Breakdown ---
            # 020 Piecework
            payroll_slip.append("earnings_table", {
                "salary_type": 20,
                "description": "Piecework",
                "from_date": from_date,
                "to_date": to_date,
                "number_of_units": 1,
                "rate_sek": item.piecework_compensation or 0,
                "total_amount": item.piecework_compensation or 0,
            })

            # Piecework Hours Pay (same salary_type group as 020, just description)
            payroll_slip.append("earnings_table", {
                "description": "Piecework Hours Pay",
                "from_date": from_date,
                "to_date": to_date,
                "number_of_units": item.total_hours or 0,
                "rate_sek": (item.piecework_compensation / (item.total_hours or 1)) if item.total_hours else 0,
                "total_amount": 0  # this line is explanatory, no total
            })

            # 021 Holiday Compensation
            payroll_slip.append("earnings_table", {
                "salary_type": 21,
                "description": "Holiday Comp. 13 %",
                "from_date": from_date,
                "to_date": to_date,
                "number_of_units": 1,
                "rate_sek": item.holiday_compensation_13 or 0,
                "total_amount": item.holiday_compensation_13 or 0,
            })

            # 022 Reduction in Working Hours
            payroll_slip.append("earnings_table", {
                "salary_type": 22,
                "description": "Red. in Working Hours 3,62 %",
                "from_date": from_date,
                "to_date": to_date,
                "number_of_units": 1,
                "rate_sek": item.reduction_in_working_hours_362 or 0,
                "total_amount": item.reduction_in_working_hours_362 or 0,
            })

            # 301 Daily Allowance
            payroll_slip.append("earnings_table", {
                "salary_type": 301,
                "description": "Daily Allowance",
                "from_date": from_date,
                "to_date": to_date,
                "number_of_units": item.attendance or 0,
                "rate_sek": item.daily_allowance_rate_sek or 0,
                "total_amount": item.daily_allowance_total_sek or 0,
            })

            # --- Totals ---
            gross_salary = (
                (item.piecework_compensation or 0) +
                (item.holiday_compensation_13 or 0) +
                (item.reduction_in_working_hours_362 or 0)
            )

            payroll_slip.gross_salary = gross_salary
            payroll_slip.tax = item.tax_amount or 0
            payroll_slip.tax_free_compensation = item.daily_allowance_total_sek or 0
            payroll_slip.payment = (
                gross_salary
                - (item.tax_amount or 0)
                + (item.daily_allowance_total_sek or 0)
            )

            payroll_slip.insert(ignore_permissions=True)

        frappe.db.commit()




    def get_month_year(self):
        """Return actual calendar month (1-12) and year (int) from fiscal year + month"""
        month_num = list(calendar.month_name).index(self.month)  # "September" -> 9

        # Split fiscal year string (e.g. "2025-2026")
        start_year, end_year = map(int, self.year.split("-"))

        # If fiscal year starts in April
        if month_num >= 4:  # Apr-Dec → belongs to start year
            return month_num, start_year
        else:  # Jan-Mar → belongs to end year
            return month_num, end_year




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
