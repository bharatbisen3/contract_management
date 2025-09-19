# Clade API 

import frappe
import requests
from datetime import datetime


GRIST_API_URL = "https://ljungan.getgrist.com/api/docs/bdCYnioEbuyGM6jMavS1Kf/tables/EMPLOYEE/records"
GRIST_TOKEN = "b83d20f59034284de9f2aec8b73f84d84193fc03"

@frappe.whitelist()
def import_employees_from_grist(limit=100, offset=0, update_existing=False):
    """
    Import employee records from Grist API to ERPNext Employee doctype
    
    Args:
        limit: Number of records to fetch (default: 100)
        offset: Offset for pagination (default: 0)
        update_existing: Whether to update existing employees (default: False)
    
    Returns:
        dict: Import summary with success/error counts
    """
    
    # Get data from Grist API
    grist_data = get_employees_from_grist(limit, offset)
    
    if not grist_data.get("records"):
        return {"status": "error", "message": "No records found in Grist API"}
    
    # Import summary
    summary = {
        "total_records": len(grist_data["records"]),
        "successful_imports": 0,
        "failed_imports": 0,
        "updated_records": 0,
        "skipped_records": 0,
        "errors": []
    }
    
    for record in grist_data["records"]:
        try:
            result = create_or_update_employee(record, update_existing)
            
            if result["status"] == "created":
                summary["successful_imports"] += 1
            elif result["status"] == "updated":
                summary["updated_records"] += 1
            elif result["status"] == "skipped":
                summary["skipped_records"] += 1
                
        except Exception as e:
            summary["failed_imports"] += 1
            error_msg = f"Record ID {record.get('id', 'Unknown')}: {str(e)}"
            summary["errors"].append(error_msg)
            frappe.log_error(error_msg, "Employee Import Error")
    
    return summary

def get_employees_from_grist(limit=100, offset=0):
    """
    Fetch paginated employee records from Grist API
    """
    headers = {
        "Authorization": f"Bearer {GRIST_TOKEN}",
        "Content-Type": "application/json"
    }

    params = {
        "limit": int(limit),
        "offset": int(offset)
    }

    try:
        res = requests.get(GRIST_API_URL, headers=headers, params=params, timeout=150)
        res.raise_for_status()
        data = res.json()
        return {
            "records": data.get("records", []),
            "limit": limit,
            "offset": offset
        }
    except requests.exceptions.RequestException as e:
        frappe.log_error(f"Grist API Error: {str(e)}", "get_employees_from_grist")
        return {"records": [], "limit": limit, "offset": offset}

def create_or_update_employee(grist_record, update_existing=False):
    """
    Create or update employee record in ERPNext
    
    Args:
        grist_record: Grist API record
        update_existing: Whether to update existing employees
    
    Returns:
        dict: Operation result
    """
    
    fields = grist_record.get("fields", {})
    
    # Map Grist fields to ERPNext Employee fields
    employee_data = map_grist_to_erpnext_fields(fields)
    
    # Check if employee already exists
    existing_employee = None
    if employee_data.get("employee_number"):
        existing_employee = frappe.db.exists("Employee", {"employee_number": employee_data["employee_number"]})
    
    # If employee exists and update_existing is False, skip
    if existing_employee and not update_existing:
        return {"status": "skipped", "employee": existing_employee}
    
    try:
        if existing_employee:
            # Update existing employee
            employee_doc = frappe.get_doc("Employee", existing_employee)
            for key, value in employee_data.items():
                if value is not None:  # Only update non-None values
                    employee_doc.set(key, value)
            employee_doc.save()
            return {"status": "updated", "employee": existing_employee}
        else:
            # Create new employee
            employee_doc = frappe.new_doc("Employee")
            employee_doc.update(employee_data)
            employee_doc.insert()
            return {"status": "created", "employee": employee_doc.name}
            
    except Exception as e:
        frappe.log_error(f"Error processing employee {employee_data.get('employee_name', 'Unknown')}: {str(e)}")
        raise

