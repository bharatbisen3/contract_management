# # import frappe
# # from erpnext.setup.doctype.employee.employee import Employee
# # import json
# # # from frappe import _, scrub, throw
# # # from frappe.model.naming import set_name_by_naming_series
# # # from frappe.permissions import (
# # #   add_user_permission,
# # #   get_doc_permissions,
# # #   has_permission,
# # #   remove_user_permission,
# # # )
# # # from frappe.utils import cstr, getdate, today, validate_email_address
# # # from frappe.utils.nestedset import NestedSet
 
 
 
# # # dev-bench/apps/erpnext/erpnext/setup/doctype/employee/employee.py
 
# # # class CustomEmployee(Employee):
# # #     # def onload(self):
# # #     #     # super().onload()
# # #     #     frappe.msgprint("this is custom app method onload")
# # #     pass

















# import frappe
# from erpnext.setup.doctype.employee.employee import Employee
# import pycountry
# import json
# from contract_management.contract_management.api.grist_api import get_employees_from_grist


# class CustomEmployee(Employee):
#     def validate(self):
#         """
#         Custom Employee validate without enforcing relieving_date.
#         """
#         from erpnext.controllers.status_updater import validate_status

#         # keep ERPNext allowed statuses
#         validate_status(self.status, ["Active", "Inactive", "Suspended", "Left"])

#         self.employee = self.name
#         self.set_employee_name()
#         self.validate_date()
#         self.validate_email()

#         # 🚫 we skip the original validate_status() that enforces relieving_date
#         self.custom_validate_status()

#         self.validate_reports_to()
#         self.set_preferred_email()
#         self.validate_preferred_email()

#         if self.user_id:
#             self.validate_user_details()
#         else:
#             existing_user_id = frappe.db.get_value("Employee", self.name, "user_id")
#             if existing_user_id:
#                 user = frappe.get_doc("User", existing_user_id)
#                 from erpnext.setup.doctype.employee.employee import validate_employee_role
#                 validate_employee_role(user, ignore_emp_check=True)
#                 user.save(ignore_permissions=True)
#                 from frappe.utils.user import remove_user_permission
#                 remove_user_permission("Employee", self.name, existing_user_id)

#     def custom_validate_status(self):
#         """
#         Replace ERPNext's validate_status that enforces relieving_date.
#         Do nothing here to bypass the check.
#         """
#         return


# @frappe.whitelist()
# def insert_employee_from_json():
#     """Entry point for Import Employee button - queues background job"""
    
#     # Enqueue the actual import as a background job
#     frappe.enqueue(
#         method='contract_management.CustomEmployee.insert_employee_from_grist',
#         queue='long',  # Use 'long' queue for time-consuming tasks
#         timeout=3600,  # 1 hour timeout
#         is_async=True,
#         job_name='employee_import',
#         now=False
#     )
    
#     return {
#         "status": "queued",
#         "message": "Employee import has been queued. You will receive a notification when it completes."
#     }


# def insert_employee_from_grist():
#     """Fetch employees from Grist API and insert them in bulk (runs in background)"""
#     employees = get_employees_from_grist()  # returns a list now
#     total = len(employees)
#     already_exist, newly_added, errors = 0, 0, []

#     for idx, record in enumerate(employees, 1):
#         if not isinstance(record, dict):
#             continue

#         # Grist returns {"id": ..., "fields": {...}}
#         data = record.get("fields", {})
#         if not data:
#             continue

#         try:
#             result = _insert_single_employee(data)
#             if result == "exists":
#                 already_exist += 1
#             elif result == "created":
#                 newly_added += 1
                
#             # Commit every 10 records to avoid long transactions
#             if idx % 10 == 0:
#                 frappe.db.commit()
                
#         except Exception as e:
#             frappe.log_error(frappe.get_traceback(), "Employee Import Error")
#             errors.append(str(e))

#     # Final commit
#     frappe.db.commit()
    
#     # Send notification to user
#     _send_completion_notification(total, already_exist, newly_added, errors)
    
#     return {
#         "total_fetched": total,
#         "already_exist": already_exist,
#         "newly_added": newly_added,
#         "errors": errors,
#         "message": "Employee bulk import completed."
#     }


