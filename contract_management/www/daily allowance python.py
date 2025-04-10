# Copyright (c) 2025, bharat and contributors
# For license information, please see license.txt

# # import frappe
# from frappe.model.document import Document


# class TimeAndDailyAllowance(Document):
# 	pass










# import frappe
# from frappe.model.document import Document

# class TimeAndDailyAllowance(Document):
#     pass

# def create_marked_attendance(doc, method):
#     frappe.enqueue(
#         "contract_management.contract_management.doctype.time_and_daily_allowance.time_and_daily_allowance.create_attendance_entries",
#         doc_name=doc.name
#     )

# def create_attendance_entries(doc_name):
#     doc = frappe.get_doc("Time and Daily Allowance", doc_name)

#     for row in doc.allowance_details:
#         # ✅ Only create entry if 'present' is "Yes" or "No"
#         if row.present in ["Yes", "No"]:
#             if not frappe.db.exists("Marked Attandance", {
#                 "employee": row.employee_id,
#                 "date": row.date
#             }):
#                 marked_attendance = frappe.get_doc({
#                     "doctype": "Marked Attandance",
#                     "employee": row.employee_id,
#                     "date": row.date,
#                     "duration": row.duration,
#                     "present": row.present,
#                     "allowance": row.allowance,
#                     "project": doc.project__client,
#                     "object": doc.object
#                 })
#                 marked_attendance.insert(ignore_permissions=True)
#                 frappe.db.commit()



























# import frappe
# from frappe.model.document import Document

# class TimeAndDailyAllowance(Document):
#     pass

# def create_marked_attendance(doc, method):
#     frappe.logger().info(f"🔎 Triggered for {doc.name}")
#     create_attendance_entries(doc.name)

# def create_attendance_entries(doc_name):
#     frappe.logger().info(f"Fetching Time and Daily Allowance doc: {doc_name}")
#     try:
#         doc = frappe.get_doc("Time and Daily Allowance", doc_name)
#         frappe.logger().info(f"Document fetched successfully: {doc.name}")

#         for row in doc.allowance_details:
#             frappe.logger().info(f"Row data -> Employee: {row.employee_id}, Date: {row.date}, Present: {row.present}")

#             if row.present in ["Yes", "No"]:
#                 existing_entry = frappe.db.exists("Marked Attandance", {
#                     "employee": row.employee_id,
#                     "date": row.date
#                 })
#                 frappe.logger().info(f"Existing entry status: {existing_entry}")

#                 if not existing_entry:
#                     frappe.logger().info(f"Creating new entry for {row.employee_id}")
                    
#                     marked_attendance = frappe.get_doc({
#                         "doctype": "Marked Attandance",
#                         "employee": row.employee_id,
#                         "date": row.date,
#                         "duration": row.duration,
#                         "present": row.present,
#                         "allowance": row.allowance,
#                         "project": doc.project__client,
#                         "object": doc.object
#                     })
#                     marked_attendance.insert(ignore_permissions=True)
#                     frappe.db.commit()

#                     frappe.logger().info(f"Inserted Marked Attendance for: {row.employee_id}")
#     except Exception as e:
#         frappe.logger().error(f"❌ Error in create_attendance_entries: {e}")















# New Code with another logic



# import frappe
# # from frappe.model.document import Document


# # class TimeAndDailyAllowance(Document):
# 	# pass

# def insert_into_marked_attendance(doc, method):
#     if not doc.start_date or not doc.end_date:
#         frappe.throw("Start Date and End Date are required.")
    
#     # Clear existing records to avoid duplication
#     frappe.db.delete("Marked Attandance", {"project": doc.project__client, "object": doc.object})
    
#     records_to_insert = []
    
#     # Fetch data from allowance_marked table
#     for row in doc.get("allowance_marked"):
#         if row.employee and row.date:
#             records_to_insert.append(
#                 (
#                     row.employee,
#                     row.date,
#                     row.duration or 8,   # Use default value if empty
#                     row.present or "No", # Default to 'No' if empty
#                     row.allowance or "No", # Default to 'No' if empty
#                     doc.project__client,
#                     doc.object
#                 )
#             )
    
#     # Insert into "Marked Attandance" using bulk_insert for better performance
#     if records_to_insert:
#         frappe.db.bulk_insert(
#             "Marked Attandance",
#             fields=["employee", "date", "duration", "present", "allowance", "project", "object"],
#             values=records_to_insert
#         )
    
#     # Commit changes to database
#     frappe.db.commit()
