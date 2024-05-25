import frappe
import json

@frappe.whitelist()
def ping1():
    return "Good"

# @frappe.whitelist()

# @frappe.whitelist()
# def get_updated_price():
#     filter ={"zone_name":"IFZA"}
#     field  =["0visa_2year"]
#     data=frappe.get_list(doctype="OT Zone Master",filters=filter,fields=field)
#     return data

# @frappe.whitelist()
# def ping1():
#     task_dict = frappe.db.get_value('Task', 'TASK-2024-00447', ['subject', 'description'], as_dict=0)
#     frappe.get_list('')
#     return task_dict

# latest_entry = frappe.get_list("Project", limit=1, order_by="creation desc")
# if latest_entry:
#     project = frappe.get_doc("Project", latest_entry[0].name)
#     project_templates = project.project_templates 
#     for obj in project_templates:
#         project_template = frappe.get_doc("Project Template", {"name": obj.project_template})
#         tasks = project_template.tasks
#         for task in tasks:
#             new_task = frappe.get_doc({
#                 "doctype": "Task",
#                 "subject": task.subject,
#                 "project": project.name
#             }).insert()
#             frappe.db.commit()


# @frappe.whitelist()
# def get_visa_1year_field():
#     filters ={"zone_name":"IFZA"}   # [["zone_code", "=", "za"]]
#     fields = ["0visa_2year"]
#     data = frappe.get_list("OT Zone Master", filters=filters, fields=fields)
#     # return frappe.as_json(data)
#     return data

# @frappe.whitelist()
# def get_visa_year_field(zonecode,no_visas,no_years):
#     doctype="OT Zone Master"
#     filters={'zone_name':zonecode}
#     field="{}visa_{}year".format(no_visas,no_years)
#     data1=frappe.get_list(doctype,filters=filters,fields=[field]) 
#     return data1


# @frappe.whitelist()
# def update_visa_1year_price(new_price):
#     try:
#         # Get a list of document names that match the filters
#         documents = frappe.get_list("OT Zone Master", filters={"zone_code": "za"}, pluck="name")

#         # Update the value of the 0visa_1year field for each document
#         for doc_name in documents:
#             frappe.db.set_value("OT Zone Master", doc_name, "0visa_1year", new_price)

#         # Return success message
#         return ("Price updated successfully.")
#     except Exception as e:
#         # Return error message if any exception occurs
#         frappe.log_error(("Error occurred while updating price: {0}").format(str(e)))
#         return ("Failed to update price. Please try again later.")
    
# @frappe.whitelist()
# def update_item_price1(new_price):
#     doctype = "OT Zone Master"
#     filters = {'zone_name':'IFZA'}
#     fields ='0visa_2year'
#     doc=frappe.get_list(doctype=doctype,filters=filters,fields=fields)
#     for d in doc:
#         frappe.db.set_value('OT Zone Master',doc,fields,new_price)
#     return "ok"
    
# @frappe.whitelist()
# def update_visa_years_price(zone_code, num_visa, num_years,new_price):
#     try:
#         # Construct field names based on input num_visa and num_years
#         field_name = "{}visa_{}year".format(num_visa, num_years)
                
#         # Update the value of the constructed field for the specified zone_code
#         frappe.db.set_value("OT Zone Master", {"zone_code": zone_code}, field_name, new_price)  # Update with any desired value

#         # Return success message  
#         return ("Price updated successfully.")
#     except Exception as e:
#         # Return error message if any exception occurs
#         frappe.log_error(("Error occurred while updating price: {0}").format(str(e)))
#         return e
#         # return ("Failed to update price. Please try again later.")
        



    



