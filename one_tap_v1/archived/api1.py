import json
import frappe

@frappe.whitelist()
def testAPI():
    return 0



@frappe.whitelist()
def create_user():
   try:
    data = json.loads(frappe.request.data)
    user_data = frappe.get_doc({
            "doctype": "User",
            "username": data['username'],
            "password": data['password'],
            "email": data['email'],
            "first_name": data.get('first_name'),
            "roles": [
        {"role": "Customer"},
        {"role": "Auditor"},
        # Add more roles as needed
    ],
        })
    user_data.insert()
    return {"status": "success", "message": f"User '{data.get('username')}' created successfully!"}
   except Exception as e:
        return {"status": "error", "message": f"Error creating user: {str(e)}"}
#    frappe.db.commit()
   
@frappe.whitelist()
def get_user_A(): 
    doctype = "User"
    fields = ["first_name","last_name","email","username"]
    data = frappe.get_all(doctype,fields=fields)
    # without filters
    return data()
   
@frappe.whitelist()
def get_user():
    doctype = "User"
    filters = {"email":"test@test.com"}
    fields = ["first_name","last_name","email","username"]
    data = frappe.get_all(doctype,fields=fields,filters=filters)
    return data
   
   
@frappe.whitelist()
def update_user_details():
    new_data = json.loads(frappe.request.data)
    user_doc = frappe.get_doc("User",new_data["email"])
    for k,A in new_data.items():
      user_doc.set(k,A)
    user_doc.save()
    # for understandings
#     my_dict = {
#     "first_name" :"sanju",
#     "last_name" :"Barik",
#     "email":"san@gmail.com"
# }
# print(my_dict)
# for key in my_dict.keys():
    # print(key)
# for items in my_dict.items():
    # print(items)
# for values in my_dict.values():
    # print(values)
# for key,values in my_dict.items():
#     # print(items)
#     print(f"{key}:{values}")
    return user_doc
   
@frappe.whitelist()
def item_searching():
    # Get all item price documents
    doctype ="Item Price"
    fields = ["item_code","item_name","price_list_rate"]
    data = frappe.get_all(doctype=doctype,fields=fields, filters={'uom': 'Year'})
    response=[]
    for obj in data:
        item_name_parts = obj.get('item_name', '').split('-')
        if item_name_parts:
                activity_name = item_name_parts[0]
                activity = frappe.get_doc('OT Business Activity', {'activity_name': activity_name})
                if activity:
                    temp = {
                        "item_code": obj.get('item_code', ''),
                        "item_price": obj.get('price_list_rate', ''),
                        "activity_group": activity.activity_group,
                        "activity_price": activity.activity_price,
                        "zone": activity.business_zone
                    }
                    response.append(temp)
    return response


    # Loop through the item price documents and get the associated activities and form the response.
# item code,item price,activity group,zone,visa,activity price
# logic-

data = """ 
first,search in activity doctype with activity name parameter and identify all activites
once all the activites names are identify search all the related items of the activites with filtes of other parameters


"""
@frappe.whitelist()
def get_item_price():
   item_price = frappe.get_all("Item Price")
   return item_price


@frappe.whitelist()
def get_item():
    item = frappe.get_all("Item")
    return item

