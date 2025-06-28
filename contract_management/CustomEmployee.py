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
# import json

# class CustomEmployee(Employee):
#     pass

# @frappe.whitelist()
# def insert_employee_from_json():    
#     frappe.msgprint("this is custom app method onload")

#     # List of employee records from Excel (both rows)
#     employees = [
#         {
#             "ID": "HR-EMP-00001",
#             "First Name": "Bharat",
#             "Last Name": "Bisen",
#             "Series": "HR-EMP-",
#             "Gender": "Male",
#             "Date of Birth": "2001-05-11",
#             "Date of Joining": "2025-06-01",
#             "Status": "Active",
#             "Company": "Ljunganforestry (Demo)",
#             "Middle Name": "kdj",
#             "Full Name": "Bharat kdj Bisen",
#             "Country of Birth": "India",
#             "Citizenship": "India",
#             "Contact Number": "+91-7030958443",
#             "Email Address": "bharat@algoware.in",
#             "Address 1": "lkj",
#             "Address 2": "lkj",
#             "Zip / Postal code": "78",
#             "City": "Gondia",
#             "State / Province": "MH",
#             "Country": "India",
#             "Bank": "BRD - Groupe Societe Generale S.A.",
#             "BIC Code": "7689",
#             "Your bank account number": "6578",
#             "User ID": "bharat@algoware.in",
#             "Mobile": "2061-05-11"
#         },
#         {
#             "ID": "HR-EMP-00002",
#             "First Name": "kldj",
#             "Last Name": "lkj",
#             "Series": "HR-EMP-",
#             "Gender": "Male",
#             "Date of Birth": "2025-03-05",
#             "Date of Joining": "2025-06-01",
#             "Status": "Active",
#             "Company": "Ljunganforestry (Demo)",
#             "Middle Name": "lkj",
#             "Full Name": "kldj lkj lkj",
#             "Country of Birth": "India",
#             "Citizenship": "India",
#             "Contact Number": "+91-9874102563",
#             "Email Address": "tla@algoware.in",
#             "Address 1": "lkj",
#             "Address 2": "hik",
#             "Zip / Postal code": "789",
#             "City": "gondia",
#             "State / Province": "MH",
#             "Country": "India",
#             "Bank": "BANCA TRANSILVANIA S.A.",
#             "BIC Code": "56789",
#             "Your bank account number": "0",
#             "User ID": "",
#             "Mobile": ""
#         }
#     ]

#     for data in employees:
#         emp = frappe.new_doc("Employee")

#         # Core Fields
#         emp.employee_name = data["Full Name"].strip()
#         emp.first_name = data["First Name"]
#         emp.middle_name = data.get("Middle Name", "")
#         emp.last_name = data.get("Last Name", "")
#         emp.date_of_joining = data["Date of Joining"]
#         emp.status = data["Status"]

#         # Custom Fields
#         emp.custom_your_bank_account_number = data.get("Your bank account number", "")
#         emp.custom_address = data.get("Address 1", "")
#         emp.custom_address_2 = data.get("Address 2", "")
#         emp.custom_city = data.get("City", "")
#         emp.custom_zip__postal_code = data.get("Zip / Postal code", "")
#         emp.custom_country = data.get("Country", "")
#         emp.custom_email_address = data.get("Email Address", "")
#         emp.custom_citizenship = data.get("Citizenship", "")
#         emp.custom_country_of_birth = data.get("Country of Birth", "")

#         # Optional Fields
#         emp.gender = data.get("Gender", "Male")
#         emp.date_of_birth = data.get("Date of Birth", "")
#         emp.custom_please_attach_your_valid_id_or_passport = ""
#         emp.custom_your_bank_account_number_a = data.get("Your bank account number", "")
#         emp.custom_name_the_other_bank = ""
#         emp.custom_bic_code = data.get("BIC Code", "")
#         emp.custom_bank = data.get("Bank", "")
#         emp.custom_stateprovince = data.get("State / Province", "")

#         # Insert the document
#         emp.insert(ignore_permissions=True)

#     frappe.db.commit()
#     frappe.msgprint("All employee records inserted successfully.")














import frappe
from erpnext.setup.doctype.employee.employee import Employee
import json
# import json
# import frappe
import requests
import pycountry  # make sure this is installed in your environment



class CustomEmployee(Employee):
    pass


@frappe.whitelist()
def insert_employee_from_json():
    # Step 1: Get Access Token
    token_url = "https://apigateway.blinfo.se/auth/oauth/v2/token"
    token_payload = {
        "grant_type": "client_credentials",
        "client_id": "50d36642-4f84-4340-9e82-48b0fb139e9a",
        "client_secret": "edba038c-9824-4131-8d70-55e0416bd5c2"
    }
    token_headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    token_response = requests.post(token_url, data=token_payload, headers=token_headers)
    if token_response.status_code != 200:
        frappe.throw(f"Token request failed: {token_response.text}")

    access_token = token_response.json().get("access_token")

    # Step 2: Fetch Employee Records
    api_url = "https://apigateway.blinfo.se/bla-api/v1/sp/employee"
    headers = {
        "accept": "application/json",
        "User-Key": "918afa8a-7a24-4907-8c1d-f3c71352432d",
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(api_url, headers=headers)
    if response.status_code != 200:
        frappe.throw(f"Employee data fetch failed: {response.text}")

    employees = response.json()  # This is a list of employee dicts

    # === TEMPORARY CHANGE FOR TESTING: limit to 4 records ===
    employees = employees[:4]

    for data in employees:
        emp = frappe.new_doc("Employee")

        # --- Name Splitting ---
        full_name = (data.get("name") or "").strip()
        name_parts = full_name.split()
        first_name = name_parts[0] if len(name_parts) >= 1 else ""
        last_name = name_parts[-1] if len(name_parts) >= 2 else ""
        middle_name = " ".join(name_parts[1:-1]) if len(name_parts) > 2 else ""

        # --- Country Code to Full Country ---
        def get_country_name(code):
            if not code:
                return ""
            try:
                return pycountry.countries.get(alpha_2=code.upper()).name
            except:
                return code  # fallback if invalid

        # --- Phone Parsing ---
        phone = data.get("phones", [])
        phone_number = phone[0].get("number") if phone else ""

        # --- Address ---
        addr = data.get("address") or {}

        # Assign fields
        emp.employee_name = full_name
        emp.first_name = first_name
        emp.middle_name = middle_name
        emp.last_name = last_name
        emp.status = "Active"
        emp.date_of_joining = data.get("employmentStart") or ""
        emp.date_of_birth = "2000-01-01"  # Not provided in API
        emp.gender = "Prefer not to say"

        # Custom Fields
        emp.custom_email_address = data.get("email", "")
        emp.custom_your_bank_account_number = data.get("bankAccount", "")
        emp.custom_address = addr.get("box", "")
        emp.custom_address_2 = addr.get("street", "")
        emp.custom_city = addr.get("city", "")
        emp.custom_zip__postal_code = addr.get("zip", "")
        emp.custom_country = get_country_name(data.get("country"))
        emp.custom_citizenship = get_country_name(data.get("citizenshipCountryCode"))
        emp.custom_country_of_birth = get_country_name(data.get("birthCountryCode"))
        emp.custom_mobile_number = phone_number
        emp.custom_bic_code = ""
        emp.custom_bank = ""
        emp.custom_stateprovince = ""

        emp.insert(ignore_permissions=True)

    frappe.db.commit()
    frappe.msgprint("All employee records inserted successfully from API.")