# price_dict = {'Trade License-IFZA-0-1': 12900, 'Trade License-IFZA-1-1': 14900, 'Trade License-IFZA-2-1': 16900, 'Trade License-IFZA-3-1': 18900, 'Trade License-IFZA-4-1': 20900, 'Trade License-IFZA-0-2': 25800, 'Trade License-IFZA-1-2': 29800, 'Trade License-IFZA-2-2': 33800, 'Trade License-IFZA-3-2': 37800, 'Trade License-IFZA-4-2': 41800, 'Trade License-IFZA-0-3': 38700, 'Trade License-IFZA-1-3': 44700, 'Trade License-IFZA-2-3': 50700, 'Trade License-IFZA-3-3': 56700, 'Trade License-IFZA-4-3': 62700, 'Trade License-IFZA-0-5': 64500, 'Trade License-IFZA-1-5': 74500, 'Trade License-IFZA-2-5': 84500, 'Trade License-IFZA-3-5': 94500, 'Trade License-IFZA-4-5': 104500, 'Trade License-MEYDAN-0-1': 12500, 'Trade License-MEYDAN-1-1': 14350, 'Trade License-MEYDAN-3-1': 18050, 'Visa allocation-MEYDAN-1-0': 1850, 'Partner visa-MEYDAN-1-0': 4000, 'Employee visa-MEYDAN-1-0': 3500, 'Establishment Card-MEYDAN-0-1': 2000, 'Establishment Card-IFZA-0-1': 2000, 'Partner visa-IFZA-1-0': 4750, 'Employee visa-IFZA-1-0': 3750}
# @frappe.whitelist()
# def update_item_price():
#     # Parse the incoming JSON data
#     # data_dict = frappe.parse_json(frappe.reuqest.data)
    
#     # Fetch the item based on the provided criteria (Entity, Type, Visa, Year)
#     items_price = frappe.get_all("Item Price")
    
#     # Check if the item exists
#     for item in items_price:
#         if item:
#             # Modify Item name 
#             # Use that item name to get the price of the item
#             # update the price
#             item_price_doc = frappe.get_doc("Item Price", item.name)
#             item_name = item_price_doc.item_name
#             temp = item_name.split("-")
#             temp = temp[1:]
#             search_str = "-".join(temp)
#             # Update the price in the 'Item Price' doctype
#             item_price_doc.price_list_rate = price_dict.get(search_str, 0)
#             item_price_doc.save()
#             frappe.db.commit()
#     return "Updated Successfully !"
            

     
    



# # @frappe.whitelist()
# # def update_item_price():
# #     item_price = frappe.get_all("Item Price")
# #     return item_price



#     # doctype ="Item"
#     # item = json.loads(frappe.request.data)
#     # # no_of_visa = item['no_of_visa']
#     # fields = ["item_name","item_group"]
#     # data = frappe.get_all(doctype=doctype,fields=fields)
#     # # item_name = item['item_name'],
#     # # item_group = item['item_group'],
#     # # filters = {"item":"item_name"}
#     # item_list =frappe.get_doc(doctype="Item",fields=["item_name","item_group"])
#     # # return item_list
#     # response = []
#     # for obj in data:
#     #         item_name_parts = obj.get('item_name', '').split('-')
#     #         if item_name_parts:
#     #             activity_name = item_name_parts[0]
#     #             activity = frappe.get_doc('OT Business Activity New', {'activity_name': activity_name})
#     #             if activity:
#     #                 temp = {
#     #                     "item_code": obj.get('item_code', ''),
#     #                     "item_price": obj.get('price_list_rate', ''),
#     #                     "activity_group": activity.activity_group,
#     #                     "activity_price": activity.activity_price,
#     #                     "zone": activity.zone
#     #                 }
#     #                 response.append(temp)

#     #             return response
            
# # # In your Frappe application, define an API endpoint to handle the request
# # @frappe.whitelist
# # def add_template_tasks_to_project():
# #    user_data = json.loads(frappe.request.data)
# #         # Finding Customer project
# #    project_name = user_data['project_name']
# #         #  Project Templates
# #    project_templates = project_name.project_templates

# #     # Retrieve the Project document
# #    project = frappe.get_doc("Project", project_name)

# #     # Add tasks from each selected template to the project
# #    for template_name in project_templates:
# #         template = frappe.get_doc("Project Template", template_name)
# #         for task in template.tasks:
# #             project.append("tasks", {
# #                 "subject": task.subject,
# #                 # "description": task.description,
# #                 "status": "Open"
# #             })

# #     # Save the changes to the project
# #     project.save()

# #   return "Tasks added successfully to project."




# # @frappe.whitelist()
# # def add_template_tasks_to_project():
# #     # user_data = json.loads(frappe.request.data)
# #     # Finding Customer project
# #     # Retrieve the Project document
# #     project = frappe.get_doc({
# #         'doctype': 'Project',
# #         'project_name' : user_data['project_name'], 
# #         'company':'TECHBIRD(Demo)',
# #         'project_templates':user_data['project_templates']
        
        
# #         })
# #     # Project Templates
# #     project_templates = project.project_templates
# #     # Add tasks from each selected template to the project
# #     for template_name in project_templates:
# #         template = frappe.get_doc("Project Templates", template_name)
# #         for task in template.tasks:
# #             frappe.new_doc(
# #                 {
# #                 "doctype": "Task",
# #                 "subject": task.subject,
# #                 # "description": task.description,
# #                 "status": "Open",
# #                 "project": project_name
# #             }).insert()
# #     # Save the changes to the project
# #     return "Success"



