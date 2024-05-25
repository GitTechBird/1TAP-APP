import frappe
import requests
import json
import re
from .helper.otp_helper import send_email_helper

@frappe.whitelist()
def get_item():
    doctype ="Item"
    fields=["item_name","item_group","item_code"]
    item=frappe.get_all(doctype=doctype,fields=fields)
    # item=frappe.get_doc(doctype="Item","name":AE_RAKEZ_CompanySetup_General Trading-2-3)
   
    return item

@frappe.whitelist()
def create_task():
    Task=frappe.get_doc(
        {
          "doctype":"Task",
          "subject":"test"

          
        }
    )
    Task.project = Task.name
    Task.save()

    return ("Task created successfully.")


@frappe.whitelist()
def create_project_task():
    # Create the project
    project = frappe.get_doc({
        "doctype": "Project",
        "project_name": "1tap",
        "status": "Open"  # Set the status as needed
    })
    project.insert()

    # Create the task associated with the project
    task = frappe.get_doc({
        "doctype": "Task",
        "subject": "Test Task",
        "project": project.name,  # Link the task to the project
    
    })
    task.insert()

    return("Task created successfully.")


@frappe.whitelist()
def delete_item():
    try:
        # Use frappe.delete_doc with the document type ('Item') and document name ('ITEM-001')
        frappe.delete_doc("Item", "Vishal")
        return("Item deleted successfully")
    except frappe.DoesNotExistError:
        return("Document does not exist")
    except Exception as e:
        return(f"Error deleting document: {str(e)}")


@frappe.whitelist()
def get_task1():
    doctype="OT Customer Details"
    fields=["country_of_operation","franchise_or_branch","proposed_company_name_1","proposed_company_name_2","proposed_company_name_3","issued_company_name"]
    Task1=frappe.get_all(doctype=doctype,fields=fields)
    return Task1

@frappe.whitelist()
def get_task2():
    doctype="OT Customer Details"
    fields=["license_type","license_years","no_of_visa_eligibilty","license_zone","no_of_business_activities_eligible","business_activities_suggested"]
    Task2=frappe.get_all(doctype=doctype,fields=fields)
    return Task2
@frappe.whitelist()
def get_task_all():
    doc="OT Customer Details"
    fields=["share_holding_type","number_of_sharholders","proposed_share_capital","proposed_share_value","total_number_of_shares","share_capital_per_shareholder","general_manage_name","general_manager_authorized_signatory","consent_form"]
    Task_all=frappe.get_doc(doc, {"customer_name":"Amol Aghade"}, fields)
    return Task_all


@frappe.whitelist()
def get_customer():
    doc="Customer"
    fields=["customer_name","customer_type","customer_group","gender"]
    resp=[]
    try:
        # Fetch customer details
        customer_doc = frappe.get_doc(doc, {"email_id": "vishalaherhhhhh83@gmail.com"}, fields)
        resp.append(customer_doc)
    except frappe.DoesNotExistError:
        resp.append({"error": "Customer not found"})
    try:
        # Fetch user details
        user_doc = frappe.get_doc(doc, {"email_id": "vishalaher83@gmail.com"}, fields)
        resp.append(user_doc)
    except frappe.DoesNotExistError:
        resp.append({"error": "User not found"})
    return resp
    # exists = frappe.db.exists("User", {"email": "vishalaher83@gmail.com"})
    # if customer_doc and user_doc:  # Check if both documents exist
    #     customer_details = {
    #         "customer_name": customer_doc.customer_name,
    #         "customer_type": customer_doc.customer_type,
    #         "customer_group": customer_doc.customer_group,
    #         "gender": customer_doc.gender,
    #         "full_name": user_doc.full_name,
    #         "username": user_doc.username,
    #         "email": user_doc.email
    #     }

        # resp.append(customer_details)

    return User
    return exists
    return customer_details


@frappe.whitelist()
def update_comapny_details():
    try:
      data=json.loads(frappe.request.data)
      company_details=frappe.get_doc("Company_test", {"company_name": data['company_name']})
      company_details.update({
          "company_name":data['new_company_name'],
          "company_owner":data['company_owner'],
          "no_of_employee":data['no_of_employee'],
          "started_on":data['started_on']
      })
    #   company_details.company_name = data['new_company_name']
    #   exists = frappe.db.exists("Company_test", {"company_name":"Sunjukta ki Company"})
    #   return exists
    #   company_details.insert()
      company_details.employees=[]
      company_details.save()
      frappe.db.commit()
      return "company_details updated successfully"
    except frappe.DoesNotExistError:
        # frappe.log_error(f"Company '{data['company_name']}' does not exist")
        return "Company does not exist"

    
#     company_details.company_name = data.get("company_name")
#     company_details.get("child_table_field_name").clear()

#     # Add or update child table entries
#     for row in data["child_table"]:
#         child_row = company_details.append("child_table_field_name", {})
#         child_row.field1 = row["field1"]
#         child_row.field2 = row["field2"]
#         # Add other fields as needed

#     # Save the updated company document
#     company_details.save()

#     return "Company details updated successfully"


