import frappe
from .search_function import search

@frappe.whitelist()
def activity_search():
    args = frappe.form_dict
    searchKey = args.get("query")
    activities = frappe.get_all("OT Business Activity",limit=20, fields=["business_activity_name", "business_activity_group_name", "business_activity_description"])
    data = []
    for activity in activities:
        data.append({
            "business_activity_name": activity.business_activity_name if activity.business_activity_name else "",
            "business_activity_group_name": activity.business_activity_group_name if activity.business_activity_group_name else "",
            "business_activity_description": activity.business_activity_description if activity.business_activity_description else ""
        })
    # return activities
    return search(data, searchKey)