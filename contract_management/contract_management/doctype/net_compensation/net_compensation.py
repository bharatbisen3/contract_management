# # # Copyright (c) 2025, bharat and contributors
# # # For license information, please see license.txt

# # # import frappe
# # from frappe.model.document import Document


# # class NetCompensation(Document):
# # 	pass










import frappe
from frappe.model.document import Document
from frappe import _
# from frappe.utils import getdate, get_first_day, get_last_day
from frappe.utils import flt, get_first_day, get_last_day, getdate
import calendar

class NetCompensation(Document):
	pass


@frappe.whitelist()
def get_employees_by_work_team(work_team):
    """Get all employees in a work team"""
    employees = frappe.get_all('Team Members List',
        filters={'parent': work_team},
        fields=['employee_id as employee']
    )
    return employees

@frappe.whitelist()
def get_employee_attendance(employee, month, year):
    # Extract first year if fiscal year format is "2025-2026"
    if '-' in str(year):
        year = str(year).split('-')[0]

    # import calendar
    # from frappe.utils import getdate, get_first_day, get_last_day

    month_number = list(calendar.month_name).index(month)
    first_day = get_first_day(getdate(f"{year}-{month_number:02d}-01"))
    last_day = get_last_day(first_day)

    # Attendance records
    attendance_records = frappe.get_all('Employee Attendance Master',
        filters={
            'employee': employee,
            'date': ['between', [first_day, last_day]],
            'present': 'Yes'
        },
        fields=['date', 'duration']
    )

    unique_days = len(set(record.date for record in attendance_records))
    total_hours = sum(flt(record.duration or 0) for record in attendance_records)

    # Daily allowance
    daily_allowance_rate = get_daily_allowance_rate(year)

    # --- Fetch Clearing & Planting Compensation from Emp Summery ---
    clearing = planting = 0
    emp_summary = frappe.get_all(
        "Emp Summery",
        filters={"employee_id": employee},
        fields=["clearing_compensation", "planting_compensation"]
    )
    if emp_summary:
        clearing = emp_summary[0].clearing_compensation or 0
        planting = emp_summary[0].planting_compensation or 0

    piecework_comp = clearing + planting

    # ✅ New formulas
    net_excl_da = piecework_comp
    total_net = net_excl_da + (unique_days * daily_allowance_rate)
    hol_comp = piecework_comp * 0.13
    reduc_work = round(piecework_comp * 0.0362)
    gsl = piecework_comp + hol_comp + reduc_work

    return {
        "attendance": unique_days,
        "total_hours": total_hours,
        "daily_allowance_rate": daily_allowance_rate,
        "daily_allowance_total_sek": unique_days * daily_allowance_rate,
        "clearing_compensation": clearing,
        "planting_compensation": planting,
        "total_net_compensation": total_net,
        "net_compensation_excluding_daily_allowance": net_excl_da,
        "piecework_compensation": piecework_comp,
        "holiday_compensation_13": hol_comp,
        "reduction_in_working_hours_362": reduc_work,
        "gross_salary_total": gsl,
        "tax_amount": gsl * 0.3
    }




def get_daily_allowance_rate(year):
    """Get the full day daily allowance rate for the given year"""
    daily_allowance = frappe.get_all('Daily Allowance',
        filters={'income_year': year},
        fields=['full_day'],
        order_by='creation desc',
        limit=1
    )
    
    if daily_allowance:
        return daily_allowance[0].full_day
    else:
        frappe.throw(_("Daily Allowance rate not found for year {0}").format(year))


MONTH_MAP = {
    "January": 1, "February": 2, "March": 3, "April": 4,
    "May": 5, "June": 6, "July": 7, "August": 8,
    "September": 9, "October": 10, "November": 11, "December": 12
}

