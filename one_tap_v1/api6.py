import frappe

@frappe.whitelist(allow_guest=True)
def create_customer():
    data = frappe.request.json
    if not frappe.db.exists("Customer", {"email_id": data.get('email')}):         
        cus_doc = frappe.get_doc({
            "doctype": "Customer",
            "customer_name": data['customer_name'],
            "customer_type": "Company",
            "email_id": data['email']
            # "mobile_no": "454545545",
            # "email_address": "sws@gmail.com",
            # "mobile_number": "454545545"
        })
        cus_doc.insert(ignore_permissions=True)
        return cus_doc
    else:
        return "Email Already Exists"


@frappe.whitelist(allow_guest=True)
def generate_keys(user):
    # data = frappe.request.json
    # user = data['user']
    frappe.only_for("System Manager")
    user_details: User = frappe.get_doc("User", user)
    api_secret = frappe.generate_hash(length=15)
    # if api key is not set generate api key
    if not user_details.api_key:
        api_key = frappe.generate_hash(length=15)
        user_details.api_key = api_key
    user_details.api_secret = api_secret
    user_details.save()

    return {"api_secret": api_secret, "api_key": user_details.api_key}

def test_user(email):
    try:
        user = frappe.get_list("User", {"email": email})
        print("No Exception", user)
    except Exception as e:
        print("Exception", e)