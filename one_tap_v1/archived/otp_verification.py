import frappe
from .test_otp import authenticate_for_2factor, confirm_otp_token

@frappe.whitelist()
def generate_otp(user_email):
    return authenticate_for_2factor(user_email)

@frappe.whitelist()
def validate_otp(user_email, otp, tmp_id):
    try:
        # return confirm_otp_token(user_email, otp, tmp_id)
        if confirm_otp_token(user_email, otp, tmp_id):
            return "Success"
        else:
            return "Error"
    except Exception as e:
        return e