# def _send_completion_notification(total, already_exist, newly_added, errors):
#     """Send notification to user when import completes"""
#     try:
#         message = f"""
#         <h4>Employee Import Completed</h4>
#         <ul>
#             <li><b>Total Fetched:</b> {total}</li>
#             <li><b>Already Exist:</b> {already_exist}</li>
#             <li><b>Newly Added:</b> {newly_added}</li>
#             <li><b>Errors:</b> {len(errors)}</li>
#         </ul>
#         """
        
#         if errors:
#             message += f"<p><b>Error Details:</b><br>{'<br>'.join(errors[:5])}</p>"
#             if len(errors) > 5:
#                 message += f"<p>...and {len(errors) - 5} more errors</p>"
        
#         frappe.publish_realtime(
#             event='msgprint',
#             message=message,
#             user=frappe.session.user
#         )
        
#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), "Notification Error")


# def _boolean_to_string(value):
#     """Convert bool/str/int to ERPNext-compatible Select values"""
#     if isinstance(value, bool):
#         return "TRUE" if value else "FALSE"
#     if isinstance(value, (int, float)):
#         return "TRUE" if int(value) != 0 else "FALSE"
#     if isinstance(value, str):
#         v = value.strip().lower()
#         if v in ["true", "1", "yes", "y"]:
#             return "TRUE"
#         elif v in ["false", "0", "no", "n"]:
#             return "FALSE"
#     return ""


# def _insert_single_employee(data):
#     """Insert a single employee record from Grist into ERPNext"""

#     def get_country_name(code):
#         if not code:
#             return ""
#         try:
#             return pycountry.countries.get(alpha_2=code.upper()).name
#         except Exception:
#             return code

#     try:
#         email = (data.get("Email_Address") or data.get("Email") or "").strip()
#         full_name = (data.get("Full_Name") or "").strip()

#         # Avoid duplicates
#         if (email and frappe.db.exists("Employee", {"custom_email_address": email})) or \
#            (not email and full_name and frappe.db.exists("Employee", {"employee_name": full_name})):
#             return "exists"

#         emp = frappe.new_doc("Employee")

#         # Name handling
#         first_name = data.get("First_Name2") or (full_name.split(" ")[0] if full_name else "")
#         last_name = data.get("Last_Name") or (full_name.split(" ")[-1] if full_name else "")
#         middle_name = data.get("Middle_Name") or " ".join(full_name.split(" ")[1:-1])

#         # Phone number
#         phone_number = data.get("Contact_Number") or data.get("Tel") or ""

#         # Core fields
#         emp.employee_name = full_name or f"{first_name} {last_name}".strip()
#         emp.first_name = first_name
#         emp.middle_name = middle_name
#         emp.last_name = last_name
#         emp.status = "Active" if data.get("Active2") else "Inactive"
#         emp.custom_email_address = email

#         # Optional custom fields
#         emp.custom_blid = data.get("BL_ID") or ""
#         emp.custom_employeeid = "EMP - " + data.get("BL_ID") or ""      #this is added by concating bl_id
#         emp.custom_entity_id = data.get("ERPNext_ID") or ""
#         emp.date_of_joining = _convert_unix_to_date(data.get("Date_of_Joining"))
#         emp.date_of_birth = _convert_unix_to_date(data.get("Date_of_Birth")) or "2000-01-01"
#         emp.gender = data.get("Gender") or "Prefer not to say"

#         emp.custom_your_bank_account_number = data.get("Bank_Account_Number", "")
#         emp.custom_address = data.get("Box", "")
#         emp.custom_address_2 = data.get("Address_1", "")
#         emp.custom_city = data.get("City") or data.get("City2", "")
#         emp.custom_zip__postal_code = data.get("Zip") or data.get("Zip_Postal_code", "")
#         emp.custom_country = get_country_name(data.get("Country"))
#         emp.custom_citizenship = get_country_name(data.get("citizenshipCountryCode"))
#         emp.custom_country_of_birth = get_country_name(data.get("Country_of_Birth"))
#         emp.custom_mobile_number = phone_number
#         emp.custom_bic_code = data.get("BIC_Code", "")
#         emp.custom_bank = data.get("Bank", "")
#         emp.custom_stateprovince = data.get("State_Province") or ""

