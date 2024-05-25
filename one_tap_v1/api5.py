import frappe
from frappe import _
import requests
import json
import re
# from .helper.otp_helper import send_email_helper
import logging
from datetime import datetime, timedelta
from frappe.utils.background_jobs import enqueue



@frappe.whitelist(allow_guest=True)
def handle_after_login(email):
    try:
        
        if validate_email(email):
            return validate_session(email)
        else:
            return "Error: User email not found. Unable to send login email."
    except frappe.DoesNotExistError:
        return "Error: User does not exist"


def is_valid_email(email):
    # Regular expression pattern for validating email
    pattern = r'^[\w\.-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(pattern, email))

def validate_email(email):
    return email != "Administrator" and email != "Guest" and is_valid_email(email)

def send_email_after_login(email):
    try:
        subject = "Login Notification"
        body = "You have successfully logged in."
        # return send_email_helper(email,"Welcome template") 
        return send_welcome_email(email,"Welcome template2")
        return "email sent"
    except frappe.DoesNotExistError:
        return "Error: User does not exist"

def validate_session(email):
    try:
        threshold_time = datetime.now() - timedelta(minutes=5)
        live_sessions = frappe.db.sql("""
            SELECT COUNT(*) as num_live_sessions
            FROM `tabSessions`
            WHERE `user` = (SELECT `name` FROM `tabUser` WHERE `email` = %s) 
            AND lastupdate > %s 
        """, (email, threshold_time), as_dict=True)
        num_live_sessions = live_sessions[0].get('num_live_sessions', 0)
        email_sent = False

        if num_live_sessions > 1:
            email_sent = send_email_helper(email, "session exceeded")
            
        else:
            send_email_helper(email, "Welcome template2")        
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

        

def send_email_helper(user_email, header=None):
    """Send email using an email template."""
    if not user_email:
        return False

    # if  template_name:
    #     email_template = frappe.get_doc("Email Template", template_name)
    #     print(email_template)
    #     subject = email_template.subject
    #     print(subject)
    #     content = email_template.response_html
    #     print(content)
    #     rendered_content= frappe.render_template(content, {'site_url': 'your_site_url', 'link': 'your_verification_link'})
    #     print(content)
    # else:
    #     return false



    # Set default header if not provided
    if not header:
        header = "Welcome"
    else:
        header = header

    # Set up email parameters
    email_args = {
        "recipients": user_email,
        # "template": "one_tap_v1/templates/emails/welcome.html",
        "sender": None,
        "subject": "welcome to company",
        # "message": email_template.response,
        "content": frappe.render_template("one_tap_v1/templates/emails/welcome.html"),
        "header": [_(header), "blue"],
        "delayed": False,
        "retry": 3,
        "user_name":"vishal",
        "logo_url":"13.233.216.191/files/Logo%20WHITE%20COLOR.png"
    }

    # Send email using Frappe's sendmail function
    enqueue(
        method=frappe.sendmail,
        queue="short",
        timeout=300,
        event=None,
        is_async=True,
        job_name=None,
        now=False,
        **email_args,
    )
    print(email_args['content'])
    return True

# +++++++++++++++++++++++++++++++++++++++++++
@frappe.whitelist()
def send_email(user_mail,subject = None):
    if not user_mail:
        return False
    if not subject:
        subject = "Welcome"
        
    email_args ={
        "logo_url": "/files/Logo%20WHITE%20COLOR.png",
        "user_name": "Vishal"
    }
    
    attachment_url = "/files/Logo%20WHITE%20COLOR.png"
    
    frappe.sendmail(
        recipients = user_mail,
        subject = subject,
        template ="welcome",
        args = email_args,
        attachments=[{"file_url":attachment_url}]
        
    )
    
    return True

    
    
    
    
    
    
    
@frappe.whitelist(allow_guest=True)
def ping():
    return "pong"


import frappe


@frappe.whitelist(allow_guest=True)
def send_welcome_email(email):
    try:
        # Retrieve the email template
        email_template = frappe.get_doc("Email Template", "welcome template2")
        print(email_template)

        if email_template:
            # Render the email template
            email_content = frappe.render_template(email_template.response)
            print(email_content)

            # Send the email
            frappe.sendmail(
                recipients=email,
                subject=email_template.subject,
                message=email_content
            )
            return "Welcome email sent successfully."
        else:
            return "Welcome email template not found."
    except Exception as e:
        frappe.log_error(f"Error sending welcome email: {str(e)}")
        return "Failed to send welcome email. Please try again later."
    
    
