import frappe
from frappe import _
import requests
import json
import re
from .helper.otp_helper import send_email_helper
import logging
from datetime import datetime, timedelta

# @frappe.whitelist(allow_guest=True)
# def handle_after_login(email):
def handle_after_login(login_manager):
    try:
        email = login_manager.user
        if validate_email(email):
            return validate_session(email, login_manager)
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
        return send_email_helper(email, subject, body)
    except frappe.DoesNotExistError:
        return "Error: User does not exist"

def validate_session(email, login_manager):
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

        if num_live_sessions > 20:
            email_sent = send_email_helper(email, "Maximum Sessions Exceeded", "Maximum login sessions exceeded for the user.")
            login_manager.logout()
            # frappe.throw(_("Session limit exceeded"))
        else:
            send_email_helper(email, "Login Notification", "You have successfully logged in.")        
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
        
# # import frappe
# # from frappe import _
# # import requests
# # import json
# # import re
# # from .helper.otp_helper import send_email_helper
# # import logging
# # from datetime import datetime, timedelta

# @frappe.whitelist(allow_guest=True)
# def handle_after_login1(email):
# # def handle_after_login(login_manager):
#     try:
#         # email = login_manager.user
#         if validate_email(email):
#             # return validate_session(email, login_manager)
#             return validate_session(email)
#         else:
#             return "Error: User email not found. Unable to send login email."
#     except frappe.DoesNotExistError:
#         return "Error: User does not exist"

# def is_valid_email(email):
#     # Regular expression pattern for validating email
#     pattern = r'^[\w\.-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
#     return bool(re.match(pattern, email))

# def validate_email(email):
#     return email != "Administrator" and email != "Guest" and is_valid_email(email)

# def send_email_after_login(email):
#     try:
        
#         return send_email_helper1(email, "Welcome Template")
#     except frappe.DoesNotExistError:
#         return "Error: User does not exist"

# # def validate_session(email, login_manager):
# def validate_session(email):
#     try:
#         threshold_time = datetime.now() - timedelta(minutes=5)
#         live_sessions = frappe.db.sql("""
#             SELECT COUNT(*) as num_live_sessions
#             FROM `tabSessions`
#             WHERE `user` = (SELECT `name` FROM `tabUser` WHERE `email` = %s) 
#             AND lastupdate > %s 
#         """, (email, threshold_time), as_dict=True)
#         num_live_sessions = live_sessions[0].get('num_live_sessions', 0)
#         email_sent = False

#         if num_live_sessions > 2:
#             email_sent = send_email_helper1(email, "session exceeded")
#             # login_manager.logout()
#             # frappe.throw(_("Session limit exceeded"))
#         else:
#             send_email_helper1(email, "Welcome Template")        
#         return {
#             "email": email,
#             "num_live_sessions": num_live_sessions,
#             "email_sent": email_sent
#         }
#     except Exception as e:
#         print(f"Error in handle_after_login: {str(e)}")
#         return {
#             "error": str(e)
#         }
        
        
# def handle_after_login(login_manager):
#     try:
#         email = login_manager.user
#         if validate_email(email):
#             return validate_session(email, login_manager)
#         else:
#             return "Error: User email not found. Unable to send login email."
#     except frappe.DoesNotExistError:
#         return "Error: User does not exist"

# def is_valid_email(email):
#     # Regular expression pattern for validating email
#     pattern = r'^[\w\.-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
#     return bool(re.match(pattern, email))

# def validate_email(email):
#     return email != "Administrator" and email != "Guest" and is_valid_email(email)

# def send_email_after_login(email):
#     try:
#         subject = "Login Notification"
#         body = "You have successfully logged in."
#         return send_welcome_email(email,"Welcome template")
#     except frappe.DoesNotExistError:
#         return "Error: User does not exist"

# def validate_session(email, login_manager):
#     try:
#         threshold_time = datetime.now() - timedelta(minutes=5)
#         live_sessions = frappe.db.sql("""
#             SELECT COUNT(*) as num_live_sessions
#             FROM `tabSessions`
#             WHERE `user` = (SELECT `name` FROM `tabUser` WHERE `email` = %s) 
#             AND lastupdate > %s 
#         """, (email, threshold_time), as_dict=True)
#         num_live_sessions = live_sessions[0].get('num_live_sessions', 0)
#         email_sent = False

#         if num_live_sessions > 2:
#             email_sent = send_email_helper(email, "session exceeded")
#             login_manager.logout()
#             # frappe.throw(_("Session limit exceeded"))
#         else:
#             send_email_helper(email, "Welcome template")       
#         return {
#             "email": email,
#             "num_live_sessions": num_live_sessions,
#             "email_sent": email_sent
#         }
#     except Exception as e:
#         print(f"Error in get_live_sessions2: {str(e)}")
#         return {
#             "error": str(e)
#         }