#         emp.custom_preferred_name = data.get("Preferred_Name") or ""
#         emp.custom_social_security_number = (
#             data.get("Social_Security_Number")
#             or data.get("Social_Security_Number_2")
#             or ""
#         )
#         emp.custom_cost_center = data.get("Cost_Center") or ""
#         emp.custom_cost_bearer = data.get("Cost_Bearer") or ""
#         emp.custom_project = data.get("Project") or ""

#         # ✅ Boolean / Select fields converted
#         emp.custom_tax_tablebased_taxation = _boolean_to_string(data.get("Tax_Table_Based_Taxation2"))
#         emp.custom_sink_tax = _boolean_to_string(data.get("SINK_Tax2") or data.get("SINK_Tax"))
#         emp.custom_asink_tax = _boolean_to_string(data.get("ASINK_Tax"))
#         emp.custom_team_leader = _boolean_to_string(data.get("Team_Leader"))
#         emp.custom_fora_exception = _boolean_to_string(data.get("FORA_Exception"))

#         emp.custom_tax_table = data.get("Tax_Table") or ""
#         tax_col = data.get("Tax_Column", [])
#         emp.custom_tax_column = tax_col[1] if isinstance(tax_col, list) and len(tax_col) > 1 else ""

#         emp.custom_end_date = _convert_unix_to_date(data.get("End_Date"))
#         emp.custom_work_place_id = data.get("Work_Place_ID") or ""
#         emp.custom_fora_fok = data.get("ForaFOK") or ""
#         emp.custom_code_of_conduct = data.get("Code_of_Conduct") or ""

#         emp.insert(ignore_permissions=True)
#         return "created"

#     except Exception:
#         frappe.log_error(
#             frappe.get_traceback(),
#             f"Failed to insert employee {data.get('Email_Address') or data.get('Email')}"
#         )
#         return "error"


# def _convert_unix_to_date(value):
#     """Convert unix timestamp or string date into YYYY-MM-DD"""
#     import datetime
#     if not value:
#         return ""
#     if isinstance(value, (int, float)) or (isinstance(value, str) and value.isdigit()):
#         try:
#             return datetime.datetime.utcfromtimestamp(int(value)).strftime("%Y-%m-%d")
#         except Exception:
#             return ""
#     s = str(value)
#     try:
#         if "T" in s:
#             return s.split("T")[0]
#         for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y"):
#             try:
#                 return datetime.datetime.strptime(s, fmt).strftime("%Y-%m-%d")
#             except Exception:
#                 pass
#     except Exception:
#         pass
#     return ""















import frappe
from erpnext.setup.doctype.employee.employee import Employee
import pycountry
import json
from contract_management.contract_management.api.grist_api import get_employees_from_grist


class CustomEmployee(Employee):
    def validate(self):
        """
        Custom Employee validate without enforcing relieving_date.
        """
        from erpnext.controllers.status_updater import validate_status

        # keep ERPNext allowed statuses
        validate_status(self.status, ["Active", "Inactive", "Suspended", "Left"])

        self.employee = self.name
        self.set_employee_name()
        self.validate_date()
        self.validate_email()

        # 🚫 we skip the original validate_status() that enforces relieving_date
        self.custom_validate_status()

        self.validate_reports_to()
        self.set_preferred_email()
        self.validate_preferred_email()

        if self.user_id:
            self.validate_user_details()
        else:
            existing_user_id = frappe.db.get_value("Employee", self.name, "user_id")
            if existing_user_id:
                user = frappe.get_doc("User", existing_user_id)
                from erpnext.setup.doctype.employee.employee import validate_employee_role
                validate_employee_role(user, ignore_emp_check=True)
                user.save(ignore_permissions=True)
                from frappe.utils.user import remove_user_permission
                remove_user_permission("Employee", self.name, existing_user_id)

    def custom_validate_status(self):
        """
        Replace ERPNext's validate_status that enforces relieving_date.
        Do nothing here to bypass the check.
        """
        return


