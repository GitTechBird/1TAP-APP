import frappe
import json

@frappe.whitelist()
def ping():
    return 'pong'

@frappe.whitelist()
def get_activity_group():
    args = frappe.form_dict
    keyword = args.get('keyword') 
    search_pattern = f"%{keyword}%"

    # Search the activity group table for the keyword
    bag_doctype = "OT Business Activity Old"
    or_filters = [
      {"activity_group": ["like", search_pattern]},
      {"activity_name": ["like", search_pattern]},
    ]
    activity_groups = frappe.get_all(bag_doctype, or_filters=or_filters, fields=["activity_group_id", "activity_group", "activity_id","activity_name"])
    temp_response = {}
    groups = []
    for obj in activity_groups:
        if obj.activity_group not in groups:
            groups.append(obj.activity_group)
            temp_response[obj.activity_group] = {
                "activity_group_name": obj.activity_group,
                "activity_group_id": obj.activity_group_id,
                "activities": [
                    {
                        "activity_name": obj.activity_name,
                        "activity_id": obj.activity_id
                    },
                ]
            }
        else:
            temp_response[obj.activity_group]['activities'].append({
                "activity_name": obj.activity_name,
                "activity_id": obj.activity_id
            })
    response = []
    for v in temp_response.values():
        response.append(v)
    return response

@frappe.whitelist()
def get_user_projects():
    try:
        user_data = json.loads(frappe.request.data)
        # Finding Customer Email
        user_email = user_data['email']
        customer_name = get_customer_name(user_email)
        # Find Related Projects for the Customer
        project_fields=["name","project_name","is_active","status","priority","company"]
        project_filters={"customer": customer_name}
        projects = frappe.get_all(doctype="Project", filters=project_filters, fields=project_fields)
        return projects
    except Exception as e:
        return  e

def get_customer_name(user_email):
    user_filters = {"user_email": user_email}
    customer_email = frappe.get_value(doctype="User Customer", filters=user_filters, fieldname="customer_email")
    # Finding Customer Name
    cus_filters = {"email_id": customer_email}
    customer_name = frappe.get_value(doctype="Customer", filters=cus_filters, fieldname="customer_name")
    return customer_name

@frappe.whitelist()
def get_user_issues(user_email):
    try:
        # Finding Customer Email
        customer_name = get_customer_name(user_email)
        # Find Related Projects for the Customer
        issue_fields = ["name","subject","customer","raised_by","description"]
        project_filters={"customer": customer_name}
        projects = frappe.get_all(doctype="Issue", filters=project_filters, fields=issue_fields)
        return projects
    except Exception as e:
        return  e

@frappe.whitelist()
def create_portal_user():
    data = json.loads(frappe.request.data)
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

# Item Searching
@frappe.whitelist()
def item_search():
    args = frappe.form_dict
    activity_group = args.get("activity_group")
    search_pattern =  f"%{activity_group}%" 
    doctype = "OT Business Activity"
    or_filters = [
      {"business_activity_group_name": ["like", search_pattern]},
      {"business_activity_name": ["like", search_pattern]},
      {"business_activity_description":["like",search_pattern]},
    ]
    activity_group = frappe.get_all(doctype=doctype,or_filters=or_filters, fields=["item_generated_code","business_zone"])
    item_tempaltes = []
    for activity in activity_group:
        if activity.item_generated_code:
            item_tempaltes.append(activity.item_generated_code)
    all_items = []
    for template in item_tempaltes:
        items = frappe.get_list(doctype="Item",filters={"variant_of": template}, fields= ["name"])
        # if items:
        # return items
        for obj in items:
            item = frappe.get_doc("Item", obj.name)
            item_price= frappe.get_value(doctype="Item Price", filters={"item_code":item.item_code}, fieldname="price_list_rate")
            temp = {    
                    "item_price":item_price,
                    "item_name": item.item_name,
                    "item_code": item.item_code,
                    "description":item.description,
                    "business_zone": activity.business_zone
                }
            for attr in item.attributes:
                temp[modify_key_name(attr.attribute)] = attr.attribute_value
            all_items.append(temp)
    return all_items

def modify_key_name(key):
    key = key.lower()
    key = "_".join(key.split(" "))
    return key

# New and faster api response
from .search_function_new import search3
@frappe.whitelist()
def activity_search3():
    args = frappe.form_dict
    searchKey = args.get("query")
    search_result = search3(searchKey)
    # return search_result
    unique_activity_group_names = []
    response = []
    if search_result:
        for result in search_result:
            if  result['business_activity_group_name'] not in unique_activity_group_names:
                unique_activity_group_names.append(result['business_activity_group_name'])
                response.append({"business_activity_group_name": result['business_activity_group_name']})
    return response


# # Old and Slower api response
# from .search_function import search1
# @frappe.whitelist()
# def activity_search1():
#     args = frappe.form_dict
#     searchKey = args.get("query")
#     activities = frappe.get_all("OT Business Activity", limit=250, fields=["business_activity_name", "business_activity_group_name", "business_activity_description"])
#     data = []
#     for activity in activities:
#         data.append({
#             "business_activity_name": activity.business_activity_name if activity.business_activity_name else "",
#             "business_activity_group_name": activity.business_activity_group_name if activity.business_activity_group_name else "",
#             "business_activity_description": activity.business_activity_description if activity.business_activity_description else ""
#         })
#     # return activities
#     search_result = search1(data, searchKey)
#     unique_activity_group_names = []
#     response = []
#     for result in search_result:
#         if  result['business_activity_group_name'] not in unique_activity_group_names:
#             unique_activity_group_names.append(result['business_activity_group_name'])
#             response.append({"business_activity_group_name": result['business_activity_group_name']})
#     return response

