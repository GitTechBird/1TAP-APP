import frappe
from .doctype import Doctype

def create_sales_invoice(data):
    try:
        sales_invoice_doc = frappe.get_doc({
            "doctype": Doctype.SALES_INVOICE,
            # "company": data['company'],
            "customer": data['customer_id'],
            "selling_price_list": "1tap_AE_price",
            # "discount_amount": 225,
            "items":[
                {    
                    "qty": 1,
                    "item_code": data['item_code'],
                    "item_name": data['item_name'],
                    "rate": data['item_price']
                }
            ]
        })
        sales_invoice_doc.insert(ignore_permissions=True)
    except Exception as e:
        return e