# import frappe
# from frappe.utils.otp import get_otp_secret, validate_otp
# # from frappe.utils.password import validate_otp_token


# # Function to generate OTP
def generate_otp(length=6):
    """Generate OTP using Frappe's built-in method"""
    return frappe.generate_hash(length=6)

# # Function to send OTP via email
# def send_otp_email(email, otp):
#     """Send OTP to email using Frappe's built-in method"""
#     subject = "Your OTP for verification"
#     message = f"Your OTP is: {otp}"
#     return frappe.sendmail(recipients=email, subject=subject, message=message)

# # Function to validate OTP
# # def validate_otp(email, otp):
# #     """Validate OTP using Frappe's built-in method"""
# #     # Fetch stored OTP from database
# #     stored_otp = frappe.db.get_value("User", {"email": email}, "otp")

# #     # Compare OTPs
# #     if stored_otp and stored_otp == otp:
# #         return True
# #     else:
# #         return False

# # Function to validate OTP
# def validate_otp(email, otp):
#     # """Validate OTP using Frappe's built-in method"""
#     # valid, message = validate_otp_token(email, otp)
#     # return valid
#     """Validate OTP using Frappe's built-in method"""
#     secret = get_otp_secret(email)
#     valid = validate_otp(secret, otp)
#     return valid



import frappe
# from frappe.utils.password import generate_otp, validate_otp_token

def generate_and_send_otp(email):
    """Generates and sends OTP to the specified email address."""
    # Generate OTP
    otp = generate_otp(length=6)

    # Send OTP via email
    # send_otp_email(email, otp)

    # Return the generated OTP
    return otp

def validate_otp(email, otp):
    """Validates the provided OTP for the specified email address."""
    # Validate OTP token
    is_valid = validate_otp_token(email, otp)

    return is_valid

def send_otp_email(email, otp):
    """Sends the OTP to the specified email address."""
    subject = "Your OTP for verification"
    message = f"Your OTP is: {otp}"
    frappe.sendmail(recipients=email, subject=subject, message=message)


import frappe

def send_2fa_verification_email(user_email, otp):
    """Send email for 2FA verification"""

    # Construct verification link with OTP
    verification_link = f"https://example.com/verify_2fa?otp={otp}"

    # Email subject
    subject = "2FA Verification"

    # Email body with verification link
    body = f"Dear User,\n\nPlease click the following link to verify your account for 2FA:\n\n{otp}"

    try:
        # Send email using Frappe's built-in sendmail function
        frappe.sendmail(
            recipients=user_email,
            subject=subject,
            message=body
        )
        return "2FA verification email sent successfully."
    except Exception as e:
        return "Error sending 2FA verification email: {str(e)}"

import frappe

def send_email(recipient, subject, message):
    """Send an email using Frappe's sendmail function."""
    try:
        frappe.sendmail(
            recipients=recipient,
            subject=subject,
            message=message
        )
        print("Email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")


def run():
    email = "hitesh.sahu@techbirdit.in"
    otp = generate_and_send_otp(email)
    # print("Otp Generated", otp)
    # # email_ack = send_otp_email(email, otp)
    # # print("Otp Sent", email_ack)
    # validate_otp(email, otp)
    # print("Otp Validated")
    # print(send_2fa_verification_email(email, otp))
    print(send_email(email, "OTP", "213123"))