@frappe.whitelist()
def update_item_price():
    try:
        # Fetch all Item Prices
        items_price = frappe.get_all("Item Price", {"uom": "Year"})
    
        # Iterate over each item price
        for item in items_price:
            # Fetch the item price document
            item_price_doc = frappe.get_doc("Item Price", item.name)
            
            # Extract the item name and split it
            item_name = item_price_doc.item_name
            temp = item_name.split("-")
            
            # Remove the first part of the item name
            temp = temp[2:3]
        
            # search_str = "-".join(temp)
            # search.append(search_str)
        
            # Update the price using a dictionary (price_dict)
            # Define your price dictionary here
            # price_dict = {'Trade License-MEYDAN-2-2':2345,'Trade License-IFZA-0-1':12345,'Trade License-IFZA-0-1': 12900, 'Trade License-IFZA-1-1': 14900, 'Trade License-IFZA-2-1': 16900, 'Trade License-IFZA-3-1': 18900, 'Trade License-IFZA-4-1': 20900, 'Trade License-IFZA-0-2': 25800, 'Trade License-IFZA-1-2': 29800, 'Trade License-IFZA-2-2': 33800, 'Trade License-IFZA-3-2': 37800, 'Trade License-IFZA-4-2': 41800, 'Trade License-IFZA-0-3': 38700, 'Trade License-IFZA-1-3': 44700, 'Trade License-IFZA-2-3': 50700, 'Trade License-IFZA-3-3': 56700, 'Trade License-IFZA-4-3': 62700, 'Trade License-IFZA-0-5': 64500, 'Trade License-IFZA-1-5': 74500, 'Trade License-IFZA-2-5': 84500, 'Trade License-IFZA-3-5': 94500, 'Trade License-IFZA-4-5': 104500, 'Trade License-MEYDAN-0-1': 12500, 'Trade License-MEYDAN-1-1': 14350, 'Trade License-MEYDAN-3-1': 18050, 'Visa allocation-MEYDAN-1-0': 1850, 'Partner visa-MEYDAN-1-0': 4000, 'Employee visa-MEYDAN-1-0': 3500, 'Establishment Card-MEYDAN-0-1': 2000, 'Establishment Card-IFZA-0-1': 2000, 'Partner visa-IFZA-1-0': 4750, 'Employee visa-IFZA-1-0': 3750}

            # new_price = price_dict.get(search_str, 0)
            # Update the price in the 'Item Price' doctype
            # item_price_doc.price_list_rate = new_price
            item_price_doc.save()

        frappe.db.commit()
        return "Updated Successfully !"

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), ("Update Item Price Failed"))
        return str(e)
    

@frappe.whitelist()
def create_item():
    data = json.loads(frappe.request.data)
    user_data = frappe.get_doc({
            "doctype": "Item",
            "item_name": data['item_name'],
            "item_group": data['item_group'],
            "stock_uom": data['stock_uom'],
           "item_code":data['item_code']
        # Add more roles as needed
    
        })
    user_data.insert()


@frappe.whitelist()
def get_activity_master():
    fields =["business_activity_name","business_activity_group_name", "business_activity_description","item_generated_code"]
    data = frappe.get_all(doctype="OT Business Activity",fields=fields)
    return data

@frappe.whitelist()
def get_activity_item_group():
    args = frappe.form_dict
    activity_group = args.get("activity_group")
    search_pattern =  f"%{activity_group}%" 
    doctype = "OT Business Activity"
    # or_filters = [
    #   {"business_activity_group_name": ["like", search_pattern]},
    #   {"business_activity_name": ["like", search_pattern]},
    #   {"business_activity_description":["like",search_pattern]},
    # ]
    filters = [
      {"business_activity_group_name": ["like", search_pattern]},
    ]
    activities = frappe.get_all(doctype=doctype,filters=filters, fields=["name","license_type","business_zone","business_activity_name","business_activity_group_name"])
    # return activities
    all_items = []
    # for activity in activities:
    items = frappe.get_list(doctype="Item",filters={"item_group": activity_group, "has_variants": 0}, fields= ["name"])
    # return items
    for obj in items:
            item = frappe.get_doc("Item", obj.name)
            item_price= frappe.get_value(doctype="Item Price", filters={"item_code":item.item_code}, fieldname="price_list_rate")
            # return item_price
            temp = {    
                    "item_price":item_price,
                    "item_name": item.item_name,
                    "item_code": item.item_code,
                    "description":item.description,
                    "business_zone": activities[0].business_zone,
                    "license_type":activities[0].license_type
                }
            for attr in item.attributes:
                temp[modify_key_name(attr.attribute)] = attr.attribute_value
            all_items.append(temp)
    return all_items

def modify_key_name(key):
    key = key.lower()
    key = "_".join(key.split(" "))
    return key

@frappe.whitelist()
def get_item_price():
    fields = ["price_list_rate"]
    doctype = "Item Price"
    item_price = frappe.get_all(doctype=doctype,fields=fields)
    return item_price


