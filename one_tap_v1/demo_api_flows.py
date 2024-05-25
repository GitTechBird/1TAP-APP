import requests
import frappe
import json

"""
    customer_name
    email
    item_code
    item_price
    project_name
    project_templates
    company
"""
data = {
    "customer_name": "Demo Flow Cust",
    "email": "demoflow123@gmail.com",
    "item_code": "123456",
    "item_price": "666",
    "project_name": "Demo Flow Project",
    "project_templates": ["Physical-office Template","VISA-Registration Template"],
    "company": "Demo flow Project",
}

# @frappe.whitelist()
# def generate():
#     data = frappe.request.json

#     # Create Customer
#     url = "http://13.233.216.191/api/resource/Customer"
#     body = {
#     "customer_name": data['customer_name'],
#     "customer_type": "Company",
#     "email_id": data['email'],
#     "mobile_no": "454545545",
#     "email_address": "sws@gmail.com",
#     "mobile_number": "454545545"
#     }
#     headers = {"Authorization": "token 71c26bf67dc93c9:9f6b42ec03533c8"}
#     response = requests.post(url, headers=headers, json=body)
#     print(response.json())
    
    
#     #create Project
#     url = "http://13.233.216.191/api/resource/Project"
#     body = {
#         "project_name": data['project_name'],
#         "project_templates": data['project_templates'],
#     # "users": [
#     #     {
#     #     "user": "1tapcus@test.com"
#     #     },
#     #     {
#     #     "user": "a@b.com"
#     #     }
#     # ],
#     # "company": data['company'],
#     # "customer": data['customer_name'] 
#     }
#     headers = {"Authorization": "token 71c26bf67dc93c9:9f6b42ec03533c8"}
#     response1 = requests.post(url, headers=headers, json=body)
#     return (response1.json())
    
    
    
#     # Create salesOrder
#     url = "http://13.233.216.191/api/resource/Sales%20Order"
    
#     body ={
#     "customer":data['customer_name'],
#     "company": data['company'],
#     "items":[{"item_code": data['item_code'],"delivery_date": "2024-03-17", "qty": 1.0}]

# }
#     headers = {"Authorization": "token 71c26bf67dc93c9:9f6b42ec03533c8"}
#     response2 = requests.post(url, headers=headers, json=body)
#     print(response2.json())
    
#     # Create Sales Invoice
#     url = "http://13.233.216.191/api/resource/Sales%20Invoice"
#     body = {
#     "company": data['company'],
#     "customer": data['customer_name'],
#     "items":
#     [
#         {    
#                 "qty": 1,
#                 "item_code": data['item_code'],
#                 "item_name": "Headphones",
#                 "rate": 221
#         }
#     ]
# }
#     headers = {"Authorization": "token 71c26bf67dc93c9:9f6b42ec03533c8"}
#     response3 = requests.post(url, headers=headers, json=body)
#     print(response3.json())

# @frappe.whitelist()
# def generate():
#     data = frappe.request.json
    
#     # Create Project
#     url = "http://13.233.216.191/api/resource/Project"
#     body = {
#         "project_name": data['project_name'],
#         "project_templates": data['project_templates'],
#     }
#     response1 = requests.post(url, headers=headers, json=body)
#     print(response1.json())
    
#     # Create Sales Order
#     url = "http://13.233.216.191/api/resource/Sales%20Order"
#     body = {
#         "customer": data['customer_name'],
#         "company": data['company'],
#         "items": [{"item_code": data['item_code'], "delivery_date": "2024-03-17", "qty": 1.0}]
#     }
#     response2 = requests.post(url, headers=headers, json=body)
#     print(response2.json())

#     # Create Customer
#     url = "http://13.233.216.191/api/resource/Customer"
#     body = {
#         "customer_name": data['customer_name'],
#         "customer_type": "Company",
#         "email_id": data['email'],
#         "mobile_no": "454545545",
#         "email_address": "sws@gmail.com",
#         "mobile_number": "454545545"
#     }
#     headers = {"Authorization": "token 71c26bf67dc93c9:9f6b42ec03533c8"}
#     response = requests.post(url, headers=headers, json=body)
#     print(response.json())
    

    
#     # Create Sales Invoice
#     url = "http://13.233.216.191/api/resource/Sales%20Invoice"
#     body = {
#         "company": data['company'],
#         "customer": data['customer_name'],
#         "items": [
#             {"qty": 1, "item_code": data['item_code'], "item_name": "Headphones", "rate": 221}
#         ]
#     }
#     response3 = requests.post(url, headers=headers, json=body)
#     print(response3.json())
    
#     # Return a response after all actions
#     return {"message": "All actions completed successfully."}

import requests
import frappe
import json

"""
    customer_name
    email
    item_code
    item_price
    project_name
    project_templates
    company
"""
data = {
    "customer_name": "Demo Flow Cust",
    "email": "demoflow123@gmail.com",
    "item_code": "AE_RAKEZ_CompanySetup_General Trading-2-3",
    "item_price": "666",
    "project_name": "Demo Flow Project",
    "project_templates": [
        {
            "template_name": "Physical-office Template"
        },
        {
            "template_name":"VISA-Registration Template"
        }
    ],
    "company": "TECHBIRD (Demo)",
    "first_name":"snehal",
    "roles":["1tap_test","Agent"]
}


@frappe.whitelist()
def call1():
    try:
        data = frappe.request.json

        # Create Customer
        cus_doc = frappe.get_doc({
            "doctype": "Customer",
            "customer_name": data['customer_name'],
            "customer_type": "Company",
            "email_id": data['email'],
            "mobile_no": "454545545",
            "email_address": "sws@gmail.com",
            "mobile_number": "454545545"
        })
        cus_doc.insert(ignore_permissions=True)
        
        # Create Project
        project_doc = frappe.get_doc({
            "doctype": "Project",
            "project_name": data['project_name'],
            "project_templates": data['project_templates'],
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

        # Create Sales Order    
        sales_doc = frappe.get_doc({
            "doctype": "Sales Order",
            "customer": data['customer_name'],
            "company": data['company'],
            "items":[{"item_code": data['item_code'],"delivery_date": "2024-11-17", "qty": 1.0}]
        })
        sales_doc.insert(ignore_permissions=True)

        # Create Sales Invoice
        sales_invoice_doc = frappe.get_doc({
            "doctype": "Sales Invoice",
            "company": data['company'],
            "customer": data['customer_name'],
            "items":[
                {    
                    "qty": 1,
                    "item_code": data['item_code'],
                    "item_name": "Headphones",
                    "rate": data['item_price']
                }
            ]
        })
        sales_invoice_doc.insert(ignore_permissions=True)
        
        # Update user roles
        user = frappe.get_doc("User", data.get("first_name"))
        if user:
            user.roles = data.get("roles", [])
            user.save()
            frappe.db.commit()
            return ("Documents created and user roles updated successfully.")
        else:
            return ("User not found.")
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), ("Error"))
        return ("Error occurred while creating documents and updating user roles. Please check logs.")