# Expermimental - Intelligent search
from .search_function_experimental import search2
@frappe.whitelist()
def activity_search2():
    args = frappe.form_dict
    searchKey = args.get("query")
    search_result = search2(searchKey)
    # return search_result
    response = []
    if search_result:
        for activity_group_name in search_result:
                response.append({"business_activity_group_name": activity_group_name})
    return response

# Expermimental - Intelligent search adv
from .search_function_experimental_adv import search
@frappe.whitelist()
def activity_search():
    args = frappe.form_dict
    searchKey = args.get("query")
    search_result = search(searchKey)
    # return search_result
    response = []
    if search_result:
        for activity_group_name in search_result:
                response.append({"business_activity_group_name": activity_group_name})
    return response


# POST request
@frappe.whitelist()
def update_user_customers_doctype(user_email, customer_email):
    frappe.get_doc({
        "doctype": "User Customer",
        "user_email": user_email,
        "customer_email": customer_email
    }).insert()

@frappe.whitelist()
def make_payment():
    # Sales Order Generate
    
    # Customer Generate

    # User to Customer Mapping
    
    # Payment Entry
    
    # Invoice
    pass

# Update item price if the price in zone master is changed
@frappe.whitelist()
def update_item_price_on_zone_master():
    data = json.loads(frappe.request.data)
    zone_name = data['zone_name']
    fieldname = data['fieldname']
    updated_zone_field_price = data['updated_zone_field_price']
    visa_number = fieldname[0]
    visa_year = fieldname[6]
    
    # Determining Activity Price
    activities = frappe.get_all(doctype="OT Business Activity", filters={"business_zone": zone_name}, fields=["business_activity_group_name", "activity_additional_price"])
    for acitivty in activities:
        sql_query = """
            SELECT DISTINCT i.name, i.item_code
            FROM `tabItem` i
            INNER JOIN `tabItem Variant Attribute` a1 ON i.name = a1.parent
            INNER JOIN `tabItem Variant Attribute` a2 ON i.name = a2.parent
            WHERE i.item_group = %s
            AND (a1.attribute = 'OT Visa Number attributes' AND a1.attribute_value = %s)
            AND (a2.attribute = 'OT Visa Years attributes' AND a2.attribute_value = %s)            
        """
        items = frappe.db.sql(sql_query, (acitivty.business_activity_group_name, visa_number, visa_year), as_dict=True)
        for item in items:
            new_price = float(acitivty.activity_additional_price) + float(updated_zone_field_price)
            item_price_doc = frappe.get_doc("Item Price", {"item_code": item.item_code})
            frappe.db.set_value("Item Price", item_price_doc.name, "price_list_rate", new_price)
    frappe.db.commit()
    return "Price updated successfully"

# Update item price if the price in zone master is changed
@frappe.whitelist()
def update_item_price_on_activity():
    data = json.loads(frappe.request.data)
    activity_group_name = data['activity_group_name']
    activity_price = data['activity_price']

    # Determining Activity Price
    activity = frappe.get_doc(doctype="OT Business Activity", filters={"business_activity_group_name": activity_group_name})
    if activity:
        business_zone = activity.business_zone
        activity_price = activity.activity_additional_price
        if business_zone:
            zone_doc = frappe.get_doc(doctype="OT Zone Master", filters={"zone_name": business_zone}, as_dict=True)
            return zone_doc["0visa_1year"]
            for year in range(1,6):
                for visa in range(0,5):
                    key = f"{visa}visa_{year}year"
                    return zone_doc
                    # if item_zone:
                    #     temp = item_zone[0]
                    #     item_zone_price = temp[list(temp.keys())[0]]
                    #     item_zone_price = item_zone_price if item_zone_price else 0
                    
                    item_total_price = int(activity_price) + int(item_zone_price)
                    return vars(zone_doc)
                    return ans
        #     sql_query = """
        #         SELECT DISTINCT i.name, i.item_code
        #         FROM `tabItem` i
        #         INNER JOIN `tabItem Variant Attribute` a1 ON i.name = a1.parent
        #         INNER JOIN `tabItem Variant Attribute` a2 ON i.name = a2.parent
        #         WHERE i.item_group = %s
        #         AND (a1.attribute = 'OT Visa Number attributes' AND a1.attribute_value = %s)
        #         AND (a2.attribute = 'OT Visa Years attributes' AND a2.attribute_value = %s)            
        #     """
        #     items = frappe.db.sql(sql_query, (acitivty.business_activity_group_name, visa_number, visa_year), as_dict=True)
        #     for item in items:
        #         new_price = float(acitivty.activity_additional_price) + float(updated_zone_field_price)
        #         item_price_doc = frappe.get_doc("Item Price", {"item_code": item.item_code})
        #         frappe.db.set_value("Item Price", item_price_doc.name, "price_list_rate", new_price)
        # frappe.db.commit()
        # return "Price updated successfully"