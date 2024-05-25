#import frappe
import frappe
from datetime import datetime, timedelta

def checkB4Session(login_manager):
    print("checkB4Session", login_manager.user)
# =============================================================================================    
    
import frappe 
import logging
from datetime import datetime, timedelta
from one_tap_v1.helper.otp_helper import send_email_helper

# @frappe.whitelist(allow_guest=True)
def get_live_sessionn(login_manager):
    try:
        # Calculate the threshold time for considering sessions as live (e.g., 5 minutes ago)
        threshold_time = datetime.now() - timedelta(minutes=5)
        
        print("Threshold Time:", threshold_time)
        email=login_manager.user

        # Query live sessions for the specified user
        live_sessions = frappe.db.sql("""
            SELECT
                COUNT(*) as num_live_sessions
            FROM
                `tabSessions`
            WHERE
                `user` = (SELECT `name` FROM `tabUser` WHERE `email` = %s) 
                AND lastupdate > %s 
        """, (email, threshold_time), as_dict=True)
        
        print("Live Sessions:", live_sessions)

        # Extract the number of live sessions
        num_live_sessions = live_sessions[0].get('num_live_sessions', 0)
        
        print("Number of Live Sessions:", num_live_sessions)

        # Flag to track if email is sent
        email_sent = False

        # If the number of live sessions is more than 1, send an email
        if num_live_sessions > 1 and is_valid_email(email):
            email_sent = send_email_helper(email, "Maximum Sessions Exceeded", "Maximum login sessions exceeded for the user.")
            frappe.throw(_("Session limit exceeded"))
        
        print("Email Sent:", email_sent)

        # Return the number of live sessions and whether email was sent
        return {
            "email": email,
            "num_live_sessions": num_live_sessions,
            "email_sent": email_sent
        }
    except Exception as e:
        # Handle any exceptions that occur during the execution of the function
        # Log the error or perform any necessary actions
        print(f"Error in get_live_sessionn: {str(e)}")
        return {
            "error": str(e)
        }
def email_validation(email):
    if  email != "administrator" and email != "Guest" and is_valid_email(email):
        pattern = r'^[\w\.-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return bool(re.match(pattern, email))

# ==================================================================================
# =====================================================
import re
import json
from datetime import datetime, timedelta
import frappe
@frappe.whitelist()
def get_live_sessions2(email):
    try:
        threshold_time = datetime.now() - timedelta(minutes=5)
        print("Threshold Time:", threshold_time)
        # email = login_manager.user
        live_sessions = frappe.db.sql("""
            SELECT COUNT(*) as num_live_sessions
            FROM `tabSessions`
            WHERE `user` = (SELECT `name` FROM `tabUser` WHERE `email` = %s) 
            AND lastupdate > %s 
        """, (email, threshold_time), as_dict=True)

        print("Live Sessions:", live_sessions)

        num_live_sessions = live_sessions[0].get('num_live_sessions', 0)
        print("Number of Live Sessions:", num_live_sessions)

        email_sent = False

        if num_live_sessions > 1 and is_valid_email(email):
            email_sent = send_email_helper(email, "Maximum Sessions Exceeded", "Maximum login sessions exceeded for the user.")
            delete_sessions = frappe.db.sql("""
                DELETE FROM
                    `tabSessions`
                WHERE
                    `user` = (SELECT `name` FROM `tabUser` WHERE `email` = %s)
                    AND `lastupdate` = (
                        SELECT MAX(`lastupdate`)
                        FROM `tabSessions`
                        WHERE `user` = (SELECT `name` FROM `tabUser` WHERE `email` = %s)
                        AND `lastupdate` > %s
                    )
            """, (email, email, threshold_time))


            # frappe.throw(_("Session limit exceeded"))
        
        print("Email Sent:", email_sent)

        return {
            "email": email,
            "num_live_sessions": num_live_sessions,
            "email_sent": email_sent
        }
    except Exception as e:
        print(f"Error in get_live_sessions2: {str(e)}")
        return {
            "error": str(e)
        }


