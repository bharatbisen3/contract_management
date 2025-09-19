# # import frappe
# # from erpnext.setup.doctype import employee as employee_module

# # def _ignore_relieving_date(self):
# #     """
# #     Custom validate_status that ignores relieving_date check.
# #     We replace ERPNext's method with this.
# #     """
# #     frappe.logger().info("⚡ Skipped relieving_date validation for Employee: {0}".format(self.name))

# #     # ✅ Do nothing: bypass relieving_date mandatory validation
# #     return

# # def apply_patch():
# #     """
# #     Apply monkey-patch for Employee.doctype
# #     """
# #     # Replace the method at runtime
# #     employee_module.employee.Employee.validate_status = _ignore_relieving_date
# #     frappe.logger().info("✅ Monkey patch applied: Employee.validate_status overridden")






# import frappe
# from erpnext.setup.doctype import employee as employee_module
# print(Employee.__module__)
# print(Employee.__name__)


# def _ignore_relieving_date(self):
#     """
#     Custom validate_status that ignores relieving_date check.
#     Logs when it is called.
#     """
#     frappe.logger().info(
#         f"⚡ Skipped relieving_date validation for Employee: {self.name}"
#     )
#     # ✅ Do nothing

# def apply_patch():
#     """
#     Apply monkey-patch for Employee doctype
#     """
#     employee_module.employee.Employee.validate_status = _ignore_relieving_date
#     frappe.logger().info("✅ Monkey patch applied: Employee.validate_status overridden")
