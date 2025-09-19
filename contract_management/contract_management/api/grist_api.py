import frappe
import requests

GRIST_API_URL = "https://ljungan.getgrist.com/api/docs/bdCYnioEbuyGM6jMavS1Kf/tables/EMPLOYEE/records"
GRIST_TOKEN = "b83d20f59034284de9f2aec8b73f84d84193fc03"   # 🔒 Keep secret, do not expose in JS

@frappe.whitelist()
def get_employees_from_grist():
    """Fetch employee records from external Grist API"""
    headers = {
        "Authorization": f"Bearer {GRIST_TOKEN}",
        "Content-Type": "application/json"
    }
    try:
        res = requests.get(GRIST_API_URL, headers=headers)
        res.raise_for_status()
        data = res.json()
        return data.get("records", [])
    except requests.exceptions.RequestException as e:
        frappe.log_error(f"Grist API Error: {e}", "get_employees_from_grist")
        return []









# import frappe
# import requests

# GRIST_API_URL = "https://ljungan.getgrist.com/api/docs/bdCYnioEbuyGM6jMavS1Kf/tables/EMPLOYEE/records"
# GRIST_TOKEN = "b83d20f59034284de9f2aec8b73f84d84193fc03"

# @frappe.whitelist()
# def get_employees_from_grist(limit=10, offset=0):
#     """
#     Fetch paginated employee records from Grist API
#     """
#     headers = {
#         "Authorization": f"Bearer {GRIST_TOKEN}",
#         "Content-Type": "application/json"
#     }

#     params = {
#         "limit": int(limit),
#         "offset": int(offset)
#     }

#     try:
#         res = requests.get(GRIST_API_URL, headers=headers, params=params, timeout=150)
#         res.raise_for_status()
#         data = res.json()
#         return {
#             "records": data.get("records", []),
#             "limit": limit,
#             "offset": offset
#         }
#     except requests.exceptions.RequestException as e:
#         frappe.log_error(f"Grist API Error: {str(e)}", "get_employees_from_grist")
#         return {"records": [], "limit": limit, "offset": offset}