@frappe.whitelist()
def business_zone():
    fields = ["business_zone"]
    doctype ="OT Business Activity"
    business_zone = frappe.get_all(doctype=doctype,fields=fields)
    return business_zone



@frappe.whitelist()
def get_zone_master_price():
    all = []
    for visa in range(1,5):
        for year in range(1,5):
            zone_name = "twofour54"
            filters = {"business_activity_name": "Testing"}
            fieldname = "activity_additional_price"
            activity= frappe.get_list(doctype="OT Business Activity", filters=filters,fields=fieldname)
            activity[0].activity_additional_price
            activity_price = int(activity[0].activity_additional_price) if activity else 0
            
            # Getting the price from the OT Zone Master
            filters = {"zone_code": zone_name}
            fieldname = f"{visa}visa_{year}year"
            item_zone = frappe.get_list(doctype="OT Zone Master", filters=filters, fields=[fieldname])
            # return item_zone
            item_zone_price = 0
            if item_zone:
                temp = item_zone[0]
                item_zone_price = temp[list(temp.keys())[0]]
            item_total_price = int(activity_price) + int(item_zone_price)
            all.append([activity_price, item_zone_price, item_total_price])
    return all
    # fields =["0visa_1year"]
    # doctype = "OT Zone Master"
    # filters={"zone_code":"SRTIP"}
    # zone_master_price = frappe.get_value(doctype=doctype,filters=filters,fieldname=fields[0])
    # # return zone_master_price
    # activity_item_price = frappe.get_value(doctype="OT Business Activity",filters={"business_activity_code":"9312.91525"},fieldname=["activity_additional_price"])
    # total_price = int(activity_item_price) + int(zone_master_price)
    # return total_price


# @frappe.whitelist()
# def item_ser():
#     doctype="Item"
#     fields=["item_code","item_group","item_name","description"]
#     # filters ={"item_code":""}
#     item_searching =frappe.get_all(doctype=doctype,fields=fields)
#     return item_searching
#     response=[]
#     for obj in item_searching:
#             item_price= frappe.get_value(doctype="Item Price", filters={"item_code":item.item_code}, fieldname="price_list_rate")
#             temp = {    
#                     "item_price":item_price,
#                     "item_name": item_searching.item_name,
#                     "item_code": item_searching.item_code,
#                     "description":item_searching.description,
#                 }
#             response.append(temp)
#     return response


@frappe.whitelist()
def item_ser():
    doctype = "Item"
    fields = ["item_code", "item_group", "item_name", "description"]
    item_searching = frappe.get_all(doctype=doctype, fields=fields)
    
    response = []
    for item in item_searching:
        item_price = frappe.get_value(doctype="Item Price", filters={"item_code": item.item_code}, fieldname="price_list_rate")
        temp = {    
            "item_price": item_price,
            "item_name": item.item_name,
            "item_code": item.item_code,
            "description": item.description,
            
        }
        response.append(temp)
    
    return response 
# for activities in activity:
#     activity = frappe.get_all(doctype=
#    "OT Business Activity",fields=["business_activity_code","business_activity_name","business_activity_group_name","business_zone"])
        


@frappe.whitelist()
def ping():
    return 'pong'

@frappe.whitelist()
def delete_items(activity_group):
        items = frappe.get_list(doctype="Item", filters={"item_group": activity_group},fields=["name"])
        # return items
        if items:
            # Delete each item
            for item in items:
                frappe.delete_doc("Item", item.name)
            frappe.db.commit()

            return f"All items belonging to activity group '{activity_group}' have been deleted successfully"