def is_valid_email(email):
    pattern = r'^[\w\.-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(pattern, email))
# ===========================================================================================================================

# # @frappe.whitelist()
# # def ping():
# #     return "pong"

# # # def search_items(item_group,visa_year_attribute,visa_number_attribute):
# # #     sql_querry =
# # #     """
# # #     SELECT DISTINCT I.NAME
    
# # #     """
    
# # @frappe.whitelist()
# # def get_frappe():
# #     doc = frappe.get_doc('Task','TASK-2024-00504')
# #     doc.Subject = 'Registration2'
# #     doc.save()
# #     return doc


# # @frappe.whitelist()
# # def create():
# #     doc = frappe.get_doc(
# #         {
# #             "doctype"  : "Task",
# #             "Subject" : "New task" ,
# #             "title":"new-title",
# #             "Project":"PROJ-0021"
            
            
        
# #         }
# #     )
# #     doc.save()
# #     return doc


# # @frappe.whitelist()
# # def create_pro():
# #    doc= frappe.get_doc( 'Project','PROJ-0037')
# #    return doc

# # @frappe.whitelist()
# # def create_pro1():
# #    doc= frappe.get_doc( doctype='Project',project_name= "Demo Flow Project 26")
# #    return doc
    
    
# # @frappe.whitelist()
# # def create_pro2():
# #     doc = frappe.get_doc(doctype='Project',project_name= 'Demo Flow Project 27')
# #     doc.insert()
    
    
# # @frappe.whitelist()
# # def create_task():
# #     data=frappe.request.json
# #     subject1 = data['subject2']
# #     description1 = data['description2']
# #     # Create a new Task document
# #     task = frappe.get_doc({
# #         "doctype": "Task",
# #         "subject": subject1,
# #         "description": description1,
# #         # Set other fields as needed
# #     })
    
# #     # Insert the Task document into the database
# #     task.insert()
    
# #     # Return the created Task document or any relevant information
# #     return {"message": "Task created successfully", "task": task.name}


# # @frappe.whitelist()
# # def last_doc():
# #     task1 = frappe.get_last_doc('Task')
# #     return task1

# # @frappe.whitelist()
# # def last():
# #     doc = frappe.get_doc()
# #     return doc

# # @frappe.whitelist()
# # def user_list():
# #     doc=frappe.get_list('User',pluck='name')
# #     return doc

# # @frappe.whitelist()
# # def open_task() :
# #     doc=frappe.get_list('Task',filters ={'status':'open'},fields=['subject','description'])
# #     return doc

# # @frappe.whitelist()
# # def open_task1():
# #     frappe.db.get_list('Task',filters = { 'data' : ['>','2019-09-08']})
# #     frappe.get_list('Task',filters = {'subject':['like','%test%']})
# #     frappe.get_list('Task',)
    
# # @frappe.whitelist()
# # def open_task2():
# #     task_dict = frappe.db.get_value('Task', 'TASK-2024-00512', ['subject', 'description'], as_dict=1)
# #     return task_dict

# #     #  "message": [--as_dict = 0
# #     #     "Registration",
# #     #     null
# #     # ]
    
# #     #     "message": {  --as_dict=1
# #     #     "subject": "Registration",
# #     #     "description": null
# #     # }
    
# # @frappe.whitelist()
# # def set_value():
# #     task=frappe.set_value('Task','TASK-2024-00517','subject','demotasked',notify=True)
# #     return task


# # @frappe.whitelist()
# # def update_task_description():
# #     data = frappe.request.json
# #     task_id = data['task_id']
# #     # Retrieve the Task document
# #     task = frappe.get_doc("Task", task_id)
    
# #     # Get the previous version of the Task document
# #     old_task = task.get_doc_before_save()
    
