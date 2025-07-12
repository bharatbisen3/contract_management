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
# # import json
# # # import json
# # # import frappe
# # import requests
# # import pycountry  # make sure this is installed in your environment
 
 
 
# # class CustomEmployee(Employee):
# #     pass
 
 
# # @frappe.whitelist()
# # def insert_employee_from_json():
# #     # Step 1: Get Access Token
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
# #         frappe.throw(f"Token request failed: {token_response.text}")
 
# #     access_token = token_response.json().get("access_token")
 
# #     # Step 2: Fetch Employee Records
# #     api_url = "https://apigateway.blinfo.se/bla-api/v1/sp/employee"
# #     headers = {
# #         "accept": "application/json",
# #         "User-Key": "918afa8a-7a24-4907-8c1d-f3c71352432d",
# #         "Authorization": f"Bearer {access_token}"
# #     }
 
# #     response = requests.get(api_url, headers=headers)
# #     if response.status_code != 200:
# #         frappe.throw(f"Employee data fetch failed: {response.text}")
 
# #     employees = response.json()  # This is a list of employee dicts
 
# #     # === TEMPORARY CHANGE FOR TESTING: limit to 4 records ===
# #     # employees = employees[:4]
 
# #     for data in employees:
 
# #         email = data.get("email", "").strip()
# #     # --- Check if employee with same email already exists ---
# #         if email:
# #             exists = frappe.db.exists("Employee", {"custom_email_address": email})
# #         if exists:
# #             frappe.logger().info(f"Skipping existing employee with email: {email}")
# #             # frappe.msgprint(f"Skipping existing employee: {email}")
 
# #             continue
 
# #         emp = frappe.new_doc("Employee")
 
# #         # --- Name Splitting ---
# #         full_name = (data.get("name") or "").strip()
# #         name_parts = full_name.split()
# #         first_name = name_parts[0] if len(name_parts) >= 1 else ""
# #         last_name = name_parts[-1] if len(name_parts) >= 2 else ""
# #         middle_name = " ".join(name_parts[1:-1]) if len(name_parts) > 2 else ""
 
# #         # --- Country Code to Full Country ---
# #         def get_country_name(code):
# #             if not code:
# #                 return ""
# #             try:
# #                 return pycountry.countries.get(alpha_2=code.upper()).name
# #             except:
# #                 return code  # fallback if invalid
 
# #         # --- Phone Parsing ---
# #         phone = data.get("phones", [])
# #         phone_number = phone[0].get("number") if phone else ""
 
# #         # --- Address ---
# #         addr = data.get("address") or {}
 
# #         # Assign fields
# #         emp.employee_name = full_name
# #         emp.first_name = first_name
# #         emp.middle_name = middle_name
# #         emp.last_name = last_name
# #         emp.status = "Active"
# #         emp.date_of_joining = data.get("employmentStart") or ""
# #         emp.date_of_birth = "2000-01-01"  # Not provided in API
# #         emp.gender = "Prefer not to say"
 
# #         # Custom Fields
# #         emp.custom_email_address = data.get("email", "")
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
 
# #         emp.insert(ignore_permissions=True)
 
# #     frappe.db.commit()
# #     frappe.msgprint("All employee records inserted successfully from API.")
 
 
 
 
 
 
 
 
 
 
 
# using frappe enqueue
 
 
 
 
 
# import frappe
# from erpnext.setup.doctype.employee.employee import Employee
# import requests
# import pycountry
 
 
# class CustomEmployee(Employee):
#     pass
 
 
# @frappe.whitelist()
# def insert_employee_from_json():
#     # frappe.enqueue("contract_management.contract_management.doctype.employee.employee.insert_employee_from_json_background",
#     frappe.enqueue("contract_management.CustomEmployee.insert_employee_from_json_background",
#                    queue='long', timeout=1800, now=False)
#     return "Employee sync job enqueued successfully."
 
 
# def insert_employee_from_json_background():
#     token_url = "https://apigateway.blinfo.se/auth/oauth/v2/token"
#     token_payload = {
#         "grant_type": "client_credentials",
#         "client_id": "50d36642-4f84-4340-9e82-48b0fb139e9a",
#         "client_secret": "edba038c-9824-4131-8d70-55e0416bd5c2"
#     }
#     token_headers = {
#         "Content-Type": "application/x-www-form-urlencoded"
#     }
 
#     token_response = requests.post(token_url, data=token_payload, headers=token_headers)
#     if token_response.status_code != 200:
#         frappe.log_error(token_response.text, "Token request failed")
#         return
 
#     access_token = token_response.json().get("access_token")
 
#     api_url = "https://apigateway.blinfo.se/bla-api/v1/sp/employee"
#     headers = {
#         "accept": "application/json",
#         "User-Key": "918afa8a-7a24-4907-8c1d-f3c71352432d",
#         "Authorization": f"Bearer {access_token}"
#     }
 
#     response = requests.get(api_url, headers=headers)
#     if response.status_code != 200:
#         frappe.log_error(response.text, "Employee fetch failed")
#         return
 
#     employees = response.json()
 