def _month_period_from_fiscal_year(fiscal_year_name: str, month_label: str):
    """
    Given Fiscal Year doc (with year_start_date/year_end_date) and a Month label,
    return (from_date, to_date) for that calendar month within the FY window.
    Handles FY that don't start on January 1.

    e.g., FY 2025-04-01 .. 2026-03-31 + "April" -> 2025-04-01 .. 2025-04-30
          FY 2025-04-01 .. 2026-03-31 + "January" -> 2026-01-01 .. 2026-01-31
    """
    fy = frappe.get_doc("Fiscal Year", fiscal_year_name)
    start = getdate(fy.year_start_date)
    end   = getdate(fy.year_end_date)
    m = MONTH_MAP.get(month_label)
    if not m:
        frappe.throw(f"Invalid month '{month_label}'. Expected one of: {', '.join(MONTH_MAP.keys())}")

    # Decide which calendar year this month falls into inside the FY
    year_for_month = start.year if m >= start.month else start.year + 1

    # Build first/last day of that month
    last_day = calendar.monthrange(year_for_month, m)[1]
    from_dt = date(year_for_month, m, 1)
    to_dt   = date(year_for_month, m, last_day)

    # Safety clamp inside FY window (should normally already be inside)
    if from_dt < start: from_dt = start
    if to_dt   > end:   to_dt   = end
    return from_dt, to_dt

def _safe_curr(val):
    return float(val) if (val is not None and val != "") else 0.0