# #     # Check if any field has changed
# #     if old_task != task:
# #         # Fields have changed, update the task description
# #         # You can customize this part to include specific information about the changes
# #         description = "Task details have been updated:\n\n"
# #         for field in task.meta.get("fields"):
# #             if task.get(field.fieldname) != old_task.get(field.fieldname):
# #                 description += f"{field.label}: {old_task.get(field.fieldname)} --> {task.get(field.fieldname)}\n"
        
# #         task.description = description
# #         task.save()
# #         return {"message": "Task description updated successfully", "task_id": task_id}
# #     else:
# #         return {"message": "No changes detected. Task description remains the same.", "task_id": task_id}


# # def item_search_old(args):
# #     activity_group = args.get("activity_group")
# #     search_pattern = f"%{activity_group}%"
# #     doctype = "OT Business Activity"
# #     or_filters = [
# #         {"bussiness_activity_group_name":["like",search_pattern]},
# #         {"bussiness_activity_name":["like",search_pattern]},
# #         {"bisiness_activity_description":["like",search_pattern]}
# #         ]
# #     activity_group =frappe.get_all(doctype = 'OT BUSINESS ACTIVITY',or_filters=or_filters,fields=["item_generated_code","business_zone"] )
# #     item_templates = []
# #     for activity in activity_group:
# #         if activity.item_generated_code:
# #             item_templates.append(activity.item_generated_code)
            
# #     all_items = []
# #     for template in item_templates:
# #         items = frappe.get_list(doctype ='Item',filters = {"variant_of":template}, fields =["name"])
# #         # if items:
# #         #     return items
        
# #     for obj in items:
# #         item  = frappe.get_all('Item','obj.name')
# #         item_value = frappe.get_value('Item Price',{"item_code":"item.item_code"},fieldname="price_list_rate")
        
    
    
        
# # @frappe.whitelist()
# # def item_search():
# #     args = frappe.form_dict
# #     return item_search_old(args)


# # @frappe.whitelist()
# # def get_customer():
# #     data = frappe.request.json
# #     resp = {}
    
# #     filters={'email_id'  : data['email']}
# #     cus_exists = frappe.db.exists("Customer", filters)
# #     if cus_exists:
# #         cust = frappe.get_doc('Customer',filters)
# #         resp["customer"] = cust
# #     else:
# #         resp['customer'] = {}

# #     user_exists = frappe.db.exists("User", filters) 
# #     if user_exists: 
# #         user = frappe.get_doc('User',{'email': data['email']})
# #         resp["user"] = user 
# #     else:
# #         resp['user'] = {}
# #     return resp

# # # @frappe.whitelist()
# # # def get_customer():
# # #     resp = { }
# # #     data = frappe.request.json
# # #     fields = {'email_id': data['email_id']}
# # #     frappe.get_value()
# # #     cus_exist=frappe.db.exist("Customer",filters)
# # #     if cus_exist:
# # #         cust = frappe.get_doc()
# # #         resp['cust']=cust
# # #     else:
# # #         resp['cust'] = {}
    
# # #     user_exists = frappe.db.exists('User',filters)
# # #     if user_exists:
# # #         user = frappe.get_doc()
# # #         resp['user'] = user
# # #     else:
# # #         resp['user']={} 
        
# # #     frappe.get_value()
    
# # # create api
# # @frappe.whitelist()
# # def company_test():
# #     try:
# #         data = frappe.request.json
# #         company_doc = frappe.get_doc(
# #             {
# #             "doctype": "Company_test",
# #             "started_on": data.get("started_on"),
# #             "no_of_employee": data.get("no_of_employee"),
# #             "company_owner": data.get("company_owner"),
# #             "company_name": data.get("company_name")
# #             }
# #         )
        
# #         for employee_data in data.get("employees", []):
# #             employee = company_doc.append("employees", {})
# #             employee.domain = employee_data.get("domain")
# #             employee.location = employee_data.get("location")
# #             employee.dob = employee_data.get("dob")
# #             employee.first_name = employee_data.get("first_name")
# #             employee.last_name = employee_data.get("last_name")

