import frappe
from .doctype import Doctype
from frappe.utils.password import update_password
def create_portal_user_helper(data):
    # if not frappe.db.exists("Customer", data["customer_name"]):
    # frappe.throw(f"Customer {data["customer_name"]} does not exist.")
    portal_user = frappe.new_doc("Portal User")

    # Set the required fields
    portal_user.update({
        "user": data['user_email'],
        "enabled": 1,
        "send_welcome_email": 0,
        "password": data['user_password'],
        "customer": data['customer_name'],
        "parent": data["customer_name"],
        "parenttype": "Customer"
    })

    # Save the portal user
    portal_user.insert(ignore_permissions=True)
    frappe.db.commit()

def update_user_password(data):
    user = frappe.get_doc("User", {"email": data['email']})
    if user:
        update_password(user.name, data['password'])
        user.save(ignore_permissions=True)
        frappe.db.commit()
        return "Password updated successfully"
        # pass
    else:
        return Exception("User not found")