@frappe.whitelist()
def insert_employee_from_json():
    """Entry point for Import Employee button - queues background job"""
    
    # Enqueue the actual import as a background job
    frappe.enqueue(
        method='contract_management.CustomEmployee.insert_employee_from_grist',
        queue='long',  # Use 'long' queue for time-consuming tasks
        timeout=3600,  # 1 hour timeout
        is_async=True,
        job_name='employee_import',
        now=False
    )
    
    return {
        "status": "queued",
        "message": "Employee import has been queued. You will receive a notification when it completes."
    }


def insert_employee_from_grist():
    """Fetch employees from Grist API and insert them in bulk (runs in background)"""
    employees = get_employees_from_grist()  # returns a list now
    total = len(employees)
    already_exist, newly_added, errors = 0, 0, []

    for idx, record in enumerate(employees, 1):
        if not isinstance(record, dict):
            continue

        # Grist returns {"id": ..., "fields": {...}}
        data = record.get("fields", {})
        if not data:
            continue

        try:
            result = _insert_single_employee(data)
            if result == "exists":
                already_exist += 1
            elif result == "created":
                newly_added += 1
                
            # Commit every 10 records to avoid long transactions
            if idx % 10 == 0:
                frappe.db.commit()
                
        except Exception as e:
            frappe.log_error(frappe.get_traceback(), "Employee Import Error")
            errors.append(str(e))

    # Final commit
    frappe.db.commit()
    
    # Send notification to user
    _send_completion_notification(total, already_exist, newly_added, errors)
    
    return {
        "total_fetched": total,
        "already_exist": already_exist,
        "newly_added": newly_added,
        "errors": errors,
        "message": "Employee bulk import completed."
    }


def _send_completion_notification(total, already_exist, newly_added, errors):
    """Send notification to user when import completes"""
    try:
        message = f"""
        <h4>Employee Import Completed</h4>
        <ul>
            <li><b>Total Fetched:</b> {total}</li>
            <li><b>Already Exist:</b> {already_exist}</li>
            <li><b>Newly Added:</b> {newly_added}</li>
            <li><b>Errors:</b> {len(errors)}</li>
        </ul>
        """
        
        if errors:
            message += f"<p><b>Error Details:</b><br>{'<br>'.join(errors[:5])}</p>"
            if len(errors) > 5:
                message += f"<p>...and {len(errors) - 5} more errors</p>"
        
        frappe.publish_realtime(
            event='msgprint',
            message=message,
            user=frappe.session.user
        )
        
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Notification Error")


def _boolean_to_string(value):
    """Convert bool/str/int to ERPNext-compatible Select values"""
    if isinstance(value, bool):
        return "TRUE" if value else "FALSE"
    if isinstance(value, (int, float)):
        return "TRUE" if int(value) != 0 else "FALSE"
    if isinstance(value, str):
        v = value.strip().lower()
        if v in ["true", "1", "yes", "y"]:
            return "TRUE"
        elif v in ["false", "0", "no", "n"]:
            return "FALSE"
    return ""