# #         # Save the company document
# #         company_doc.insert(ignore_permissions=True)
# #         return {"success": True, "message": ("Company created successfully")}
# #     except Exception as e:
# #         return {"success": False, "message": str(e)}
    
# # @frappe.whitelist()
# # def get_company_test(company_name):
# #     try:
# #         # data =frappe.request.json
# #         # company_name = data['company_name']
# #         filters = {'company_name' :company_name}
# #         company_doc = frappe.get_doc('Company_test',filters)
# #         if company_name:
# #             return{"sucess":True,"data":company_doc.as_dict()}
# #         else:
# #             return{"sucess":False,"massage":("company not found")}
# #     except Exception as e:
# #         return{"success":False,"message":str(e)}
    
    
    
    
# # @frappe.whitelist
# # def get_company(company_name):
# #     try:
# #         filters = {'company_name' : company_name}
# #         doc = frappe.get_doc('company_test',filters)
# #         if company_name:
# #             return{"success":True,"data":doc.as_dict()}
# #         else:
# #             return{"success":False,"masaage":"company not found"}
        
# #     except Exception as e:
# #         return{"success":False, 'massage':str(e)}
    
    
# # @frappe.whitelist()
# # def create_company1():
# #     try:
# #         data = frappe.request.json
# #         company_doc = frappe.get_doc(
# #             {
# #                 "doctype":"company_test",
# #                 "started_on":data.get('started_on'),
# #                 "no_of_employee" : data.get('no_of_employee'),
# #                 "company_owner"  :data.get('company_owner'),
# #                 "company_name"   : data.get('company_name')
# #             }
# #         )
        
# #         for emp_data in data.get('employees',[]):
# #             employee=company_doc.append("employees",{})
# #             employee.domain = emp_data.get('domain')
# #             employee.location=emp_data.get('location')
# #             employee.dob = emp_data.get("dob")
# #             employee.first_name = emp_data.get("first_name")
# #             employee.last_name = emp_data.get("last_name")
            
# #         company_doc.insert()
# #         return{"sucess":True,"message":("company created successfully")}
# #     except Exception as e :
# #         return{}
    
    
# # @frappe.whitelist()
# # def add_task_project(project_name):
# #     task_doc = frappe.get_doc('task',filters={'project':project_name},fields=["name", "subject", "status"],order_by="subject")
# #     resp = {}
# #     idx =1
# #     for task in task:
# #         idx = 1
# #         return resp
        
        
# # @frappe.whitelist
# # def get_project_task(project_name):
# #     tasks=frappe.get_all('Task',filters={'project': project_name},fields=["name", "subject", "status"],order_by= "subject")
# #     resp = {}
# #     idx =1
# #     for task in tasks:
# #         resp[idx] = {
# #             "task_name": task.name,
# #             "subject": task.subject,
# #             "status": task.status
# #         }
# #         idx +=1
# #     return resp


# # @frappe.whitelist()
# # def update_task_helper():
# #     task = frappe.get_doc()

@frappe.whitelist(allow_guest=True)
def get_user_cache_keys():
    # all_cache_entries = {}
    # # Iterate over all keys in the cache
    return frappe.cache.keys()
    # for key in frappe.cache.keys():
    #     # Retrieve the value for each key
    #     value = frappe.cache.get(key)
    #     # Add the key-value pair to the dictionary
    #     all_cache_entries[key] = value
    # return all_cache_entries


    # keys_for_user = []
    # # Iterate over all keys in the cache
    # for key in frappe.cache.keys():
    #     # Check if the key corresponds to the specific user
    #     if key.endswith("_usr"):
    #         cached_user = frappe.cache.get(key)
    #         if cached_user == user:
    #             # Extract the tmp_id from the key and add it to the list
    #             tmp_id = key.rsplit("_", 1)[0]
    #             keys_for_user.append(tmp_id)
    # return keys_for_user
    
    user = "hitesh.sahu@techbirdit.in"  # Provide the specific user
    user_keys = []

    # Iterate over all keys in the cache
    for key in frappe.cache.keys():
        # Convert bytes key to string
        key_str = key.decode('utf-8') if isinstance(key, bytes) else key

        # Check if the key corresponds to the specific user
        if key_str.endswith("_usr"):
            cached_user = frappe.cache.get(key_str)
            if cached_user == user:
                # Extract the tmp_id from the key and add it to the list
                tmp_id = key_str.rsplit("_", 1)[0]
                user_keys.append(tmp_id)

    return user_keys

