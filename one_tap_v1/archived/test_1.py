import requests
import frappe
import json

"""
    customer_name
    email
    item_code
    item_price
    project_name
    project_templates
    company
"""
data = {
    "customer_name": "Demo Flow Cust",
    "email": "vishalaher83@gmail.com",
    # "email": "demoflow123@gmail.com",
    "item_code": "AE_RAKEZ_CompanySetup_General Trading-2-3",
    "item_price": "666",
    "project_name": "Demo Flow Project",
    "project_templates": ["Physical-office Template", "VISA-Registration Template"],
    "company": "TECHBIRD (Demo)",
    "roles": ["Agent", "1tap_test"]
}

@frappe.whitelist()
def next_steps():
    # data = frappe.request.json
    # Create Customer
	create_customer(data)
    # Update Customer / User Roles
	udapte_customer_roles(data)
    # Create Project
	create_project(data)
    # Create Sales Order    
	create_sales_order(data)
    # Create Sales Invoice
	create_sales_invoice(data)
    frappe.db.commit()
    # Send email

def create_customer(data):
	cus_doc = frappe.get_doc({
        "doctype": "Customer",
        "customer_name": data['customer_name'],
        "customer_type": "Company",
        "email_id": data['email'],
        "mobile_no": "454545545",
        "email_address": "sws@gmail.com",
        "mobile_number": "454545545"
    })
    cus_doc.insert(ignore_permissions=True)

def update_customer_roles(data):
	user = frappe.get_doc("User", {"email": data.get("email")})
    if user:
        for role in data.get("roles"):
            user.append("roles", {"role": role})
        # user.roles = roles
        user.flags.ignore_permissions = True  # Ignore permissions during save
        user.save()

def create_project(data):
	project_templates = []
    for template in data['project_templates']:
        project_templates.append({"template_name": template})
    project_doc = frappe.get_doc({
        "doctype": "Project",
        "project_name": data['project_name'],
        "project_templates": project_templates,
        "users": [
            {
                "user": "1tapcus@test.com"
            },
            {
                "user": "a@b.com"
            }
        ],
        "company": data['company'],
        "customer": data['customer_name'] 
    })
    project_doc.insert(ignore_permissions=True)

def create_sales_order(data):
	sales_doc = frappe.get_doc({
        "doctype": "Sales Order",
        "customer": data['customer_name'],
        "company": data['company'],
        "items":[{"item_code": data['item_code'],"delivery_date": "2024-03-27", "qty": 1.0}]
    })
    sales_doc.insert(ignore_permissions=True)

def create_sales_invoice(data):
	sales_invoice_doc = frappe.get_doc({
        "doctype": "Sales Invoice",
        "company": data['company'],
        "customer": data['customer_name'],
        "items":[
            {    
                "qty": 1,
                "item_code": data['item_code'],
                "item_name": "Headphones",
                "rate": data['item_price']
            }
        ]
    })
    sales_invoice_doc.insert(ignore_permissions=True)






def test1():
    # Update user roles
    user = frappe.get_doc("User", {"email": data.get("email")})
    if user:
        for role in data.get("roles"):
            user.append("roles", {"role": role})
        # user.roles = roles
        
        user.flags.ignore_permissions = True  # Ignore permissions during save
        user.save()
        frappe.db.commit()
        return "User roles updated successfully."
    else:
        return "User not found."
