from . import __version__ as app_version

app_name = "tenantmanagementsystem"
app_title = "Tenant Management System"
app_publisher = "Stephen"
app_description = "Manage Tenant and Agents"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "wachangasteve@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/tenantmanagementsystem/css/tenantmanagementsystem.css"
# app_include_js = "/assets/tenantmanagementsystem/js/tenantmanagementsystem.js"

# include js, css files in header of web template
# web_include_css = "/assets/tenantmanagementsystem/css/tenantmanagementsystem.css"
# web_include_js = "/assets/tenantmanagementsystem/js/tenantmanagementsystem.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "tenantmanagementsystem/public/scss/website"

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

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "tenantmanagementsystem.install.before_install"
# after_install = "tenantmanagementsystem.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "tenantmanagementsystem.uninstall.before_uninstall"
# after_uninstall = "tenantmanagementsystem.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "tenantmanagementsystem.notifications.get_notification_config"
fixtures = [
    {
        "dt": "Client Script",
        "filters": [
            ["name", "in", ["Sales Invoice-Form", "Item-Form"]]
        ],
    },
    {
        "dt": "Custom Field",
        "filters": [
            [
                "name",
                "in",
                [
                    "Item-property",
                    "Item-property_name",
                    "Item-col_prop",
                    "Item-select_property",
                    "Sales Invoice-tenancy_contract",
                    "Sales Invoice-billing_period",
                    "Sales Invoice-arrears_note",
                    "Sales Invoice Item-remit_full_amount",
                    "Sales Invoice Item-remittable",
                    "Sales Invoice-property_unit",
                    "Purchase Invoice Item-not_landlord_expense",
                    "Purchase Invoice-owner_contract",
                    "Employee-assigned_property_unit",
                    "Employee-assigned_property",
                    "Sales Invoice-property_name",
                ],
            ]
        ],
    },
    {"dt": "Customer Group", "filters": [["name", "in", ["Tenants", "Landlords"]]]},
    {
        "dt": "Notification",
        "filters": [
            [
                "name",
                "in",
                [
                    "15 Days - Tenancy Contract Expiry Alert",
                    "1 Day - Tenancy Contract Expiry Alert",
                    "Tenancy Contract Ended",
                    "2 Days - Tenancy Contract Expiry Alert",
                    "5 Days - Tenancy Contract Expiry Alert",
                    "10 Days - Tenancy Contract Expiry Alert",
                    "30 Days - Tenancy Contract Expiry Alert",
                ],
            ]
        ],
    },
    {"dt": "Item Group", "filters": [["name", "in", ["Property Charge"]]]},
    {
        "dt": "Workflow",
        "filters": [["name", "in", ["Tenancy Contract", "Owner Contract"]]],
    },
    {
        "dt": "Workflow Action Master",
        "filters": [
            [
                "name",
                "in",
                [
                    "Cancel",
                    "Suspend",
                    "Terminate",
                    "Review",
                    "Reject",
                    "Approve",
                    "Activate",
                ],
            ]
        ],
    },
    {
        "dt": "Workflow State",
        "filters": [
            [
                "name",
                "in",
                [
                    "Rejected",
                    "Approved",
                    "Pending",
                    "New",
                    "Suspended",
                    "Cancelled",
                    "Terminated",
                    "Active",
                ],
            ]
        ],
    },
]

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
#	}
# }

doc_events = {
    "Sales Invoice": {
        "before_insert": "tenantmanagementsystem.tenant_management_system.hooks.doc_hooks.sales_invoice_arrears",
        "before_submit": "tenantmanagementsystem.tenant_management_system.hooks.doc_hooks.sales_invoice_arrears",
        "before_cancel": "tenantmanagementsystem.tenant_management_system.hooks.doc_hooks.sales_invoice_cancel",
    }
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"tenantmanagementsystem.tasks.all"
# 	],
# 	"daily": [
# 		"tenantmanagementsystem.tasks.daily"
# 	],
# 	"hourly": [
# 		"tenantmanagementsystem.tasks.hourly"
# 	],
# 	"weekly": [
# 		"tenantmanagementsystem.tasks.weekly"
# 	]
# 	"monthly": [
# 		"tenantmanagementsystem.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "tenantmanagementsystem.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "tenantmanagementsystem.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "tenantmanagementsystem.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


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
# 	"tenantmanagementsystem.auth.validate"
# ]

