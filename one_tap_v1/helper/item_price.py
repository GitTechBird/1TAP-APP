import frappe
from .doctype import Doctype

def update_item_price_on_zone_master_helper(data):
    zone_name = data['zone_name']
    fieldname = data['fieldname']
    updated_zone_field_price = data['updated_zone_field_price']
    visa_number = fieldname[0]
    visa_year = fieldname[6]
    
    # Determining Activity Price
    activities = frappe.get_all(doctype=Doctype.OT_BUSINESS_ACTIVITY, filters={"business_zone": zone_name}, fields=["business_activity_group_name", "activity_additional_price"])
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
            item_price_doc = frappe.get_doc(Doctype.ITEM_PRICE, {"item_code": item.item_code})
            frappe.db.set_value(Doctype.ITEM_PRICE, item_price_doc.name, "price_list_rate", new_price)
    frappe.db.commit()
    return "Price updated successfully"

def update_item_price_on_activity_helper(data):
    activity_group_name = data['activity_group_name']
    activity_price = data['activity_price']

    # Determining Activity Price
    activity = frappe.get_doc(doctype=Doctype.OT_BUSINESS_ACTIVITY, filters={"business_activity_group_name": activity_group_name})
    if activity:
        business_zone = activity.business_zone
        activity_price = activity.activity_additional_price
        if business_zone:
            zone_doc = frappe.get_doc(doctype=Doctype.OT_ZONE_MASTER, filters={"zone_name": business_zone}, as_dict=True)
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