@frappe.whitelist()
def get_company_details():
    doctype="Company_test"
    fields=["company_name","company_owner","no_of_employee","started_on"]
    company_details=frappe.get_doc(doctype,{"company_name":"Sunjukta ki Company"},fields)
    return company_details

@frappe.whitelist()
def create_company_details():
    data = json.loads(frappe.request.data)
    create_company=frappe.get_doc({
        "doctype":"Company_test",
        "company_name":data['company_name'],
        "company_owner":data['company_owner'],
        "no_of_employee":data['no_of_employee'],
        "started_on":data['started_on']
    })
    create_company.insert()
    frappe.db.commit()



   
@frappe.whitelist()
def ping():
    return"Sanju"



@frappe.whitelist(allow_guest=True)
def send_login_email(email):
    subject = "Login Notification"
    body = "You have successfully logged in."
    recipient = email

    # Check if the recipient already exists in the Email Queue Recipient table
    if not frappe.db.exists("Email Queue Recipient", {"recipient": recipient}):
        # Insert the recipient into the Email Queue Recipient table
        email_queue_recipient = frappe.get_doc({
            "doctype": "Email Queue Recipient",
            "recipient": recipient
        })
        email_queue_recipient.insert()

    # Send email using Frappe's email functionality
    frappe.sendmail(recipients=[email], subject=subject, message=body)




# from frappe.core.doctype.communication.email import make

def send_email_after_login(login_manager):
    try:
        print("send_email_after_login", json.dumps(login_manager.info))
        print("send_email_after_user", json.dumps(login_manager.user))
        
        # user = login_manager.user
        # email = user.get("email")
        email = login_manager.user

        if email != "administrator" and email != "Guest" and is_valid_email(email):
            subject = "Login Notification"
            body = "You have successfully logged in."
            recipient = email
            
            # # Check if the email matches the pattern
            # if is_valid_email(email):
            #     print("Login email sent successfully to:", login_manager.user)
                
            #     # Check if the recipient already exists in the Email Queue Recipient table
            #     if not frappe.db.exists("Email Queue Recipient", {"recipient": recipient}):
            #         # Insert the recipient into the Email Queue Recipient table
            #         email_queue_recipient = frappe.get_doc({
            #             "doctype": "Email Queue Recipient",
            #             "recipient": recipient
            #         })
            #         email_queue_recipient.insert()

            #     # Send email using Frappe's email functionality
            #     frappe.sendmail(recipients=[email], subject=subject, message=body)
                
            #     return "Successfully sent mail"
            # else:
            #     return "Invalid email format"
            return send_email_helper(email, subject, body)
        else:
            # Email does not exist, raise an error or handle accordingly
            print("Error: User email not found. Unable to send login email.")
            return "Error: User email not found. Unable to send login email."
    except frappe.DoesNotExistError:
        return "Error: User does not exist"

def is_valid_email(email):
    # Regular expression pattern for validating email
    pattern = r'^[\w\.-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(pattern, email))

# @frappe.whitelist()
# def item_search_helper_new():
#     data = frappe.request.json
#     resp = []
#     for obj in data["request"]:
#         zone_code = obj['zone']
#         activity_type = obj['type']
#         zone = frappe.get_doc("OT Zone Master", {"zone_code": zone_code})
#         zone_code_pattern = f"%{zone_code}%"
#         activity_type_pattern = f"%{activity_type}%"
#         filters = [
#             {"item_name": ["like", zone_code_pattern]},
#             {"item_name": ["like", activity_type_pattern]},
#             {"has_variants": 0}
#         ]
        
#         items = frappe.get_all(doctype="Item", filters=filters, fields=["item_code"])
#         all_items = []
        
#         for item_obj in items:
#             item = frappe.get_doc("Item", {"item_code": item_obj['item_code']})
#             item_price = frappe.get_value(doctype="Item Price", filters={"item_code": item.item_code}, fieldname="price_list_rate")
#             temp = {
#                 "item_price": item_price if item_price else 0,
#                 "item_name": item.item_name,
#                 "item_code": item.item_code,
#                 "description": item.description,
#                 "business_zone": zone_code
#             }
#             for attr in item.attributes:
#                 temp[modify_key_name(attr.attribute)] = attr.attribute_value
#             all_items.append(temp)
        
#         resp.append({
#             "zone": obj['zone'],
#             "type": obj['type'],
#             "pros": zone.Pros,  # Accessing pros field from zone document
#             "cons": zone.Cons,  
#             "items": all_items
#         })
#     return resp


@frappe.whitelist()
def get_pros_cons_details():
    doctype="OT Zone Master"
    fields=["pros","cons"]
    pros_cons_details=frappe.get_all(doctype=doctype,fields=fields)
    return  pros_cons_details

@frappe.whitelist()
def get_customer_name(user_email):
    user_filters = {"user_email": user_email}
    customer_email = frappe.get_value(doctype="User Customer", filters=user_filters, fieldname="customer_email")
    # Finding Customer Name
    cus_filters = {"email_id": customer_email}
    customer_name = frappe.get_value(doctype="CUSTOMER", filters=cus_filters, fieldname="customer_name")
    return customer_name 

