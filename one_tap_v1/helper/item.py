import frappe
import json
from .utility import modify_key_name
from .doctype import Doctype

def item_search_old_helper(args):
    activity_group = args.get("activity_group")
    search_pattern =  f"%{activity_group}%" 
    doctype = "OT Business Activity"
    or_filters = [
        {"business_activity_group_name": ["like", search_pattern]},
        {"business_activity_name": ["like", search_pattern]},
        {"business_activity_description":["like",search_pattern]},
    ]
    activity_group = frappe.get_all(doctype=Doctype.OT_BUSINESS_ACTIVITY,or_filters=or_filters, fields=["item_generated_code","business_zone"])
    item_tempaltes = []
    for activity in activity_group:
        if activity.item_generated_code:
            item_tempaltes.append(activity.item_generated_code)
    all_items = []
    for template in item_tempaltes:
        items = frappe.get_list(doctype=Doctype.Item,filters={"variant_of": template}, fields= ["name"])
        # if items:
        # return items
        for obj in items:
            item = frappe.get_doc(Doctype.Item, obj.name)
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

def item_search_helper(args):
    activity_group = args.get("activity_group")
    license_type = args.get("license_type")
    visa_number = args.get("visa_number")
    visa_year = args.get("visa_year")

    filters = {"business_activity_group_name": activity_group}
    if license_type:
        filters['license_type'] = license_type
    activities = frappe.get_all(doctype=Doctype.OT_BUSINESS_ACTIVITY,filters=filters, fields=["business_zone","business_activity_group_name","license_type"], group_by="business_activity_group_name")   
    resp = []
    if activities:
        activity = activities[0]
        items = search_items(activity_group, visa_year, visa_number)

        item_dict = {}
        for item_obj in items:
            item = frappe.get_doc(Doctype.ITEM,{"item_code": item_obj['item_code']})
            item_price = frappe.get_value(doctype="Item Price", filters={"item_code":item.item_code}, fieldname="price_list_rate")
            temp={
                "item_price":item_price,
                "item_name":item.item_name,
                "item_code":item.item_code,
                "description":item.description,
                "business_zone":activity.business_zone,
                "license_type":activity.license_type
            }
            for attr in item.attributes:
                temp[modify_key_name(attr.attribute)] = attr.attribute_value

            if not "item_group" in item_dict:
                item_dict["item_group"] = item.item_group           
            if not "items" in item_dict:
                item_dict["items"] = []
            item_dict["items"].append(temp)
        resp.append(item_dict)
    return resp


def search_items(item_group, visa_year_attribute, visa_number_attribute):
    sql_query = """
        SELECT DISTINCT i.name, i.item_code as item_code
        FROM `tabItem` i
        """
    params = []
    if visa_year_attribute:
        sql_query += " INNER JOIN `tabItem Variant Attribute` a1 ON i.name = a1.parent"
    if visa_number_attribute:
        sql_query += " INNER JOIN `tabItem Variant Attribute` a2 ON i.name = a2.parent"
    
    sql_query += " WHERE i.item_group = %s AND has_variants = 0"
    params.append(item_group)
    
    if visa_year_attribute:
        sql_query += " AND (a1.attribute = 'OT Visa Years attributes' AND a1.attribute_value = %s)"
        params.append(visa_year_attribute)
    if visa_number_attribute:
        sql_query += " AND (a2.attribute = 'OT Visa Number attributes' AND a2.attribute_value = %s)"
        params.append(visa_number_attribute)

    results = frappe.db.sql(sql_query, tuple(params), as_dict=True)
    return [{'name': r['name'], 'item_code': r['item_code']} for r in results]


# @frappe.whitelist(allow_guest=True)
# def item_search_helper_new():
# data = json.loads(frappe.request.data)
def item_search_helper_new(data):
    resp = []
    for obj in data["request"]:
        zone_code = obj['zone']
        activity_type = obj['type']
        zone = frappe.get_doc(Doctype.OT_ZONE_MASTER, {"zone_code": zone_code})
        zone_code_pattern = f"%{zone_code}%"
        activity_type_pattern = f"%{activity_type}%"
        filters = [
            {"item_name": ["like", zone_code_pattern]},
            {"item_name": ["like", activity_type_pattern]},
            {"has_variants": 0}
        ]
        
        items = frappe.get_all(doctype="Item" ,filters=filters, fields=["item_code"])
        all_items = []
        
        for item_obj in items:
            item = frappe.get_doc(Doctype.ITEM, {"item_code": item_obj['item_code']})
            item_price = frappe.get_value(doctype="Item Price", filters={"item_code":item.item_code}, fieldname="price_list_rate")
            temp={
                "item_price": item_price if item_price else 0,
                "item_name": item.item_name,
                "item_code": item.item_code,
                "description": item.description,
                "business_zone": zone_code
            }
            for attr in item.attributes:
                temp[modify_key_name(attr.attribute)] = attr.attribute_value
            all_items.append(temp)
        
        resp.append({
            "zone": obj['zone'],
            "type": obj['type'],
            "pros": zone.pros,  # Accessing pros field from zone document
            "cons": zone.cons,  
            "items": all_items
        })
    return resp