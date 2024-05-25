import frappe
import json
@frappe.whitelist()
def ping1():
    return "pong"

@frappe.whitelist()
def get_details():
    doc = frappe.get_doc("Project", "PROJ-0006")
    doc = doc.as_dict()
    return doc["project_name"]
    


@frappe.whitelist()
def create_user():
    try:
        data = json.loads(frappe.request.data)
        user_data = frappe.get_doc({
            "doctype":"User",
            "username":data['Username'],
            "password":data['password'],
            "email":data['email'],
            "first_name":data.get('first_name'),
            "roles":[{"role":"customer"},
                    {"role":"Auditor"},
            ],
        })
        user_data.insert()
        return{}
        
    except Exception as e:
        return{}
my_dict ={"":"",}
print(my_dict)
print(my_dict.values)
print(my_dict.keys)
print(my_dict.items)


@frappe.whitelist()
def get_user():
    doctype ="User",
    field=["first_name","lastname","email","username"]
    data=frappe.get_all(doctype=doctype,fields=field)
    return data

@frappe.whitelist()
def get_user_a():
    doctype="User",
    filters={"emails":"testy@test.com"},
    fields =["first_name","last_name","user_name","password"]
    data = frappe.get_all(doctype,fields=fields,filters=filters)
    return data


@frappe.whitelist()
def update_user_details():
    try:
        new_data = json.loads(frappe.request.data)
        
        # Check if the email field is present in the request data
        if "email" not in new_data:
            return "Email address is required for updating user details."
        
        email = new_data["email"]
        
        # Check if the user exists
        if frappe.db.exists("User", email):
            user_doc = frappe.get_doc("User", email)
            
            # Update user details
            for key, value in new_data.items():
                user_doc.set(key, value)
                
            user_doc.save()
            
            return "User details updated successfully."
        else:
            return f"User with email '{email}' not found."
    except Exception as e:
        # Log the error
        frappe.log_error(f"Error updating user details: {str(e)}")
        return "An error occurred while updating user details. Please try again later."

@frappe.whitelist
def update_gmail():
    try:
        new_data=json.loads(frappe.request.data)
        if'email' not in new_data:
            print("email is not available not required")
        email = new_data['email']
        if frappe.db.exists("User",email):
            user_doc=frappe.get_doc('User',email)
            
            for k,v in new_data.items():
                user_doc.set(k,v)
                
            user_doc.save()
            return "user updates successfully"
        else:
            return f"user with email{email} not found"
        
    except Exception as e:
        frappe.log_error(f"error: {str(e)}")
        return "error is updating"
            
    
    

