import frappe
from frappe import _
import requests
import json
import re
from .helper.otp_helper import send_email_helper
import logging
from datetime import datetime, timedelta
from frappe.sessions import delete_session, clear_sessions

@frappe.whitelist(allow_guest=True)
# def handle_before_login(email):
def handle_before_login(login_manager):
    try:
        email = login_manager.user
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
        return send_email_helper(email, subject, body)
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

        if num_live_sessions > 2:
            email_sent = send_email_helper(email, "Maximum Sessions Exceeded", "Maximum login sessions exceeded for the user.")
            delete_session(frappe.session.sid, user=email, reason="User Manually Logged Out")
            clear_cookies()
            return "Maximum no. of sessions reached"
            # clear_sessions(email)
            # return frappe.session.sid
            # frappe.throw(_("Session limit exceeded"))
        else:
            send_email_helper(email, "Login Notification", "You have successfully logged in.")        
        # return {
        #     "email": email,
        #     "num_live_sessions": num_live_sessions,
        #     "email_sent": email_sent
        # }
    except Exception as e:
        print(f"Error in get_live_sessions2: {str(e)}")
        return {
            "error": str(e)
        }

def clear_cookies():
	if hasattr(frappe.local, "session"):
		frappe.session.sid = "Test"
		frappe.session.multisession = True
	frappe.local.cookie_manager.delete_cookie(["full_name", "user_id", "sid", "user_image", "system_user"])