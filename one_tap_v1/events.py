from one_tap_v1.helper.otp_helper import send_email_after_login

def get_hooks():
    return {
        "on_login": [
            send_email_after_login
        ]
    }