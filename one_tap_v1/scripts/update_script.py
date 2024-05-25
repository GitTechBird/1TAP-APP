import frappe
import time
from .for_server_script import create_template
@frappe.whitelist()
def update_business_catergory_attributes_custom():
    documents = frappe.get_list('OT Business Activity')
    idx = 0
    for doc in documents:
        idx += 1
        print(idx, doc.name)
        # if idx == 10:
        #     break
        otba_doc = frappe.get_doc("OT Business Activity", doc.name)
        
        # Initialize the attributes field if necessary
        # if not otba_doc.activity_item_attributes:
        #     otba_doc.activity_item_attributes = []
        
        attributes_list = [
            {
                "attribute": "OT Visa Number attributes",
                "from_range": 0,
                "to_range": 4,
                "numeric_values": 1,
                "increment": 1
            },
            {
                "attribute": "OT Visa Years attributes",
                "from_range": 1,
                "to_range": 5,
                "numeric_values": 1,
                "increment": 1
            }
        ]

        # Set the child table using the attributes list directly
        otba_doc.set('activity_item_attributes', [])

        for attr in attributes_list:
            otba_doc.append('activity_item_attributes', attr)

        # Save the parent document
        otba_doc.save()
        frappe.db.commit()
        
        # Optionally, add a time delay if needed
        # time.sleep(30)
    
def generate_items():
    activity_list = frappe.get_list("OT Business Activity", fields=["name"])
    for activity in activity_list:
        # if activity.business_activity_group_name:
        create_template(activity.name)
        # time.sleep(30)
        print(activity)

def update_items_on_activity_group_name_change():
    pass

def update_item_price_on_zone_master_price_update():
    pass

def update_item_price_on_activity_additional_price_update():
    pass