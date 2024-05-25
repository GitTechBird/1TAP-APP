import frappe
from frappe import _
from frappe.utils import now_datetime
from datetime import timedelta

def custom_login(login_manager):
    try:
        # Get username from the login_manager object
        email = login_manager.user

        # Check number of active sessions for the user
        active_sessions = get_active_sessions(email)

        if len(active_sessions) < 2:
            # Allow login
            login_user(email)
        else:
            # Trigger email notification
            send_session_limit_exceeded_email(email)
            # Prevent login
            frappe.msgprint(_("Session limit exceeded"))
    except Exception as e:
        # Log the exception for debugging
        frappe.log_error(f"Error during custom login: {e}", title="Custom Login Error")

def get_active_sessions(email):
    try:
        # Retrieve active sessions for the user
        active_sessions = frappe.get_all("User Session", filters={"user": email, "session_expiry": (">", now_datetime())}, fields=["name"])

        # Return active sessions
        return active_sessions
    except Exception as e:
        # Log the exception for debugging
        frappe.log_error(f"Error while fetching active sessions: {e}", title="Active Sessions Error")
        return []

def send_session_limit_exceeded_email(email):
    try:
        # Send an email notification to the user
        frappe.sendmail(
            recipients=email,
            subject=_("Session Limit Exceeded"),
            message=_("You have exceeded the maximum number of allowed sessions."),
        )
    except Exception as e:
        # Log the exception for debugging
        frappe.log_error(f"Error while sending session limit exceeded email: {e}", title="Session Limit Exceeded Email Error")

def login_user(email):
    try:
        # Implement your login logic here
        # This might involve validating the credentials against the database
        # and creating a new session record if the login is successful
        # For simplicity, let's assume a successful login creates a new session record
        frappe.get_doc({
            "doctype": "User Session",
            "user": email,
            "session_expiry": now_datetime() + timedelta(hours=1)  # Assuming session expiry in 1 hour
        }).insert(ignore_permissions=True)
    except Exception as e:
        # Log the exception for debugging
        frappe.log_error(f"Error during login user: {e}", title="Login User Error")