#     for data in employees:
#         try:
#             email = data.get("email", "").strip()
#             if email:
#                 exists = frappe.db.exists("Employee", {"custom_email_address": email})
#                 if exists:
#                     frappe.logger().info(f"Skipping existing employee with email: {email}")
#                     continue
 
#             emp = frappe.new_doc("Employee")
#             full_name = (data.get("name") or "").strip()
#             name_parts = full_name.split()
#             first_name = name_parts[0] if len(name_parts) >= 1 else ""
#             last_name = name_parts[-1] if len(name_parts) >= 2 else ""
#             middle_name = " ".join(name_parts[1:-1]) if len(name_parts) > 2 else ""
 
#             def get_country_name(code):
#                 if not code:
#                     return ""
#                 try:
#                     return pycountry.countries.get(alpha_2=code.upper()).name
#                 except:
#                     return code
 
#             phone = data.get("phones", [])
#             phone_number = phone[0].get("number") if phone else ""
#             addr = data.get("address") or {}
 
#             emp.employee_name = full_name
#             emp.first_name = first_name
#             emp.middle_name = middle_name
#             emp.last_name = last_name
#             emp.status = "Active"
#             emp.date_of_joining = data.get("employmentStart") or ""
#             emp.date_of_birth = "2000-01-01"
#             emp.gender = "Prefer not to say"
 
#             emp.custom_email_address = email
#             emp.custom_your_bank_account_number = data.get("bankAccount", "")
#             emp.custom_address = addr.get("box", "")
#             emp.custom_address_2 = addr.get("street", "")
#             emp.custom_city = addr.get("city", "")
#             emp.custom_zip__postal_code = addr.get("zip", "")
#             emp.custom_country = get_country_name(data.get("country"))
#             emp.custom_citizenship = get_country_name(data.get("citizenshipCountryCode"))
#             emp.custom_country_of_birth = get_country_name(data.get("birthCountryCode"))
#             emp.custom_mobile_number = phone_number
#             emp.custom_bic_code = ""
#             emp.custom_bank = ""
#             emp.custom_stateprovince = ""
 
#             emp.insert(ignore_permissions=True)
#             frappe.db.commit()
#         except Exception as e:
#             frappe.log_error(frappe.get_traceback(), f"Failed to insert employee {email}")
 
#     frappe.logger().info("Background employee import finished.")
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
import frappe
from erpnext.setup.doctype.employee.employee import Employee
import requests
import pycountry
 
 
class CustomEmployee(Employee):
    pass
 
@frappe.whitelist()
def insert_employee_from_json():
    return insert_employee_from_json_direct()
 
 
def insert_employee_from_json_direct():
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
        frappe.throw("Failed to get access token")
 
    access_token = token_response.json().get("access_token")
 
    api_url = "https://apigateway.blinfo.se/bla-api/v1/sp/employee"
    headers = {
        "accept": "application/json",
        "User-Key": "918afa8a-7a24-4907-8c1d-f3c71352432d",
        "Authorization": f"Bearer {access_token}"
    }
 
    response = requests.get(api_url, headers=headers)
    if response.status_code != 200:
        frappe.throw("Failed to fetch employee data")
 
    employees = response.json()
 
    total = len(employees)
    existing = 0
    inserted = 0
 
    def get_country_name(code):
        if not code:
            return ""
        try:
            return pycountry.countries.get(alpha_2=code.upper()).name
        except:
            return code
 
    # employees = employees[:4]
 
 
    for data in employees:
 
        try:
            # email = data.get("email", "").strip()
            # if email and frappe.db.exists("Employee", {"custom_email_address": email}):
            #     existing += 1
            #     continue
 
            
            email = (data.get("email") or "").strip()
            full_name = (data.get("name") or "").strip()
 
            # If email is present, check uniqueness by email
            # If email is blank, check uniqueness by name
            if (email and frappe.db.exists("Employee", {"custom_email_address": email})) or \
               (not email and frappe.db.exists("Employee", {"employee_name": full_name})):
                existing += 1
                continue
 
 
            emp = frappe.new_doc("Employee")
            full_name = (data.get("name") or "").strip()
            name_parts = full_name.split()
            first_name = name_parts[0] if len(name_parts) >= 1 else ""
            last_name = name_parts[-1] if len(name_parts) >= 2 else ""
            middle_name = " ".join(name_parts[1:-1]) if len(name_parts) > 2 else ""
 
            phone = data.get("phones", [])
            phone_number = phone[0].get("number") if phone else ""
            addr = data.get("address") or {}
 
            emp.custom_blid = data.get("id") or ""
            emp.employee_name = full_name
            emp.first_name = first_name
            emp.middle_name = middle_name
            emp.last_name = last_name
            emp.custom_entity_id = data.get("entityId") or ""
            emp.status = "Active"
            emp.date_of_joining = data.get("employmentStart") or ""
            emp.date_of_birth = "2000-01-01"
            emp.gender = "Prefer not to say"
 
            emp.custom_email_address = email
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
            inserted += 1
 
        except Exception as e:
            frappe.log_error(frappe.get_traceback(), f"Failed to insert employee {email}")
 
    return {
        "total_fetched": total,
        "already_exist": existing,
        "newly_added": inserted,
        "message": "Employee import completed successfully."
    }