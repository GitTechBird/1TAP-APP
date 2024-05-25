import frappe
import pyotp
from frappe.auth import LoginManager
from frappe.twofactor import (
	confirm_otp_token,
    get_otpsecret_for_,
    get_verification_obj,
    get_verification_method
)

# Frappe Modified Functions
def authenticate_for_2factor_modified(user):
	"""Authenticate two factor for enabled user before login."""
	if frappe.form_dict.get("otp"):
		return
	otp_secret = get_otpsecret_for_(user)
	token = int(pyotp.TOTP(otp_secret).now())
	tmp_id = frappe.generate_hash(length=8)
	cache_2fa_data(user, token, otp_secret, tmp_id)
	verification_obj = get_verification_obj(user, token, otp_secret)
	# Save data in local
	frappe.local.response["verification"] = verification_obj
	frappe.local.response["tmp_id"] = tmp_id

def cache_2fa_data(user, token, otp_secret, tmp_id):
    """Cache and set expiry for data."""
    pwd = frappe.form_dict.get("pwd")
    verification_method = get_verification_method()

    # set increased expiry time for SMS and Email
    if verification_method in ["SMS", "Email"]:
        expiry_time = frappe.flags.token_expiry or 300
        frappe.cache.set(str(tmp_id) + "_token", str(token))
        frappe.cache.expire(str(tmp_id) + "_token", expiry_time)
    else:
        expiry_time = frappe.flags.otp_expiry or 180
    for k, v in {"_usr": user, "_pwd": pwd, "_otp_secret": otp_secret}.items():
        frappe.cache.set(str(tmp_id) + str(k), str(v))
        frappe.cache.expire(str(tmp_id) + str(k), expiry_time)

## OTP
# generate otp
@frappe.whitelist()
def generate_otp(user_email):
    return authenticate_for_2factor_modified(user_email)

# validate_otp
@frappe.whitelist()
def validate_otp(user_email, otp, tmp_id):
    login_manager = LoginManager()
    login_manager.user = user_email
    return confirm_otp_token(login_manager, otp, tmp_id)

@frappe.whitelist()
def send_email_helper(user_email, subject=None, message=None):
	"""Send token to user as email."""
	if not user_email:
		return False
	if not subject:
		subject = "Some Default Subject"
	if not message:
		message = "Some Default Message"

	email_args = {
		"recipients": user_email,
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