@frappe.whitelist()
def update_ot_customer():
    data = frappe.request.json
    cust_doc =frappe.get_doc('OT Customer Details',{'name':data['customer_id']})
    for k,v in data.items():
        cust_doc.set(k,v)
    return cust_doc
    

@frappe.whitelist()
def update_customer_helper(data):
    if not frappe.get_all("Ot Customer Details",filters={"Name":data.get('customer_detail_id',None)}):
        cus_detail_doc=frappe.get_doc({"doctype":"Ot Customer Details"})
        cus_detail_doc.insert()
        data['cus_detail_id'] = cus_detail_doc.name
        
    cus_details = frappe.get_doc("Ot Customer Detail"),data['customer_detail_id']
    for k,v in data.items():
            if k in ["customer_detail_id","business_activities_suggested", "share_holders_details"]:
                    if k =="share_holder_details":
                        customer_details = cus_detail.share_holder_details
                        
def send_email_helper1(user_email, subject=None, message=None, header=None):
    """Send token to user as email."""
    if not user_email:
        return False
    if not subject:
        subject = "Some Default Subject"
    if not message:
        message = "Some Default Message"
    if not header:
        header = "Welcome"

    attachment_url = "/files/Logo%20WHITE%20COLOR.png"
    temp_args = {
        "logo_url": "/files/Logo%20WHITE%20COLOR.png",
        "user_name": "Vishal"
    }

    email_args = {
        "recipients": user_email,
        "sender": None,
        "subject": subject,
        "template": "welcome",
        "attachments": [{"file_url": attachment_url}],
        "message": message,
        "header": [_(header), "blue"],
        "delayed": False,
        "retry": 3,
    }

    enqueue(
        method=frappe.sendmail,
        queue="short",
        timeout=300,
        event=None,
        is_async=True,
        job_name=None,
        now=False,
        **email_args,
        **temp_args
    )
    return True
# ==========================================================================================================================================
@frappe.whitelist(allow_guest=True)
def handle_after_login2(email):
    try:
        if validate_email(email):
            return validate_session(email)
        else:
            return "Error: User email not found. Unable to send login email."
    except frappe.DoesNotExistError:
        return "Error: User does not exist"


def is_valid_email(email):
    # Regular expression pattern for validating email
    pattern = r'^[\w\.-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(pattern, email))

def validate_email(email):
    return email != "Administrator" and email != "Guest" and is_valid_email(email)

def send_email_after_login1(email):
    try:
        subject = "Login Notification"
        body = "You have successfully logged in."
        # return send_email_helper(email,"Welcome template") 
        return send_welcome_email(email,"Welcome template2")
        return "email sent"
    except frappe.DoesNotExistError:
        return "Error: User does not exist"

def validate_session(email):
    try:
        threshold_time = datetime.now() - timedelta(minutes=5)
        live_sessions = frappe.db.sql("""
            SELECT COUNT(*) as num_live_sessions
            FROM `tabSessions`
            WHERE `user` = (SELECT `name` FROM `tabUser` WHERE `email` = %s) 
            AND lastupdate > %s 
        """, (email, threshold_time), as_dict=True)
        num_live_sessions = live_sessions[0].get('num_live_sessions', 0)
        email_sent = False

        if num_live_sessions > 1:
            email_sent = send_email_helper(email, "session exceeded")
            
        else:
            send_email_helper(email, "Welcome Template")        
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


def send_email_helper2(user_email,template=None, subject=None, message=None, header=None):
    """Send token to user as email."""
    if not user_email:
        return False
    if not subject:
        subject = "Some Default Subject"
    if not message:
        message = "Some Default Message"
    if not header:
        header = "Welcome"

    # attachment_url = "http://3.110.128.51/files/Logo%20blue%20%20COLOR.png"
    # temp_args = {
    #     "logo_url": "http://3.110.128.51/files/Logo%20blue%20%20COLOR.png",
    #     "user_name": "Vishal"
    # }

    email_args = {
        "recipients": user_email,
        "sender": None,
        "subject": subject,
        "template": "Welcome Template",
        # "attachments": [{"file_url": attachment_url}],
        "message": template.response,
        "header": [_(header), "blue"],
        "delayed": False,
        "retry": 3,
    }

    enqueue(
        method=frappe.sendmail,
        queue="short",
        timeout=300,
        event=None,
        is_async=True,
        job_name=None,
        now=False,
        **email_args,
    
    )
    return True





