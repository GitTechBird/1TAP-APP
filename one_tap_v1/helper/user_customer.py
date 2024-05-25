import frappe
from .doctype import Doctype

def update_user_customers_doctype_helper(user_email, customer_email):
    frappe.get_doc({
        "doctype": Doctype.USER_CUSTOMER,
        "user_email": user_email,
        "customer_email": customer_email
    }).insert()