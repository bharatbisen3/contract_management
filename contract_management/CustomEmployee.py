# # # import frappe
# # # from erpnext.setup.doctype.employee.employee import Employee
# # # import json
# # # # from frappe import _, scrub, throw
# # # # from frappe.model.naming import set_name_by_naming_series
# # # # from frappe.permissions import (
# # # #   add_user_permission,
# # # #   get_doc_permissions,
# # # #   has_permission,
# # # #   remove_user_permission,
# # # # )
# # # # from frappe.utils import cstr, getdate, today, validate_email_address
# # # # from frappe.utils.nestedset import NestedSet
 
 
 
# # # # dev-bench/apps/erpnext/erpnext/setup/doctype/employee/employee.py
 
# # # # class CustomEmployee(Employee):
# # # #     # def onload(self):
# # # #     #     # super().onload()
# # # #     #     frappe.msgprint("this is custom app method onload")
# # # #     pass







# # import frappe
# # from erpnext.setup.doctype.employee.employee import Employee
# # import requests
# # import pycountry

# # class CustomEmployee(Employee):
# #     pass

# # @frappe.whitelist()
# # def insert_employee_from_json():
# #     return insert_employee_from_json_direct()

# # def insert_employee_from_json_direct():
# #     token_url = "https://apigateway.blinfo.se/auth/oauth/v2/token"
# #     token_payload = {
# #         "grant_type": "client_credentials",
# #         "client_id": "50d36642-4f84-4340-9e82-48b0fb139e9a",
# #         "client_secret": "edba038c-9824-4131-8d70-55e0416bd5c2"
# #     }
# #     token_headers = {
# #         "Content-Type": "application/x-www-form-urlencoded"
# #     }

# #     token_response = requests.post(token_url, data=token_payload, headers=token_headers)
# #     if token_response.status_code != 200:
# #         frappe.throw("Failed to get access token")

# #     access_token = token_response.json().get("access_token")

# #     api_url = "https://apigateway.blinfo.se/bla-api/v1/sp/employee"
# #     headers = {
# #         "accept": "application/json",
# #         "User-Key": "918afa8a-7a24-4907-8c1d-f3c71352432d",
# #         "Authorization": f"Bearer {access_token}"
# #     }

# #     response = requests.get(api_url, headers=headers)
# #     if response.status_code != 200:
# #         frappe.throw("Failed to fetch employee data")

# #     employees = response.json()

# #     total = len(employees)

# #     for data in employees:
# #         frappe.enqueue(
# #             method=_insert_single_employee,
# #             queue='default',
# #             timeout=300,
# #             is_async=True,
# #             data=data
# #         )

# #     return {
# #         "total_fetched": total,
# #         "already_exist": "Handled in background",
# #         "newly_added": "Handled in background",
# #         "message": "Employee import started in background."
# #     }

# # def _insert_single_employee(data):
# #     def get_country_name(code):
# #         if not code:
# #             return ""
# #         try:
# #             return pycountry.countries.get(alpha_2=code.upper()).name
# #         except:
# #             return code

# #     try:
# #         email = (data.get("email") or "").strip()
# #         full_name = (data.get("name") or "").strip()

# #         if (email and frappe.db.exists("Employee", {"custom_email_address": email})) or \
# #            (not email and frappe.db.exists("Employee", {"employee_name": full_name})):
# #             return  # Already exists

# #         emp = frappe.new_doc("Employee")
# #         name_parts = full_name.split()
# #         first_name = name_parts[0] if len(name_parts) >= 1 else ""
# #         last_name = name_parts[-1] if len(name_parts) >= 2 else ""
# #         middle_name = " ".join(name_parts[1:-1]) if len(name_parts) > 2 else ""

# #         phone = data.get("phones", [])
# #         phone_number = phone[0].get("number") if phone else ""
# #         addr = data.get("address") or {}
# #         adj = data.get("adjustment") or {}

# #         emp.custom_blid = data.get("id") or ""
# #         emp.employee_name = full_name
# #         emp.first_name = first_name
# #         emp.middle_name = middle_name
# #         emp.last_name = last_name
# #         emp.custom_entity_id = data.get("entityId") or ""
# #         emp.status = "Active"
# #         emp.date_of_joining = data.get("employmentStart") or ""
# #         emp.date_of_birth = "2000-01-01"
# #         emp.gender = "Prefer not to say"

# #         emp.custom_email_address = email
# #         emp.custom_your_bank_account_number = data.get("bankAccount", "")
# #         emp.custom_address = addr.get("box", "")
# #         emp.custom_address_2 = addr.get("street", "")
# #         emp.custom_city = addr.get("city", "")
# #         emp.custom_zip__postal_code = addr.get("zip", "")
# #         emp.custom_country = get_country_name(data.get("country"))
# #         emp.custom_citizenship = get_country_name(data.get("citizenshipCountryCode"))
# #         emp.custom_country_of_birth = get_country_name(data.get("birthCountryCode"))
# #         emp.custom_mobile_number = phone_number
# #         emp.custom_bic_code = ""
# #         emp.custom_bank = ""
# #         emp.custom_stateprovince = ""

