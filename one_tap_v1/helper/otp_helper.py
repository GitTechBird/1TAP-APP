import frappe
import json
import pyotp
from frappe import _
from frappe.utils.background_jobs import enqueue
from frappe.auth import LoginManager
from frappe.twofactor import (
    get_otpsecret_for_,
    get_verification_obj,
    get_verification_method,
    confirm_otp_token
	# get_email_subject_for_2fa,
	# get_email_body_for_2fa
)
from datetime import datetime
from frappe import db

#Custom Functions
def generate_otp_helper(data):
    return authenticate_for_2factor_modified(data.get('email'))

def invalidate_previous_otps(user):
    # Invalidate previous OTPs for the user by updating the valid_until field to a past datetime
    current_datetime = datetime.utcnow()
    db.sql("UPDATE `tabOTP` SET valid_until = %s WHERE user = %s AND valid_until > %s", (current_datetime, user, current_datetime))

def validate_otp_helper(data):
    login_manager = LoginManager()
    login_manager.user = data.get('email')
    # invalidate_previous_otps(login_manager.user)
    return confirm_otp_token(login_manager, data.get('otp'), data.get('tmp_id', None))

# Frappe Functions
def get_email_body_for_2fa(kwargs_dict):
	"""Get email body for 2fa."""
	body_template = """
		Enter this code to complete your registration:
		<br><br>
		<b style="font-size: 18px;">{{ otp }}</b>
	"""
	return frappe.render_template(body_template, kwargs_dict)

def get_email_subject_for_2fa(kwargs_dict):
	"""Get email subject for 2fa."""
	subject_template = _("Registration Verification Code from {}").format(
		frappe.get_system_settings("otp_issuer_name")
	)
	return frappe.render_template(subject_template, kwargs_dict)

def authenticate_for_2factor_modified(user):
	"""Authenticate two factor for enabled user before login."""
	if frappe.form_dict.get("otp"):
		return
	otp_secret = get_otpsecret_for_(user)
	token = int(pyotp.TOTP(otp_secret).now())
	tmp_id = frappe.generate_hash(length=8)
	cache_2fa_data_modified(user, token, otp_secret, tmp_id)
	otp_issuer = frappe.get_system_settings("otp_issuer_name")
	verification_obj = process_2fa_for_email_modified(user, token, otp_secret, otp_issuer)
	# Save data in local
	frappe.local.response["verification"] = verification_obj
	frappe.local.response["tmp_id"] = tmp_id

def cache_2fa_data_modified(user, token, otp_secret, tmp_id):
    """Cache and set expiry for data."""
    expiry_time = frappe.flags.token_expiry or 300
    frappe.cache.set(tmp_id + "_token", token)
    frappe.cache.expire(tmp_id + "_token", expiry_time)
    for k, v in {"_usr": user, "_otp_secret": otp_secret}.items():
        frappe.cache.set(f"{tmp_id}{k}", v)
        frappe.cache.expire(f"{tmp_id}{k}", expiry_time)

def process_2fa_for_email_modified(user, token, otp_secret, otp_issuer):
	"""Sending email verification"""
	prompt = _("Verification code has been sent to your registered email address.")
	subject=None
	message=None
	status = send_token_via_email(user, token, otp_secret, otp_issuer, subject=subject, message=message)
	return {
		"token_delivery": status,
		"prompt": status and prompt,
		"method": "Email",
		"setup": status,
	}

def send_token_via_email(user, token, otp_secret, otp_issuer, subject=None, message=None):
	"""Send token to user as email."""
	hotp = pyotp.HOTP(otp_secret)
	otp = hotp.at(int(token))
	template_args = {"otp": otp, "otp_issuer": otp_issuer}
	if not subject:
		subject = get_email_subject_for_2fa(template_args)
	if not message:
		message = get_email_body_for_2fa(template_args)

	email_args = {
		"recipients": user,
		"sender": None,
		"subject": subject,
		"message": message,
		"header": [_("Verfication Code"), "blue"],
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

def send_email_helper(user_email, subject=None, message=None, header=None):
	"""Send token to user as email."""
	if not user_email:
		return False
	if not subject:
		subject = "Some Default Subject"
	if not message:
		message = "Some Default Message"
	if not header:
		header = "Welcome"

	email_args = {
		"recipients": user_email,
		"sender": None,
		"subject": subject,
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
	)
	return True


# def send_email_after_login(login_manager):
#     # doc = frappe.get_doc({
# 	# 	"doctype": "Company_test",
# 	# 	"company_name": "Test"
# 	# })
#     # doc.insert()
# 	# Call the function to send the login email
#     send_email_helper(login_manager.user, "Welcome email", "Welcome to 1tap.")


# def send_email_helper(user_email, template_name=None, subject=None, header=None):
#     """Send email using an email template."""
#     if not user_email:
#         return False

#     if template_name:
#         email_template = frappe.get_doc("Email Template", template_name)
#         subject = email_template.subject
#     else:
#         if not subject:
#             subject = "Some Default Subject"
#         if not message:  # Assuming message is a parameter you forgot to define
#             message = "Some Default Message"
#         if not header:
#             header = "Welcome"

#     email_args = {
#         "recipients": user_email,
#         "sender": None,
#         "subject": subject,
#         "message": email_template.response if template_name else message,
#         "header": [_(header), "blue"],
#         "delayed": False,
#         "retry": 3,
#     }

#     # Send email using Frappe's sendmail function
#     enqueue(
#         method=frappe.sendmail,
#         queue="short",
#         timeout=300,
#         event=None,
#         is_async=True,
#         job_name=None,
#         now=False,
#         **email_args,
#     )

#     return True
