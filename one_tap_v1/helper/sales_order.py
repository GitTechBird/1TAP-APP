import frappe
from .doctype import Doctype

def create_sales_order(data):
    try:
        sales_doc = frappe.get_doc({
            "doctype": Doctype.SALES_ORDER,
            "customer": data['customer_id'],
            # "company": data['company'],
            "selling_price_list": "1tap_AE_price",
            # "discount_amount": 225,
            "items":[{"item_code": data['item_code'],"delivery_date": "2025-03-27", "qty": 1.0}]
        })
        sales_doc.insert(ignore_permissions=True)
    except Exception as e:
        return e