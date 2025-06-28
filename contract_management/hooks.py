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

override_doctype_class = {
# 	"Job Offer": "override.custom_job_offer.custom_job_offer"
	"Job Offer": "contract_management.custom_job_offer.custom_job_offer",
	"Employee": "contract_management.CustomEmployee.CustomEmployee"
}
# apps/contract_management/contract_management/custom_job_offer.py


# contract_management/override/custom_job_offer

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

# scheduler_events = {
#     "cron": {
#         "29 17 * * *": [
#             "contract_management.contract_management.doctype.project_setup.project_setup.send_open_project_reminders"
#             # "contract_management.api.project_email.send_open_project_reminders"
#         ]
#     }
# }


scheduler_events = {
    "cron": {
        "*/2 * * * *": [
            "contract_management.contract_management.doctype.project_setup.project_setup.send_open_project_reminders"
        ]
    }
}

# apps/contract_management/contract_management/contract_management/doctype/project_setup/project_setup.py

# scheduler_events = {
#     "hourly": [
#             "contract_management.contract_management.doctype.project_setup.project_setup.send_open_project_reminders"
#     ]
# }






# Testing
# -------

# before_tests = "contract_management.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	# "frappe.desk.doctype.event.event.get_events": "contract_management.event.get_events"
# 	"hrms.hr.doctype.job_offer.job_offer.send_email": "override.custom_job_offer.send_email"
#     # hrms.hrms.hr.doctype.job_offer.job_offer.py
#     # apps/contract_management/contract_management/override/custom_job_offer.py
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