# # ----------------------------------------------------------------------

    
# def create_task_using_project_template():
#     pass

# latest_entry = frappe.get_list("Project", limit=1, order_by="creation desc")
# if latest_entry:
#     project = frappe.get_doc("Project", latest_entry[0].name)
#     project_templates = project.project_templates 
#     for obj in project_templates:
#         project_template = frappe.get_doc("Project Template", {"name": obj.project_template})
#         tasks = project_template.tasks
#         for task in tasks:
#             new_task = frappe.get_doc({
#                 "doctype": "Task",
#                 "subject": task.subject,
#                 "project": project.name
#             }).insert()
#             frappe.db.commit()
            
            
            
# # # --------------------------------------------------------------------------------------------
# # @frappe.whitelist()
# # def update_prices():
# #         # Fetch activity groups with associated price changes
# #         activity_groups = frappe.get_all("Activity Group", filters={"status": "Active"}, fields=["name", "new_price"])
# #         return activity_groups
# #         for group in activity_groups:
# #             # Fetch items associated with the activity group
# #             items = frappe.get_all("Item", filters={"activity_group": group.name}, fields=["name", "price"])

# #             # Update prices based on the new price in the activity group
# #             for item in items:
# #                 frappe.db.set_value("Item", item.name, "price", group.new_price)

# #         frappe.db.commit()
# # #         frappe.msgprint("Prices updated successfully")




# # @frappe.whitelist()
# # def update_zone_master_price(zone_code): 
# #     # args = frappe.form_dict
# #     # zone_code = args.get("zone_code")
# #     search_pattern =  f"%{zone_code}%"   
# #     doctype = "OT Zone Master"
# #     # filters = {"zone_code": "za"}
# #     filters = [
# #         {"zone_code": ["like", search_pattern]},
# #     ]
# #     fieldname = "0visa_1year"

# #     new_doc=frappe.get_doc(doctype, filters[0]['zone_code'],fieldname)
# #     return new_doc
# #     # frappe.db.commit()
# #     # return "Price updated successfully"

# # @frappe.whitelist()
# # def doc_api():
# #     data = json.loads(frappe.request.data)
# #     zone_code = data['zonecode']
# #     filter2={"zone_code":"za"}
    
# #     search_pattern = f"%{zone_code}%"
# #     filter1={'zone_name' : 'IFZA'}
# #     filters=[{zone_code:["like",search_pattern]}]
# #     field="0visa_1year"
# #     doctype ='OT Zone Master'
# #     task1 = frappe.get_value(doctype,filters=filter2,fields=field)
# #     return task1

# # def update_item_price_on_activity_helper(data):
# #     activity_group_name = data['activity_group_name']
# #     activity_price = data['activity_price']

# #     # Determining Activity Price
# #     activity = frappe.get_doc(doctype=Doctype.OT_BUSINESS_ACTIVITY, filters={"business_activity_group_name": activity_group_name})
# #     if activity:
# #         business_zone = activity.business_zone
# #         activity_price = activity.activity_additional_price
# #         if business_zone:
# #             zone_doc = frappe.get_doc(doctype=Doctype.OT_ZONE_MASTER, filters={"zone_name": business_zone}, as_dict=True)
# #             return zone_doc["0visa_1year"]
# #             for year in range(1,6):
# #                 for visa in range(0,5):
# #                     key = f"{visa}visa_{year}year"
# #                     return zone_doc
# #                     # if item_zone:
# #                     #     temp = item_zone[0]
# #                     #     item_zone_price = temp[list(temp.keys())[0]]
# #                     #     item_zone_price = item_zone_price if item_zone_price else 0
                    
# #                     item_total_price = int(activity_price) + int(item_zone_price)
# #                     return vars(zone_doc)
# #                     return ans

# @frappe.whitelist()
# def get_visa_1year_field():
#     filters ={"zone_name":"IFZA"}   # [["zone_code", "=", "za"]]
#     fields = ["0visa_2year"]
#     data = frappe.get_list("OT Zone Master", filters=filters, fields=fields)
#     # return frappe.as_json(data)
#     return data

# @frappe.whitelist()
# def get_company():
#     data=frappe.get_list(doctype="DEMO_CUSTOMER",filters={"company": "demo_company"})
#     return data
