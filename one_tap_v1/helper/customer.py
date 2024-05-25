import frappe
from .doctype import Doctype
from .sales_order import create_sales_order
from .sales_invoice import create_sales_invoice
from .otp_helper import send_email_helper
from .customer_details import update_customer_details_helper
# from .project import create_project


def get_customer_name(user_email):
    user_filters = {"user_email": user_email}
    customer_email = frappe.get_value(doctype=Doctype.USER_CUSTOMER, filters=user_filters, fieldname="customer_email")
    # Finding Customer Name
    cus_filters = {"email_id": customer_email}
    customer_name = frappe.get_value(doctype=Doctype.CUSTOMER, filters=cus_filters, fieldname="customer_name")
    return customer_name    

def update_customer_roles(data):
    try:
        customer_roles = ["1tap_test","Customer"]
        user = frappe.get_doc(Doctype.USER, {"email": data.get("email")})
        if user:
            for role in customer_roles:
                user.append("roles", {"role": role})
            # user.roles = roles
            user.flags.ignore_permissions = True  # Ignore permissions during save
            user.save()
    except Exception as e:
        return e

def create_customer(data, user_name):
    try:
        cus_doc = frappe.get_doc({
            "doctype": "Customer",
            "customer_name": user_name,
            "customer_type": "Company",
            "email_id": data['email']
        })
        cus_doc.insert(ignore_permissions=True)
        data['customer_id'] = cus_doc.name
    except Exception as e:
        return e

def next_steps_helper(data):
    try:
        # Get user name
        user_name = get_user_name(data['email'])
        if not frappe.db.exists(Doctype.CUSTOMER, {"email_id": data.get('email')}):
            # Create Customer
            create_customer(data, user_name)
            # Update Customer / User Roles
            update_customer_roles(data)
        else:
            cus_doc = frappe.get_doc(Doctype.CUSTOMER, {"email_id": data.get('email')})
            data['customer_id'] = cus_doc.name
        # #Create Project
        create_project(data)
        #Modify data for customer details and Update Customer Details
        modify_data_for_customer_details(data, user_name)
        update_customer_details_helper(data['customer_details'])
        # Create Sales Order    
        create_sales_order(data)
        # Create Sales Invoice
        create_sales_invoice(data)
        frappe.db.commit()
        # Send email
        send_email_helper(data["email"], "Welcome to 1Tap", "Your account has been created successfully.")
        return "Customer onboarded successfully!"
    except Exception as e:
        return e

def create_project(data):
    try:
        proj_templates = frappe.get_list(Doctype.PROJECT_TEMPLATE, filters={"project_type": "Company Incorporation"}, pluck="name")
        project_templates = []
        for template in proj_templates:
            project_templates.append({"template_name": template})
        
        # Find already created project for this user
        projects = frappe.get_all(Doctype.PROJECT, filters={"customer": data['customer_id']})
        idx = len(projects) + 1
        project_doc = frappe.get_doc({
            "doctype": Doctype.PROJECT,
            "project_name": "PROJ-" + data['customer_id'] + " - " + str(idx),
            "project_templates": project_templates,
            "customer": data['customer_id']
        })
        project_doc.insert(ignore_permissions=True)
        data['project_id'] = project_doc.name
    except Exception as e:
        return e

def get_user_name(email):
    user = frappe.get_doc(Doctype.USER, {"email": email})
    return user.full_name

def is_customer_helper(email):
    try:
        customer = frappe.get_doc(Doctype.CUSTOMER, {"email_id": email})
        return customer
    except Exception as e:
        return "Customer not found"

def modify_data_for_customer_details(data, user_name):
    if not data.get('customer_details', None):
        data['customer_details'] = {}
    data['customer_details']['customer_id'] = user_name
    data['customer_details']['user_email'] = data['email']
    data['customer_details']['item_code'] = data['item_code'] 
    data['customer_details']['project_id'] = data['project_id']