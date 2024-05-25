import frappe
from .customer import get_customer_name
from .doctype import Doctype


def get_user_projects_helper(user_email):
    # Finding Customer Email
    customer_name = get_customer_name(user_email)
    # Find Related Projects for the Customer
    project_fields=["name","project_name","is_active","status","priority","company"]
    project_filters={"customer": customer_name}
    projects = frappe.get_all(doctype=Doctype.PROJECT, filters=project_filters, fields=project_fields)
    return projects

def create_project(data):
    project_templates = []
    for template in data['project_templates']:
        project_templates.append({"template_name": template})
    project_doc = frappe.get_doc({
        "doctype": Doctype.PROJECT,
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