def _insert_single_employee(data):
    """Insert a single employee record from Grist into ERPNext"""

    def get_country_name(code):
        if not code:
            return ""
        try:
            return pycountry.countries.get(alpha_2=code.upper()).name
        except Exception:
            return code

    try:
        # ✅ CHECK UNIQUENESS BY BL_ID ONLY
        bl_id = (data.get("BL_ID") or "").strip()
        
        # Skip if no BL_ID provided
        if not bl_id:
            frappe.log_error(
                f"Skipping employee - No BL_ID provided: {data.get('Full_Name') or data.get('Email_Address')}",
                "Employee Import - Missing BL_ID"
            )
            return "exists"
        
        # Check if employee with this BL_ID already exists
        if frappe.db.exists("Employee", {"custom_blid": bl_id}):
            return "exists"

        email = (data.get("Email_Address") or data.get("Email") or "").strip()
        full_name = (data.get("Full_Name") or "").strip()

        emp = frappe.new_doc("Employee")

        # Name handling
        first_name = data.get("First_Name2") or (full_name.split(" ")[0] if full_name else "")
        last_name = data.get("Last_Name") or (full_name.split(" ")[-1] if full_name else "")
        middle_name = data.get("Middle_Name") or " ".join(full_name.split(" ")[1:-1])

        # Phone number
        phone_number = data.get("Contact_Number") or data.get("Tel") or ""

        # Core fields
        emp.employee_name = full_name or f"{first_name} {last_name}".strip()
        emp.first_name = first_name
        emp.middle_name = middle_name
        emp.last_name = last_name
        emp.status = "Active" if data.get("Active2") else "Inactive"
        emp.custom_email_address = email

        # Optional custom fields
        emp.custom_blid = bl_id
        emp.custom_employeeid = "EMP - " + bl_id      #this is added by concating bl_id
        emp.custom_entity_id = data.get("ERPNext_ID") or ""
        emp.date_of_joining = _convert_unix_to_date(data.get("Date_of_Joining"))
        emp.date_of_birth = _convert_unix_to_date(data.get("Date_of_Birth")) or "2000-01-01"
        emp.gender = data.get("Gender") or "Prefer not to say"

        emp.custom_your_bank_account_number = data.get("Bank_Account_Number", "")
        emp.custom_address = data.get("Box", "")
        emp.custom_address_2 = data.get("Address_1", "")
        emp.custom_city = data.get("City") or data.get("City2", "")
        emp.custom_zip__postal_code = data.get("Zip") or data.get("Zip_Postal_code", "")
        emp.custom_country = get_country_name(data.get("Country"))
        emp.custom_citizenship = get_country_name(data.get("citizenshipCountryCode"))
        emp.custom_country_of_birth = get_country_name(data.get("Country_of_Birth"))
        emp.custom_mobile_number = phone_number
        emp.custom_bic_code = data.get("BIC_Code", "")
        emp.custom_bank = data.get("Bank", "")
        emp.custom_stateprovince = data.get("State_Province") or ""

        emp.custom_preferred_name = data.get("Preferred_Name") or ""
        emp.custom_social_security_number = (
            data.get("Social_Security_Number")
            or data.get("Social_Security_Number_2")
            or ""
        )
        emp.custom_cost_center = data.get("Cost_Center") or ""
        emp.custom_cost_bearer = data.get("Cost_Bearer") or ""
        emp.custom_project = data.get("Project") or ""

        # ✅ Boolean / Select fields converted
        emp.custom_tax_tablebased_taxation = _boolean_to_string(data.get("Tax_Table_Based_Taxation2"))
        emp.custom_sink_tax = _boolean_to_string(data.get("SINK_Tax2") or data.get("SINK_Tax"))
        emp.custom_asink_tax = _boolean_to_string(data.get("ASINK_Tax"))
        emp.custom_team_leader = _boolean_to_string(data.get("Team_Leader"))
        emp.custom_fora_exception = _boolean_to_string(data.get("FORA_Exception"))

        emp.custom_tax_table = data.get("Tax_Table") or ""
        tax_col = data.get("Tax_Column", [])
        emp.custom_tax_column = tax_col[1] if isinstance(tax_col, list) and len(tax_col) > 1 else ""

        emp.custom_end_date = _convert_unix_to_date(data.get("End_Date"))
        emp.custom_work_place_id = data.get("Work_Place_ID") or ""
        emp.custom_fora_fok = data.get("ForaFOK") or ""
        emp.custom_code_of_conduct = data.get("Code_of_Conduct") or ""

        emp.insert(ignore_permissions=True)
        return "created"

    except Exception:
        frappe.log_error(
            frappe.get_traceback(),
            f"Failed to insert employee {data.get('BL_ID')} - {data.get('Email_Address') or data.get('Email')}"
        )
        return "error"


def _convert_unix_to_date(value):
    """Convert unix timestamp or string date into YYYY-MM-DD"""
    import datetime
    if not value:
        return ""
    if isinstance(value, (int, float)) or (isinstance(value, str) and value.isdigit()):
        try:
            return datetime.datetime.utcfromtimestamp(int(value)).strftime("%Y-%m-%d")
        except Exception:
            return ""
    s = str(value)
    try:
        if "T" in s:
            return s.split("T")[0]
        for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y"):
            try:
                return datetime.datetime.strptime(s, fmt).strftime("%Y-%m-%d")
            except Exception:
                pass
    except Exception:
        pass
    return ""