# prefix = 'b9cbfd38'
def find_keys_with_prefix(prefix):
    matching_entries = {}
    # Iterate over all keys in the cache
    for key in frappe.cache.keys():
        # Convert bytes key to string if needed
        key_str = key.decode('utf-8') if isinstance(key, bytes) else key
        # Check if the key starts with the specified prefix
        if key_str.startswith(prefix):
            # Retrieve the value for the key
            value = frappe.cache.get(key_str)
            # Add the key-value pair to the dictionary
            matching_entries[key_str] = value.decode()
    return matching_entries

value = 'hitesh.sahu@techbirdit.in'
def find_entries_with_value():
    matching_entries = {}
    try:
        # Iterate over all keys in the cache
        for key in frappe.cache.keys():
            # Convert bytes key to string if needed
            key_str = key.decode('utf-8') if isinstance(key, bytes) else key
            try:
                # Retrieve the value for the key
                cached_value = frappe.cache.get(key_str)
                cached_value = cached_value.decode()
                # print(cached_value, type(cached_value))
                # return
                # Check if the value matches the specified value
                if cached_value == value:
                    # Add the key-value pair to the dictionary
                    matching_entries[key_str] = cached_value
            # except redis.exceptions.ResponseError as e:
            except Exception as e:
                # Handle ResponseError (e.g., log the error)
                print(f"Ignoring key due to ResponseError: {key_str} - {e}")
    except Exception as ex:
        # Handle any other exceptions
        print(f"Error occurred while fetching cache entries: {ex}")
    return matching_entries


def find_keys_with_prefix_new(email_prefix):
    matching_entries = {}
    # Iterate over all keys in the cache
    for key in frappe.cache.keys():
        # Convert bytes key to string if needed
        key_str = key.decode('utf-8') if isinstance(key, bytes) else key
        # Retrieve the value for the key
        value = frappe.cache.get(key_str)
        # Convert value to string if it's bytes
        value_str = value.decode('utf-8') if isinstance(value, bytes) else value
        # Check if the email prefix is present in the value
        if email_prefix in value_str:
            matching_entries[key_str] = value_str
    return matching_entries


# def find_keys_ending_with(suffix):
#     matching_keys = []
#     # Iterate over all keys in the cache
#     for key in frappe.cache.keys():
#         # Convert bytes key to string if needed
#         key_str = key.decode('utf-8') if isinstance(key, bytes) else key
#         # Check if the key ends with the specified suffix
#         if key_str.endswith(suffix):
#             matching_keys.append(key_str)
#     return matching_keys


def find_keys_ending_with(email):
    suffix = '_usr'
    matching_keys = []
    # Iterate over all keys in the cache
    for key in frappe.cache.keys():
        # Convert bytes key to string if needed
        key_str = key.decode('utf-8') if isinstance(key, bytes) else key
        # Check if the key ends with the specified suffix
        if key_str.endswith(suffix):
            # Retrieve the value for the key
            value = frappe.cache.get(key_str)
            # Convert value to string if it's bytes
            value_str = value.decode('utf-8') if isinstance(value, bytes) else value
            # Check if the value matches the email
            if value_str == email:
                matching_keys.append(key_str)
    for key in matching_keys:
        key = key[:-4]
        for suffix in ['_usr', '_token','_otp_secret']:
            tkey = key+suffix
            frappe.cache.delete(tkey)
    return matching_keys