fixtures = [
    # "Website Settings",
    # "Role Permission for Page and Report",  # For Role Permission Manager data
    # "Role Profile",
    # {"doctype": "Workspace"},  # Custom Workspaces
    # {"doctype": "Workspace"},  # Custom Workspaces
    # {"doctype": "Workspace Link"},  # Links inside workspaces (optional but recommended)
    # {"doctype": "Navbar Item", "filters": [["parent", "=", "Navbar Settings"]]},
    # {"doctype": "Workspace Shortcut"},
    # {"doctype": "Workspace Chart"},
    {
        "doctype": "Custom Field",
        "filters": [
            ["name", "in", [
                # "field2",
                "Job Applicant-custom_column_break_39erl",
                "Job Applicant-custom_salary_per_hour",
                "Job Applicant-custom_working_hours_per_week",
                "Job Applicant-custom_column_break_qmlxw",
                "Job Applicant-custom_employment_type",
                "Job Applicant-custom_end_date",
                "Job Applicant-custom_start_date",
                "Job Applicant-custom_details_by_hr_department",
                "Job Applicant-custom_please_attach_your_valid_id_or_passport",
                "Job Applicant-custom_section_break_f08xr",
                "Job Applicant-custom_bank_account_number",
                "Job Applicant-custom_bic_code",
                "Job Applicant-custom_column_break_nvhhj",
                "Job Applicant-custom_other_bank_name",
                "Job Applicant-custom_bank",
                "Job Applicant-custom_column_break_ym2kj",
                "Job Applicant-custom_bank_information",
                "Job Applicant-custom_mobilephone_number",
                "Job Applicant-custom_country",
                "Job Applicant-custom_stateprovince",
                "Job Applicant-custom_column_break_dqfbg",
                "Job Applicant-custom_city",
                "Job Applicant-custom_zippostal_code",
                "Job Applicant-custom_address_2",
                "Job Applicant-custom_address",
                "Job Applicant-custom_address__contact",
                "Job Applicant-custom_citizenship",
                "Job Applicant-custom_country_of_birth",
                "Job Applicant-custom_date_of_birth",
                "Job Applicant-custom_gender",
                "Job Applicant-custom_last_name",
                "Job Applicant-custom_middle_name",
                "Job Applicant-custom_column_break_s4gps",
                "Job Offer-custom_column_break_bjkjr",
                "Job Offer-custom_other_conditions",
                "Job Offer-custom_termination_of_the_employment__copy",
                "Job Offer-custom_collective_agreement",
                "Job Offer-custom_the_employment_protection_act",
                "Job Offer-custom_termination_of_the_employment_",
                "Job Offer-custom_according_to_collective_agreement_and_law_a",
                "Job Offer-custom_by_law_a",
                "Job Offer-custom_insurances",
                "Job Offer-custom_any_training_provided_by_the_employer",
                "Job Offer-custom_according_to_collective_agreement_and_law",
                "Job Offer-custom_by_law",
                "Job Offer-custom_holiday_right",
                "Job Offer-custom_the_salary_is_paid_on_the_25th_of_each_month",
                "Job Offer-custom_the_salary_is_paid_the_month_after_earning",
                "Job Offer-custom_pay_period",
                "Job Offer-custom_section_break_qbhud",
                "Job Offer-custom_plecework_pay_according_to_separate_agreement_",
                "Job Offer-custom_column_break_wxwcz",
                "Job Offer-custom_hourly_salary_in_sek_gross_salary",
                "Job Offer-custom_section_break_jdiyc",
                "Job Offer-custom_according_to_the_applicable_collective_agreement_",
                "Job Offer-custom_only_ordered_overtime_or_moretime",
                "Job Offer-custom_conditions_for_overtime_work_or_moretime_work",
                "Job Offer-custom_time_span_end",
                "Job Offer-custom_time_span_start",
                "Job Offer-custom_column_break_htpih",
                "Job Offer-custom_hours_per_week",
                "Job Offer-custom_terms_of_employment_",
                "Job Offer-custom_mission",
                "Job Offer-custom_part_of_above_emp_form",
                "Job Offer-custom_estimated_finish_date",
                "Job Offer-custom_estimated_starting_date",
                "Job Offer-custom_column_break_sfxve",
                "Job Offer-custom_seasonal_work",
                "Job Offer-custom_special_fixed_term_employment",
                "Job Offer-custom_probationary_employment_period_in_month",
                "Job Offer-custom_probationary_employment",
                "Job Offer-custom_basis_for_time_limitation",
                "Job Offer-custom_form_of_employment",
                "Job Offer-custom_workspace_text",
                "Job Offer-custom_workspace",
                "Job Offer-custom_the_exception_rule",
                "Job Offer-custom_the_alternative_rule",
                "Job Offer-custom_the_main_rule",
                "Job Offer-custom_place_of_employment_a1",
                "Job Offer-custom_place_of_employment_a",
                "Job Offer-custom_anytext",
                "Job Offer-custom_work_report",
                "Job Offer-custom_forest_planning",
                "Job Offer-custom_forest_planting",
                "Job Offer-custom_forest_clearing",
                "Job Offer-custom_the_work_includes_the_following_html",
                "Job Offer-custom_the_work_includes_the_following",
                "Job Offer-custom_job_duties",
                "Job Offer-custom_employment_and_workspace",
                "Job Offer-custom_please_attach_your_valid_id_or_passport",
                "Job Offer-custom_your_bank_account_number",
                "Job Offer-custom_bic_code",
                "Job Offer-custom_column_break_kpwkf",
                "Job Offer-custom_name_the_other_bank",
                "Job Offer-custom_bank",
                "Job Offer-custom_bank_information",
                "Job Offer-custom_country_a",
                "Job Offer-custom_stateprovince",
                "Job Offer-custom_city_a1",
                "Job Offer-custom_column_break_l7gju",
                "Job Offer-custom_zippostal_code_",
                "Job Offer-custom_address_2",
                "Job Offer-custom_applicant_address_a1",
                "Job Offer-custom_employee_address_a1",
                "Job Offer-custom_applicant_contact_number",
                "Job Offer-custom_citizenship_",
                "Job Offer-custom_country_of_birth_",
                "Job Offer-custom_date_of_birth",
                "Job Offer-custom_gender",
                "Job Offer-custom_last_name",
                "Job Offer-custom_middle_name",
                "Job Offer-custom_country",
                "Job Offer-custom_postcode_",
                "Job Offer-custom_city",
                "Job Offer-custom_address",
                "Job Offer-custom_column_break_no5ge",
                "Job Offer-custom_website",
                "Job Offer-custom_mobile_phone_number",
                "Job Offer-custom_email",
                "Job Offer-custom_organization_number",
                "Job Offer-custom_employer_information",
                "Job Offer-custom_employer",
                "Job Offer-custom_public_access_token",
                "Job Offer-custom_token",
                "Job Offer-custom_section_break_q2yiq",
                "Job Offer-custom_staff_personal_data",
                "Employee-custom_email_address",
                "Employee-custom_contact_number",
                "Employee-custom_citizenship",
                "Employee-custom_country_of_birth",
                "Employee-custom_your_bank_account_number",
                "Employee-custom_please_attach_your_valid_id_or_passport",
                "Employee-custom_your_bank_account_number_a",
                "Employee-custom_name_the_other_bank",
                "Employee-custom_column_break_ovdd5",
                "Employee-custom_bic_code",
                "Employee-custom_bank",
                "Employee-custom_bank_information",
                "Employee-custom_country",
                "Employee-custom_stateprovince",
                "Employee-custom_city",
                "Employee-custom_column_break_vyq4y",
                "Employee-custom_zip__postal_code",
                "Employee-custom_address_2",
                "Employee-custom_address",
                "Employee-custom_address_information",
                "Employee-provident_fund_account",
                "Employee-micr_code",
                "Employee-pan_number",
                "Employee-ifsc_code",
                "Employee-bank_cb",
                "Employee-payroll_cost_center",
                "Employee-salary_cb",
                "Employee-shift_request_approver",
                "Employee-column_break_45",
                "Employee-leave_approver",
                "Employee-expense_approver",
                "Employee-approvers_section",
                "Employee-health_insurance_no",
                "Employee-health_insurance_provider",
                "Employee-health_insurance_section",
                "Employee-default_shift",
                "Employee-grade",
                "Employee-job_applicant",
                "Employee-employment_type",
                "Job Offer-custom_estimated_dates",
                "Job Offer-custom_basis_for_time_limitation_a",
                "Job Offer-custom___",
                "Job Offer-custom______",
                "Job Offer-custom_jd_agriment",
                "Job Offer-custom_requested_on",
                "Job Offer-custom_number_of_paid_holiday_days",
                "Job Offer-custom_workspace_new",
                "Job Offer-custom_collective_agreement_gs_union",
                "Job Offer-custom_training",
                "Job Offer-custom_the_employer_provides_adequate_training",
                "Job Offer-custom_deviating_regulations_a",
                "Job Offer-custom_terms_workinghours",
                "Job Applicant-custom_custom_zippostal_code"




            ]]
        ]
    },
    {
        "doctype": "Client Script",
        "filters": [
            ["name", "in", [
                # "field2",
                "Status Wise Attendance Block",
                "Set Total",
                "Send Attendance alert Button",
                "Employee Access to TL",
                "set request time",
                "contract timing",
                "Call Token and Email",
                "Button in Applicant",
                "Set Citizenship",
                "Get Work In Project",
                "Set Workspace",
                "Hide Add Button of PA",
                "Work Team TL",
                "Calculate Work",
                "Concat Project Name",
                "Insert From Project To Marked",
                "Filter ONly Team Leaders",
                "Date Range For Project Attendance",
                "Fetch Attendance Information",
                "Contract Status",
                "Other Bank Validation",
                "Table Employee Id",
                "SpecializationDropdown",
                "Make dates editable",
                "Ins BL Into Emp"
            ]]
        ]
    },
    {
        "doctype": "Property Setter",
        "filters": [
            ["name", "in", [
                # "field2",
                # "field2",
                "Job Applicant-country-report_hide",
                "Job Applicant-country-print_hide",
                "Job Applicant-country-hidden",
                "Job Applicant-main-field_order",
                "Job Applicant-applicant_name-report_hide",
                "Job Applicant-applicant_rating-in_list_view",
                "Job Applicant-status-in_list_view",
                "Job Applicant-applicant_name-in_list_view",
                "Job Applicant-job_title-in_list_view",
                "Job Applicant-section_break_16-hidden",
                "Job Applicant-section_break_6-hidden",
                "Job Applicant-source_and_rating_section-hidden",
                "Job Applicant-phone_number-hidden",
                "Job Applicant-details_section-label",
                "Job Applicant-designation-hidden",
                "Job Applicant-job_title-hidden",
                "Job Applicant-applicant_name-label",
                "Job Applicant-section_break_16-report_hide",
                "Job Applicant-section_break_16-print_hide",
                "Job Applicant-section_break_6-report_hide",
                "Job Applicant-section_break_6-print_hide",
                "Job Applicant-source_and_rating_section-report_hide",
                "Job Applicant-source_and_rating_section-print_hide",
                "Job Offer-main-field_order",
                "Job Offer-designation-in_list_view",
                "Job Offer-applicant_email_address-in_list_view",
                "Job Offer-applicant_name-in_list_view",
                "Job Offer-company-report_hide",
                "Job Offer-company-print_hide",
                "Job Offer-company-hidden",
                "Job Offer-offer_date-report_hide",
                "Job Offer-offer_date-print_hide",
                "Job Offer-offer_date-hidden",
                "Job Offer-designation-report_hide",
                "Job Offer-designation-print_hide",
                "Job Offer-designation-hidden",
                "Job Offer-applicant_name-label",
                "Job Offer-status-hidden",
                "Job Offer-printing_details-report_hide",
                "Job Offer-printing_details-print_hide",
                "Job Offer-printing_details-hidden",
                "Job Offer-terms-report_hide",
                "Job Offer-terms-print_hide",
                "Job Offer-terms-hidden",
                "Job Offer-select_terms-report_hide",
                "Job Offer-select_terms-hidden",
                "Job Offer-section_break_14-report_hide",
                "Job Offer-section_break_14-print_hide",
                "Job Offer-section_break_14-hidden",
                "Job Offer-offer_terms-hidden",
                "Job Offer-section_break_4-hidden",
                "Employee-basic_information-label",
                "Employee-connections_tab-hidden",
                "Employee-exit-hidden",
                "Employee-profile_tab-hidden",
                "Employee-personal_details-hidden",
                "Employee-salary_information-hidden",
                "Employee-attendance_and_leave_details-hidden",
                "Employee-contact_details-hidden",
                "Employee-employment_details-hidden",
                "Employee-company_details_section-report_hide",
                "Employee-company_details_section-print_hide",
                "Employee-company_details_section-hidden",
                "Employee-main-field_order",
                "Employee-status-hidden",
                "Employee-salutation-report_hide",
                "Employee-salutation-print_hide",
                "Employee-salutation-hidden",
                "Employee-last_name-reqd",
                "Employee-email_address-in_list_view",
                "Employee-employee_name-in_list_view",
                "Employee-designation-in_list_view",
                "Employee-naming_series-options",
                "Job Applicant-custom_last_name-in_list_view",
                "Employee Contract-status-in_list_view",
                "Employee Contract-first_name-in_list_view",
                "Employee Contract-applicant_email-in_list_view",
                "Employee-create_user-hidden",
                "Employee-employee_number-hidden",
                "Employee-employee_number-reqd",
                "Employee-naming_series-reqd",
                "Employee-naming_series-hidden",
                "Job Offer-job_applicant-read_only",
                "Employee-date_of_joining-hidden"



            ]]
        ]
    }

]