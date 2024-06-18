# Copyright (c) 2024, one_tap_v1 and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from .create_items_script import create_template_1, create_and_update_item_price, create_variant


class OTZoneMaster(Document):
    pass



def Ot_zone_master_change(doc, method):
    frappe.logger().info(f'QWERTY : {doc.name}')
    frappe.logger().debug('This is a debug message')
    frappe.logger().info('This is an info message')
    frappe.logger().warning('This is a warning message')
    frappe.logger().error('This is an error message')
    frappe.logger().critical('This is a critical message')



COUNTRY_CODE = "AE"
SERVICE_TYPE = "Company Setup"
ACTIVITY_TYPES = ["General Trading", "Regular Trading"]
VISA_MIN = 0
VISA_MAX = 4
YEAR_MIN = 1
YEAR_MAX = 5

# Current working for both functionalities i.e. create / update
def update_item_price(doc, method):
    # doc = frappe.get_doc("OT Zone Master", "Meydan Free Zone")
    zone_code = doc.zone_code
    zone_name = doc.zone_name
    for visa in range(VISA_MIN, VISA_MAX + 1):
        for year in range(YEAR_MIN, YEAR_MAX + 1):
            for activity_type in ACTIVITY_TYPES:
                key = f"{visa}visa_{year}year"
                template_name = f"{COUNTRY_CODE}_{zone_code}_{SERVICE_TYPE}_{activity_type}"
                item_code = f"{template_name}-{visa}-{year}"
                if activity_type == "General Trading":
                    key = key + "_gt"
    
                zone_key_price = getattr(doc, key)
                if zone_key_price:
                    print("-----------------------------")
                    print(key, zone_key_price, activity_type, item_code)
                    print("-----------------------------")
                    if frappe.db.exists("Item Price", {"item_code": item_code}):
                        item_price_doc = frappe.get_doc("Item Price", {"item_code": item_code})
                        if item_price_doc:
                            item_price_doc.price_list_rate = zone_key_price
                            print(key, "---", vars(item_price_doc), "-------------", zone_key_price, vars(doc))
                            item_price_doc.save()
                    else:
                        print(item_code, "not found")
                        attribute_values = {
                            "OT Visa Years attributes": str(year),
                            "OT Visa Number attributes": str(visa),
                        }
                        variant = create_variant(template_name, attribute_values)
                        variant.save()
                        # Create Item Price and update value for item_price
                        frappe.get_doc(
                            {
                                "doctype": "Item Price",
                                "item_code": item_code,
                                "item_name": item_code,
                                "price_list_rate": getattr(doc, key),
                                "price_list": "Standard Selling",
                            }
                        ).insert()
    frappe.db.commit()