# #         emp.custom_preferred_name = data.get("sortName") or ""
# #         emp.custom_social_security_number = data.get("socialSecurityNumber") or ""
# #         emp.custom_cost_center = data.get("costCenter") or ""
# #         emp.custom_cost_bearer = data.get("costBearer") or ""
# #         emp.custom_project = data.get("project") or ""
# #         emp.custom_tax_tablebased_taxation = ""
# #         emp.custom_sink_tax = data.get("sink") or ""
# #         emp.custom_asink_tax = data.get("asink") or ""
# #         emp.custom_tax_adjustment__tax_relief = ""
# #         emp.custom_tax_table = data.get("taxationTable") or ""
# #         emp.custom_tax_column = data.get("") or ""
# #         emp.custom_end_date = data.get("employmentEnd") or ""
# #         emp.custom_work_place_id = data.get("workplaceId") or ""
# #         emp.custom_fora_exception = data.get("") or ""
# #         emp.custom_fora_fok = data.get("fokCode") or ""
# #         emp.custom_team_leader = ""
# #         emp.custom_code_of_conduct = ""


# #         emp.insert(ignore_permissions=True)
# #         frappe.db.commit()

# #     except Exception:
# #         frappe.log_error(frappe.get_traceback(), f"Failed to insert employee {data.get('email')}")























# # the above code is used to import employees from BL API




# # Emport employee from grist API



# import frappe
# from erpnext.setup.doctype.employee.employee import Employee
# import pycountry
# import json
# from contract_management.contract_management.api.grist_api import get_employees_from_grist


# class CustomEmployee(Employee):
#     """Extend ERPNext Employee if needed"""
#     pass


# @frappe.whitelist()
# def insert_employee_from_json():
#     """Entry point for Import Employee button"""
#     return insert_employee_from_grist()


# def insert_employee_from_grist():
#     """Fetch employees from Grist API and insert them in bulk"""
#     employees = get_employees_from_grist()  # returns a list now
#     total = len(employees)
#     already_exist, newly_added, errors = 0, 0, []

#     for record in employees:
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
#         except Exception as e:
#             frappe.log_error(frappe.get_traceback(), "Employee Import Error")
#             errors.append(str(e))

#     return {
#         "total_fetched": total,
#         "already_exist": already_exist,
#         "newly_added": newly_added,
#         "errors": errors,
#         "message": "Employee bulk import completed."
#     }


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
#         emp.custom_tax_tablebased_taxation = data.get("Tax_Table_Based_Taxation2") or ""
#         emp.custom_sink_tax = data.get("SINK_Tax2") or data.get("SINK_Tax") or ""
#         emp.custom_asink_tax = data.get("ASINK_Tax") or ""
#         emp.custom_tax_adjustment__tax_relief = data.get("Tax_adjustment_tax_relief") or ""
#         emp.custom_tax_table = data.get("Tax_Table") or ""
#         tax_col = data.get("Tax_Column", "")
#         emp.custom_tax_column = ", ".join(tax_col) if isinstance(tax_col, list) else (tax_col or "")
#         emp.custom_end_date = _convert_unix_to_date(data.get("End_Date"))
#         emp.custom_work_place_id = data.get("Work_Place_ID") or ""
#         emp.custom_fora_exception = data.get("FORA_Exception") or ""
#         emp.custom_fora_fok = data.get("ForaFOK") or ""
#         emp.custom_team_leader = data.get("Team_Leader") or ""
#         emp.custom_code_of_conduct = data.get("Code_of_Conduct") or ""

#         emp.insert(ignore_permissions=True)
#         frappe.db.commit()
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
    # pass

    # """Extend ERPNext Employee if needed"""

    # def validate(self):
    #     # Call original validation first
    #     super().validate()

    #     # Disable ERPNext's requirement for relieving_date
    #     # Even if status = "Left", we ignore that check
    #     # (ERPNext normally enforces this)
    #     if "relieving_date" in self.meta.fields_map:
    #         self.meta.get_field("relieving_date").reqd = 0
    #     return
    
    # pass


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
    """Entry point for Import Employee button"""
    return insert_employee_from_grist()


def insert_employee_from_grist():
    """Fetch employees from Grist API and insert them in bulk"""
    employees = get_employees_from_grist()  # returns a list now
    total = len(employees)
    already_exist, newly_added, errors = 0, 0, []

    for record in employees:
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
        except Exception as e:
            frappe.log_error(frappe.get_traceback(), "Employee Import Error")
            errors.append(str(e))

    return {
        "total_fetched": total,
        "already_exist": already_exist,
        "newly_added": newly_added,
        "errors": errors,
        "message": "Employee bulk import completed."
    }


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
        email = (data.get("Email_Address") or data.get("Email") or "").strip()
        full_name = (data.get("Full_Name") or "").strip()

        # Avoid duplicates
        if (email and frappe.db.exists("Employee", {"custom_email_address": email})) or \
           (not email and full_name and frappe.db.exists("Employee", {"employee_name": full_name})):
            return "exists"

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
        emp.custom_blid = data.get("BL_ID") or ""
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
        emp.custom_tax_adjustment__tax_relief = _boolean_to_string(data.get("Tax_adjustment_tax_relief"))
        emp.custom_team_leader = _boolean_to_string(data.get("Team_Leader"))
        emp.custom_fora_exception = _boolean_to_string(data.get("FORA_Exception"))

        emp.custom_tax_table = data.get("Tax_Table") or ""
        tax_col = data.get("Tax_Column", "")
        emp.custom_tax_column = ", ".join(tax_col) if isinstance(tax_col, list) else (tax_col or "")
        emp.custom_end_date = _convert_unix_to_date(data.get("End_Date"))
        emp.custom_work_place_id = data.get("Work_Place_ID") or ""
        emp.custom_fora_fok = data.get("ForaFOK") or ""
        emp.custom_code_of_conduct = data.get("Code_of_Conduct") or ""

        emp.insert(ignore_permissions=True)
        frappe.db.commit()
        return "created"

    except Exception:
        frappe.log_error(
            frappe.get_traceback(),
            f"Failed to insert employee {data.get('Email_Address') or data.get('Email')}"
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