@frappe.whitelist()
def update_zone_master_price():
     data = json.loads(frappe.request.data)
     zone_name = data['zone_name']
     fieldname = "0visa_1year"
     visa_number = fieldname[0]
     visa_year = fieldname[6]
     data = json.loads(frappe.request.data)
     search_pattern =  f"%{data['zone_code']}%"
     doctype = "Item"
     activities = frappe.get_list(doctype="OT Business Activity", filters={"business_zone": zone_name}, pluck="business_activity_group_name")

     sql_query = """
        SELECT DISTINCT i.name, i.item_code
        FROM `tabItem` i
        INNER JOIN `tabItem Variant Attribute` a1 ON i.name = a1.parent
        INNER JOIN `tabItem Variant Attribute` a2 ON i.name = a2.parent
        WHERE i.item_name like %s
        AND (a1.attribute = 'OT Visa Number attributes' AND a1.attribute_value = %s)
        AND (a2.attribute = 'OT Visa Years attributes' AND a2.attribute_value = %s)
    """

    # Pass values using parameters in the sql() function
     results = frappe.db.sql(sql_query, ( visa_number,search_pattern,visa_year), as_dict=True)
     return results
     filters = [
    {"zone_code": ["like", search_pattern]},
    ]
     fieldname = "0visa_1year"
     for item in results:
        # frappe.set_value(doctype, filters[0]['zone_code'],fieldname)
        frappe.set_value(doctype, filters[0]['zone_code'], fieldname)
     frappe.db.commit()
     return "Price updated successfully"




@frappe.whitelist()
def update_zone_master_price_A():
    data = json.loads(frappe.request.data)
    # search_pattern =  f"%{data['zone_code']}%"
    zone_name = data['zone_name']
    fieldname = data['fieldname']
    updated_zone_field_price = data['updated_zone_field_price']
    visa_number = fieldname[0]
    visa_year = fieldname[6]
    
    # Determining Activity Price
    activities = frappe.get_all(doctype="OT Business Activity", filters={"business_zone": zone_name}, fields=["business_activity_group_name", "activity_additional_price"])
    all_items = []
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
        # return "hello"
        for item in items:
            new_price = float(acitivty.activity_additional_price) + float(updated_zone_field_price)
            item_price_doc = frappe.get_doc("Item Price", {"item_code": item.item_code})
            frappe.db.set_value("Item Price", item_price_doc.name, "price_list_rate", new_price)


@frappe.whitelist()
def item_price_details():
    doctype="Item Price"
    filters={"uom":"nos"}
    fields=["price_list_rate","item_code","item_name"]
    data=frappe.get_all(doctype=doctype,fields=fields,filters=filters)
    return data

@frappe.whitelist()
def item_list_all():
    doctype="Item"
    fields=["item_name","stock_uom","item_group","variant_based_on"]
    data=frappe.get_all(doctype=doctype,fields=fields)
    return data

@frappe.whitelist()
def item_activity(activity_group):
    # return activity_group
    doctype ="Item"
    fields=["item_name","stock_uom","item_group","description","item_code","item_group"]
    data=frappe.get_all(doctype=doctype,fields=fields)
    # return data
    response=[]
    for item in data:
        activities=frappe.get_all(doctype="OT Business Activity",filters={"item_generated_code":item.item_code},fields=["business_activity_name","activity_additional_price","business_activity_group_name","business_zone"])
        # return activities
        for activity in activities:
            temp={
            "item_name": item.item_name,
            "item_group": item.item_group,
            # "price_list_rate": item.price_list_rate,
            "item_code": item.item_code,
            "description": item.description,
            "business_activity_name":activity.business_activity_name,
            "activity_additional_price":activity.activity_additional_price,
            "business_activity_group_name":activity.business_activity_group_name,
            "business_zone":activity.business_zone,
             }
    
        response.append(temp)
    return response 
    
    # return data
    

@frappe.whitelist()
def is_customer(email):
    exists = frappe.db.exists('Customer', {'email_id':email})
    if exists:
        return exists
    else:
        None    

@frappe.whitelist()
def customer_details(customer_name):
    doctype="Customer"
    data = frappe.get_doc(doctype, customer_name)
    # return data
    return {
        "portal_users": data.portal_users,
        "name": data.name,
        "email_id": data.email_id
    }

@frappe.whitelist()
def customer_details_new(email):
    customer_name = is_customer(email)
    if customer_name:
        return customer_details(customer_name)
    else:
        return "Does not exists"