app_name = "contract_management"
app_title = "Contract Management"
app_publisher = "bharat"
app_description = "This app is created for forest department"
app_email = "bharat@algoware.in"
app_license = "mit"


# web_include_css = "/assets/contract_management/css/asdfad.css"
# app_include_js = "/assets/contract_management/js/project_setup.js"

# web_include_css = "/assets/contract_management/css/workteam.css"



# send information form to applicant using email

# doc_events = {
#     "Prospect Applicant": {
#         "after_insert": "contract_management.contract_management.doctype.prospect_applicant.prospect_applicant.send_email_on_creation"
#     }
# }

#  Create Entry in Marked Attandance doctype using frappe.enqueue
# doc_events = {
#     "Time and Daily Allowance": {
#         "before_save": "contract_management.contract_management.doctype.time_and_daily_allowance.time_and_daily_allowance.create_attendance_entries"
#         # "before_save": "contract_management.contract_management.doctype.time_and_daily_allowance.time_and_daily_allowance.before_save"
#     }
# }

# doc_events = {
#     "Time and Daily Allowance": {
#         "before_save": "contract_management.contract_management.doctype.time_and_daily_allowance.time_and_daily_allowance.create_marked_attendance"
#     }
# }

# doc_events = {
#     "Time And Daily Allowance": {
#         "before_save": "contract_management.time_and_daily_allowance.insert_into_marked_attendance"
#     }
# }


# contract_management/contract_management/contract_management/doctype/project_setup/project_setup.py


# doc_events = {
#     "Verification By HR": {
#         "after_insert": "contract_management.contract_management.doctype.verification_by_hr.verification_by_hr.send_email_api"
#     }
# }


# Trying to create user permission automatically by project setup

# doc_events = {
#     "Project Setup": {
#         "before_save": "contract_management.contract_management.doctype.project_setup.project_setup.create_user_permission"
#     }
# }

# contract_management/contract_management/contract_management/doctype/project_setup/project_setup.py

# doc_events = {
#     "Project Setup": {
#         "after_insert": "contract_management.contract_management.doctype.project_setup.project_setup.create_user_permission"
#         # "before_save": "contract_management.contract_management.doctype.project_setup.project_setup.create_user_permission"
#         # "on_update": "contract_management.contract_management.doctype.project_setup.project_setup.create_user_permission"
#     }
# }






# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "contract_management",
# 		"logo": "/assets/contract_management/logo.png",
# 		"title": "Contract Management",
# 		"route": "/contract_management",
# 		"has_permission": "contract_management.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/contract_management/css/contract_management.css"
# app_include_js = "/assets/contract_management/js/contract_management.js"

# include js, css files in header of web template
# web_include_css = "/assets/contract_management/css/contract_management.css"
# web_include_js = "/assets/contract_management/js/contract_management.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "contract_management/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "contract_management/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "contract_management.utils.jinja_methods",
# 	"filters": "contract_management.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "contract_management.install.before_install"
# after_install = "contract_management.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "contract_management.uninstall.before_uninstall"
# after_uninstall = "contract_management.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "contract_management.utils.before_app_install"
# after_app_install = "contract_management.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "contract_management.utils.before_app_uninstall"
# after_app_uninstall = "contract_management.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "contract_management.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"contract_management.tasks.all"
# 	],
# 	"daily": [
# 		"contract_management.tasks.daily"
# 	],
# 	"hourly": [
# 		"contract_management.tasks.hourly"
# 	],
# 	"weekly": [
# 		"contract_management.tasks.weekly"
# 	],
# 	"monthly": [
# 		"contract_management.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "contract_management.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "contract_management.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "contract_management.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["contract_management.utils.before_request"]
# after_request = ["contract_management.utils.after_request"]

# Job Events
# ----------
# before_job = ["contract_management.utils.before_job"]
# after_job = ["contract_management.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"contract_management.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

