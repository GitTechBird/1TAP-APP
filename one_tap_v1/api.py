import frappe
import requests
import json
from frappe.twofactor import confirm_otp_token
from frappe.auth import LoginManager
from .helper.activity.activity import activity_search_helper
from .helper.user import create_portal_user_helper, update_user_password
from .helper.project import get_user_projects_helper 
from .helper.issue import get_user_issues_helper
from .helper.item import item_search_helper_new
from .helper.user_customer import update_user_customers_doctype_helper
from .helper.item_price import update_item_price_on_zone_master_helper, update_item_price_on_activity_helper
from .helper.otp_helper import authenticate_for_2factor_modified, send_email_helper, generate_otp_helper, validate_otp_helper
from .helper.metadata import SERVICE_METADATA
from .helper.customer_details import fetch_customer_details_helper, update_customer_details_helper, fetch_customer_transaction_details_helper
from .helper.task import update_task_status_helper
from .helper.customer import next_steps_helper, is_customer_helper
from .helper.task import get_project_tasks_helper

@frappe.whitelist()
def get_user_projects(user_email):
    # user_data = json.loads(frappe.request.data)
    return get_user_projects_helper(user_email)

@frappe.whitelist()
def get_user_issues(user_email):
    return get_user_issues_helper(user_email)

@frappe.whitelist()
def create_portal_user():
    data = json.loads(frappe.request.data)
    return create_portal_user_helper(data)

# Item Searching
@frappe.whitelist()
def item_search():
    data = frappe.request.json
    return item_search_helper_new(data)

@frappe.whitelist()
def activity_search():
    args = frappe.form_dict
    return activity_search_helper(args)

# POST request
@frappe.whitelist()
def update_user_customers_doctype(user_email, customer_email):
    return update_user_customers_doctype_helper(user_email, customer_email)

## OTP 
@frappe.whitelist(allow_guest=True)
def generate_otp():
    # data = frappe.request.json
    # return generate_otp_helper(data)
    data = frappe.request.json
    if user_exists(data.get('email')):
        return generate_otp_helper(data)
    else:
        return "Email not found"

@frappe.whitelist(allow_guest=True)
def validate_otp():
    data = frappe.request.json
    return validate_otp_helper(data)

@frappe.whitelist()
def send_email():
    user_email = frappe.request.json.get('user_email')
    subject = frappe.request.json.get('subject', None)
    message = frappe.request.json.get('message', None)
    return send_email_helper(user_email, subject, message)

@frappe.whitelist(allow_guest=True)
def user_exists(email):
    user = frappe.db.exists("User", {"email": email})
    if user:
        # return "User exists"
        return True
    else:
        # return "User does not exist"
        return False

@frappe.whitelist(allow_guest=True)
def generate_otp_for_user():
    data = frappe.request.json
    if not user_exists(data.get('email')):
        return generate_otp_helper(data)
    else:
        return "Email aleady in use"

@frappe.whitelist(allow_guest=True)
def validate_otp_for_user():
    data = frappe.request.json
    if validate_otp_helper(data):
        return create_user(data)
    else:
        return Exception("Otp Invalid")

@frappe.whitelist(allow_guest=True)
def validate_otp_and_update_password():
    data = frappe.request.json
    if validate_otp_helper(data):
        return update_user_password(data)
    else:
        return Exception("Otp Invalid")

@frappe.whitelist(allow_guest=True)
def create_user(data):
    doc = frappe.get_doc(
        {
            "doctype": "User",
            "email": data['email'],
            "first_name": data['first_name'],
            "last_name": data['last_name'],
            "new_password": data['password'],
            "roles": data.get('roles', []),
        }
    )
    doc.insert(ignore_permissions=True)
    frappe.db.commit()
    return "User created successfully"

@frappe.whitelist()
def next_steps():
    data = frappe.request.json
    return next_steps_helper(data)

@frappe.whitelist()
def get_metadata():
    return SERVICE_METADATA

# Customer Details
@frappe.whitelist()
def fetch_customer_details(customer_id):
    return fetch_customer_details_helper(customer_id)

@frappe.whitelist()
def fetch_customer_transaction_details(customer_detail_id):
    return fetch_customer_transaction_details_helper(customer_detail_id)

@frappe.whitelist()
def update_customer_details():
    data = frappe.request.json
    return update_customer_details_helper(data)

# Task
@frappe.whitelist()
def update_task_status():
    data = frappe.request.json
    return update_task_status_helper(data)

@frappe.whitelist()
def get_project_tasks(project_id):
    return get_project_tasks_helper(project_id)

@frappe.whitelist()
def is_customer(email):
    return is_customer_helper(email)