def map_grist_to_erpnext_fields(grist_fields):
    """
    Map Grist fields to ERPNext Employee doctype fields
    
    Args:
        grist_fields: Dictionary of Grist field values
    
    Returns:
        dict: Mapped ERPNext Employee fields
    """
    
    # Helper function to convert timestamp to date
    def timestamp_to_date(timestamp):
        if timestamp and timestamp > 0:
            return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
        return None
    
    # Helper function to get gender
    def get_gender(gender_str):
        if isinstance(gender_str, str):
            if gender_str.lower() == 'male':
                return 'Male'
            elif gender_str.lower() == 'female':
                return 'Female'
        return 'Other'
    
    # Helper function to get status
    def get_status():
        # Check if employee is active
        active = grist_fields.get("Active", "False") or grist_fields.get("Active2", "False")
        return "Active" if active else "Inactive"

    # Helper function to format phone number with country code
    def format_phone_number(phone_number, country_code="SE"):
        if not phone_number:
            return ""
        
        # Convert to string and clean
        phone_str = str(phone_number).strip()
        if not phone_str:
            return ""
        
        # Country code mapping
        country_codes = {
            "SE": "+46",  # Sweden
            "NO": "+47",  # Norway
            "DK": "+45",  # Denmark
            "FI": "+358", # Finland
            "US": "+1",   # United States
            "GB": "+44",  # United Kingdom
            "DE": "+49",  # Germany
        }
        
        # Get country from Grist data or default to SE (Sweden)
        country = grist_fields.get("Country", "SE") or "SE"
        prefix = country_codes.get(country, "+46")  # Default to Sweden
        
        # If phone already has country code, return as is
        if phone_str.startswith("+"):
            return phone_str
        
        # Remove leading zeros and add country code
        if phone_str.startswith("0"):
            phone_str = phone_str[1:]
        
        return f"{prefix}{phone_str}"
    
    # Helper function to convert boolean to string for specific fields
    def boolean_to_string(value):
        if isinstance(value, bool):
            return "TRUE" if value else "FALSE"
        elif isinstance(value, str):
            if value.lower() in ["true", "1", "yes"]:
                return "TRUE"
            elif value.lower() in ["false", "0", "no"]:
                return "FALSE"
        return ""
    

    
    # Map the fields
    employee_data = {
        # Basic Information
        "employee_number": str(grist_fields.get("BL_ID", "")),
        "first_name": grist_fields.get("First_Name2", ""),
        "middle_name": grist_fields.get("Middle_Name", ""),
        "last_name": grist_fields.get("Last_Name", ""),
        "employee_name": grist_fields.get("Full_Name", ""),
        "gender": get_gender(grist_fields.get("Gender")),
        "date_of_joining": timestamp_to_date(grist_fields.get("Date_of_Joining")),
        "date_of_birth": timestamp_to_date(946684800),
        "status": get_status(),
        
        # Contact Details
        # "cell_number": str(grist_fields.get("Contact_Number", "")) if grist_fields.get("Contact_Number") else "",
        # "cell_number": format_phone_number(str(grist_fields.get("Contact_Number", "")) if grist_fields.get("Contact_Number") else ""),
        # "cell_number": format_phone_number(grist_fields.get("Contact_Number")),
        "personal_email": grist_fields.get("Email_Address", ""),
        "company_email": grist_fields.get("Email", ""),
        "prefered_contact_email": grist_fields.get("Email_Address", ""),
        
        # Address Information
        "current_address": f"{grist_fields.get('Address_1', '')}\n{grist_fields.get('Address_2', '')}".strip(),
        "permanent_address": f"{grist_fields.get('Address_1', '')}\n{grist_fields.get('Address_2', '')}".strip(),
        
        # Employment Details
        # "contract_end_date": timestamp_to_date(grist_fields.get("End_Date")),
        
        # Bank Details
        "bank_name": grist_fields.get("Bank", ""),
        "bank_ac_no": str(grist_fields.get("Bank_Account_Number", "")) if grist_fields.get("Bank_Account_Number") else "",
        
        # Custom Fields
        "custom_social_security_number": grist_fields.get("Social_Security_Number_2", ""),
        "custom_preferred_name": grist_fields.get("Preferred_Name", ""),
        "custom_your_bank_account_number": str(grist_fields.get("Bank_Account_Number", "")) if grist_fields.get("Bank_Account_Number") else "",
        "custom_bic_code": grist_fields.get("BIC_Code", ""),
        "custom_bank": grist_fields.get("Bank", ""),
        # "custom_country": grist_fields.get("Country", ""),
        "custom_city": grist_fields.get("City2", ""),
        "custom_zip__postal_code": str(grist_fields.get("Zip_Postal_code", "")) if grist_fields.get("Zip_Postal_code") else "",
        "custom_address_2": grist_fields.get("Address_2", ""),
        "custom_address": grist_fields.get("Address_1", ""),
        "custom_email_address": grist_fields.get("Email_Address", ""),
        "custom_contact_number": str(grist_fields.get("Contact_Number", "")) if grist_fields.get("Contact_Number") else "",
        "custom_citizenship": grist_fields.get("Citizenship", ""),
        # "custom_country_of_birth": grist_fields.get("Country_of_Birth", ""),
        "custom_blid": str(grist_fields.get("BL_ID2", "")) if grist_fields.get("BL_ID2") else "",
        "custom_work_place_id": grist_fields.get("Work_Place_ID", ""),
        # "custom_end_date": timestamp_to_date(grist_fields.get("End_Date")),
        "custom_tax_table": str(grist_fields.get("Tax_Table", "")) if grist_fields.get("Tax_Table") else "",
        "custom_tax_adjustment__tax_relief": boolean_to_string(grist_fields.get("Tax_adjustment_tax_relief", False)),
        "custom_asink_tax": boolean_to_string(grist_fields.get("ASINK_Tax", "False")),
        "custom_sink_tax": boolean_to_string(grist_fields.get("SINK_Tax2", "False")),
        # "custom_tax_tablebased_taxation": grist_fields.get("Tax_Table_Based_Taxation2", False),
        "custom_tax_tablebased_taxation": boolean_to_string(grist_fields.get("Tax_Table_Based_Taxation2")),
        "custom_project": boolean_to_string(grist_fields.get("Project", False)),
        "custom_cost_bearer": str(grist_fields.get("Cost_Bearer", "")) if grist_fields.get("Cost_Bearer") else "",
        "custom_cost_center": boolean_to_string(grist_fields.get("Cost_Center", False)),
        "custom_team_leader": boolean_to_string(grist_fields.get("Team_Leader", False)),
        "custom_fora_fok": grist_fields.get("ForaFOK", ""),
        "custom_fora_exception": boolean_to_string(grist_fields.get("FORA_Exception", False)),
        "custom_please_attach_your_valid_id_or_passport": grist_fields.get("ID_Passport", ""),
        "custom_code_of_conduct": grist_fields.get("Code_of_Conduct", "")
    }
    
    # Handle Tax Column (appears to be a list in Grist)
    tax_column = grist_fields.get("Tax_Column")
    if tax_column and isinstance(tax_column, list) and len(tax_column) > 0:
        employee_data["custom_tax_column"] = tax_column[0]  # Take first value
    
    # Remove None values
    employee_data = {k: v for k, v in employee_data.items() if v is not None and v != ""}
    
    return employee_data

@frappe.whitelist()
def bulk_import_all_employees():
    """
    Import all employees from Grist API with pagination
    """
    
    total_summary = {
        "total_records": 0,
        "successful_imports": 0,
        "failed_imports": 0,
        "updated_records": 0,
        "skipped_records": 0,
        "errors": []
    }
    
    limit = 100
    offset = 0
    
    while True:
        batch_summary = import_employees_from_grist(limit, offset, update_existing=False)
        
        if batch_summary.get("total_records", 0) == 0:
            break
        
        # Aggregate summaries
        total_summary["total_records"] += batch_summary.get("total_records", 0)
        total_summary["successful_imports"] += batch_summary.get("successful_imports", 0)
        total_summary["failed_imports"] += batch_summary.get("failed_imports", 0)
        total_summary["updated_records"] += batch_summary.get("updated_records", 0)
        total_summary["skipped_records"] += batch_summary.get("skipped_records", 0)
        total_summary["errors"].extend(batch_summary.get("errors", []))
        
        offset += limit
        
        # If we got fewer records than the limit, we've reached the end
        if batch_summary.get("total_records", 0) < limit:
            break
    
    return total_summary


