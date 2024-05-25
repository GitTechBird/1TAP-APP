import frappe
from .doctype import Doctype

def fetch_customer_details_helper(customer_id):
    customer_details_docs = frappe.get_all(doctype=Doctype.OT_CUSTOMER_DETAILS, filters={"customer_id": customer_id}, fields=["name", "user_email", "customer_id", "project_id","service_type"])
    return customer_details_docs
    # for customer_details_doc in customer_details_docs:
    #     customer_details = frappe.get_doc(Doctype.OT_CUSTOMER_DETAILS, customer_details_doc['name'])
    #     resp.append(customer_details.as_dict(fields))
    # # customer_detail_name = frappe.get_value(doctype=Doctype.OT_CUSTOMER_DETAILS, filters={"customer_id": customer_id}, pluck='name')
    # # customer_details = frappe.get_doc(Doctype.OT_CUSTOMER_DETAILS, customer_detail_name) 
    # # if customer_details:
    # #     customer_details = customer_details[
    # # else:
    # # if not customer_details:
    # #     customer_details = {}
    # # return customer_details
    # return resp

def fetch_customer_transaction_details_helper(customer_detail_id):
    return frappe.get_doc(Doctype.OT_CUSTOMER_DETAILS, customer_detail_id).as_dict(["*"])
    # return {}

def update_customer_details_helper(data):
    try:
        # Checking if the relevant information exists for the given customer
        if not frappe.get_all(Doctype.OT_CUSTOMER_DETAILS, filters={"name": data.get('customer_detail_id', None)}):
            cus_detail_doc = frappe.get_doc({
                "doctype": Doctype.OT_CUSTOMER_DETAILS
            })
            cus_detail_doc.insert()
            # frappe.db.commit()
            data['customer_detail_id'] = cus_detail_doc.name
        # Getting Customer_details from Doctype
        cus_details = frappe.get_doc(Doctype.OT_CUSTOMER_DETAILS, data['customer_detail_id'])
        # Update Customer Details
        for k, v in data.items():
            if k in ["customer_detail_id","business_activities_suggested", "share_holders_details"]:
                if k == "share_holders_details":
                    customer_details = cus_details.share_holders_details
                    cus_details.share_holders_details = []
                    share_holders_temp = []
                    for share_holder in v:
                        for cus_obj in customer_details:
                            if cus_obj.name == share_holder.get("share_holder_id"):
                                cus_obj.update(share_holder)
                                share_holders_temp.append(share_holder)
                            cus_details.append("share_holders_details", cus_obj)
                        if share_holder not in share_holders_temp:
                            cus_details.append("share_holders_details", share_holder)
                elif k == "business_activities_suggested":
                    cus_details.business_activities_suggested = []
                    for activity in v:
                        cus_details.append("business_activities_suggested", {"business_activity_name": activity})
            else:
                cus_details.set(k, v)
            cus_details.save(ignore_permissions=True)
        frappe.db.commit()
        return "Customer Details Updated"
    except Exception as e:
        return e