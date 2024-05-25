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
                    cus_details.share_holders_details = []
                    for share_holder in v:
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