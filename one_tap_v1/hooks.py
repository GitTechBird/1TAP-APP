# from one_tap_v1.helper.otp_helper import send_email_after_login
app_name = "one_tap_v1"
app_title = "one_tap_v1"
app_publisher = "one_tap_v1"
app_description = "one_tap_v1"
app_email = "admin@admin.com"
app_license = "mit"
# required_apps = []

# Includes in <head>
# ------------------
app_include_css = "/assets/one_tap_v1/css/custom.css"
app_include_js = "/assets/one_tap_v1/js/custom_navbar_display.js"

# include js, css files in header of desk.html
# app_include_css = "/assets/one_tap_v1/css/one_tap_v1.css"
# app_include_js = "/assets/one_tap_v1/js/one_tap_v1.js"

# include js, css files in header of web template
# web_include_css = "/assets/one_tap_v1/css/one_tap_v1.css"
# web_include_js = "/assets/one_tap_v1/js/one_tap_v1.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "one_tap_v1/public/scss/website"

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
# app_include_icons = "one_tap_v1/public/icons.svg"

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
# 	"methods": "one_tap_v1.utils.jinja_methods",
# 	"filters": "one_tap_v1.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "one_tap_v1.install.before_install"
# after_install = "one_tap_v1.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "one_tap_v1.uninstall.before_uninstall"
# after_uninstall = "one_tap_v1.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "one_tap_v1.utils.before_app_install"
# after_app_install = "one_tap_v1.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "one_tap_v1.utils.before_app_uninstall"
# after_app_uninstall = "one_tap_v1.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "one_tap_v1.notifications.get_notification_config"

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
#     "OT Zone Master": {
#         "on_change": "one_tap_v1.for_server_script.create_activity_items.after_save",
#         # "validate": "one_tap_v1.for_server_script.create_activity_items",
#         # "after_save": "my_app.module_name.file_name.after_save"
#     }
# }

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}

# "MyDocType": {
#         "before_save": "my_app.module_name.file_name.before_save",
#         "after_save": "my_app.module_name.file_name.after_save"
#     }

# doc_events = {
#     "OT Business Activity": {
#          "after_save": "one_tap_v1.for_server_script.create_activity_items.after_save",
#         # "validate": "one_tap_v1.for_server_script.create_activity_items",
#         # "after_save": "my_app.module_name.file_name.after_save"
#     }
# }
# your_app/hooks.py

doc_events = {
    "OT Zone Master": {
        "after_insert": "one_tap_v1.one_tap_v1.doctype.ot_zone_master.ot_zone_master.Ot_zone_master_change",
        "on_update": "one_tap_v1.one_tap_v1.doctype.ot_zone_master.ot_zone_master.Ot_zone_master_change",
    }
}



# doc_events = {
#     "OT Zone Master": {
#         "on_change": "one_tap.onetap_app.doctype.ot_zone_master.ot_zone_master.ot_zone_master_on_change"
        
#     }
# }


# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"one_tap_v1.tasks.all"
# 	],
# 	"daily": [
# 		"one_tap_v1.tasks.daily"
# 	],
# 	"hourly": [
# 		"one_tap_v1.tasks.hourly"
# 	],
# 	"weekly": [
# 		"one_tap_v1.tasks.weekly"
# 	],
# 	"monthly": [
# 		"one_tap_v1.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "one_tap_v1.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "one_tap_v1.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "one_tap_v1.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["one_tap_v1.utils.before_request"]
# after_request = ["one_tap_v1.utils.after_request"]

# Job Events
# ----------
# before_job = ["one_tap_v1.utils.before_job"]
# after_job = ["one_tap_v1.utils.after_job"]

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
# 	"one_tap_v1.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }
doc_events = {
    "Ifza copy1": {
        "validate": "one_tap_v1.web_form.ifza_copy1_webform1.validate_company"
    },
    "OT Zone Master": {
        "on_change": "one_tap_v1.one_tap_v1.doctype.ot_zone_master.ot_zone_master.update_item_price"
    },
    # "Item": {
    #     "on_trash": "one_tap.onetap_app.doctype.ot_zone_master.ot_zone_master.delete_item_price"
    # }
}

# my_custom_validation.py  file
# validate_company  function
# "validate": "my_app.my_module.my_custom_validation.validate_company"
website_route_rules = [
    {'from_route': '/1tap-test/<path:app_path>', 'to_route': '1tap-test'},
    {'from_route': '/service/<path:app_path>', 'to_route': 'service'},
    {"from_route": '/home/<path:app_path>', "to_route": 'home'},
    {"from_route": '/techhelpdesk/<path:app_path>', "to_route": 'techhelpdesk'},
]

# on_session_creation = "one_tap_v1.api2.send_email_after_login"
# on_login = "one_tap_v1.api1.get_live_sessionn"

# on_session_creation = [
#     "one_tap_v1.api2.send_email_after_login",
#     "one_tap_v1.api1.get_live_sessionn"
# ]

# on_session_creation = [
#     "one_tap_v1.api3.handle_after_login"
# ]