def on_submit(doc, method):
    try:
        frappe.log_error(f"[{doc.name}] Start generating Payroll Slips", "Payroll Debug")

        # Resolve monthly period from FY + Month
        try:
            period_from, period_to = _month_period_from_fiscal_year(doc.year, doc.month)
        except Exception:
            frappe.log_error(f"[{doc.name}] Failed to resolve month period: {frappe.get_traceback()}", "Payroll Slip Error")
            # Fallback: use FY start/end to avoid total failure
            fy = frappe.get_doc("Fiscal Year", doc.year)
            period_from, period_to = getdate(fy.year_start_date), getdate(fy.year_end_date)

        for item in doc.compensation:
            try:
                frappe.log_error(f"[{doc.name}] Employee {item.employee}: start", "Payroll Debug")

                # Read inputs safely
                piecework                  = _safe_curr(getattr(item, "piecework_compensation", 0))
                holiday_13                 = _safe_curr(getattr(item, "holiday_compensation_13", 0))
                reduction_362              = _safe_curr(getattr(item, "reduction_in_working_hours_362", 0))
                attendance_days            = _safe_curr(getattr(item, "attendance", 0))
                daily_allow_rate           = _safe_curr(getattr(item, "daily_allowance_rate_sek", 0))
                daily_allow_total_row      = _safe_curr(getattr(item, "daily_allowance_total_sek", 0))
                total_hours                = _safe_curr(getattr(item, "total_hours", 0))
                tax_amount                 = _safe_curr(getattr(item, "tax_amount", 0))

                # Compute Daily Allowance total ourselves to ensure correctness
                daily_allow_total_calc = attendance_days * daily_allow_rate
                if abs(daily_allow_total_calc - daily_allow_total_row) > 0.005:
                    frappe.log_error(
                        f"[{doc.name}] {item.employee}: Daily Allowance mismatch. "
                        f"calc={daily_allow_total_calc} vs row={daily_allow_total_row}",
                        "Payroll Debug"
                    )

                # Compute per-hour rate for "Piecework Hours Pay"
                # Assumption: rate_per_hour = piecework_total / total_hours  (common approach)
                rate_per_hour = 0.0
                if total_hours > 0:
                    rate_per_hour = piecework / total_hours
                else:
                    if piecework and total_hours == 0:
                        frappe.log_error(f"[{doc.name}] {item.employee}: total_hours is 0; cannot compute hourly rate", "Payroll Debug")

                # Derived totals
                gross_salary = piecework + holiday_13 + reduction_362
                tax_free_comp = daily_allow_total_calc
                # If your tax is a deduction stored as positive number, keep '-' below.
                # If you already store tax as negative, you can replace with: payment = gross_salary + tax_free_comp + tax_amount
                payment = gross_salary + tax_free_comp - tax_amount

                # Create Payroll Slip
                payroll = frappe.new_doc("Payroll Slip")
                payroll.employee = item.employee
                payroll.employee_name = frappe.db.get_value("Employee", item.employee, "employee_name")
                payroll.net_compensation = doc.name
                payroll.work_team = doc.work_team
                payroll.team_leader = doc.team_leader
                payroll.month = doc.month
                payroll.year = doc.year
                payroll.from_date = period_from
                payroll.to_date = period_to

                # ===== Child rows (Payroll Slip Item) =====
                # 020 Piecework
                if piecework:
                    payroll.append("earnings_table", {
                        "salary_type": 20,  # "020" stored as 20 (Int)
                        "description": "Piecework",
                        "from_date": period_from,
                        "to_date": period_to,
                        "number_of_units": 1,
                        "rate_sek": piecework,
                        "total_amount": 1 * piecework,
                    })

                # Piecework Hours Pay (informational; NOT part of gross aggregation)
                if total_hours:
                    payroll.append("earnings_table", {
                        # No salary_type code specified in your sheet for this row
                        "description": "Piecework Hours Pay",
                        "from_date": period_from,
                        "to_date": period_to,
                        "number_of_units": total_hours,
                        "rate_sek": rate_per_hour,
                        "total_amount": total_hours * rate_per_hour,  # equals piecework if rate_per_hour computed as above
                    })

                # 021 Holiday Comp. 13 %
                if holiday_13:
                    payroll.append("earnings_table", {
                        "salary_type": 21,
                        "description": "Holiday Comp. 13 %",
                        "from_date": period_from,
                        "to_date": period_to,
                        "number_of_units": 1,
                        "rate_sek": holiday_13,
                        "total_amount": 1 * holiday_13,
                    })

                # 022 Red. in Working Hours 3,62 %
                if reduction_362:
                    payroll.append("earnings_table", {
                        "salary_type": 22,
                        "description": "Red. in Working Hours 3,62 %",
                        "from_date": period_from,
                        "to_date": period_to,
                        "number_of_units": 1,
                        "rate_sek": reduction_362,
                        "total_amount": 1 * reduction_362,
                    })

                # 301 Daily Allowance
                if attendance_days and daily_allow_rate:
                    payroll.append("earnings_table", {
                        "salary_type": 301,
                        "description": "Daily Allowance",
                        "from_date": period_from,
                        "to_date": period_to,
                        "number_of_units": attendance_days,
                        "rate_sek": daily_allow_rate,
                        "total_amount": attendance_days * daily_allow_rate,
                    })

                # ===== Totals on parent =====
                payroll.gross_salary = gross_salary
                payroll.tax = tax_amount
                payroll.tax_free_compensation = tax_free_comp
                payroll.payment = payment

                # Insert + Submit
                frappe.log_error(f"[{doc.name}] {item.employee}: inserting Payroll Slip", "Payroll Debug")
                payroll.insert(ignore_permissions=True)
                frappe.log_error(f"[{doc.name}] {item.employee}: inserted as {payroll.name}", "Payroll Debug")
                payroll.submit()
                frappe.log_error(f"[{doc.name}] {item.employee}: submitted {payroll.name}", "Payroll Debug")

            except Exception:
                frappe.log_error(
                    f"[{doc.name}] Error while processing employee {getattr(item, 'employee', 'UNKNOWN')}:\n{frappe.get_traceback()}",
                    "Payroll Slip Error"
                )

        frappe.log_error(f"[{doc.name}] Completed generating Payroll Slips", "Payroll Debug")

    except Exception:
        frappe.log_error(f"[{doc.name}] Outer error:\n{frappe.get_traceback()}", "Payroll Slip Error")

