import frappe
from .customer import get_customer_name
from .doctype import Doctype

def get_user_issues_helper(user_email):
    # Finding Customer Email
    customer_name = get_customer_name(user_email)
    # Find Related Projects for the Customer
    issue_fields = ["name","subject","customer","raised_by","description"]
    project_filters={"customer": customer_name}
    projects = frappe.get_all(doctype=Doctype.ISSUE, filters=project_filters, fields=issue_fields)
    return projects