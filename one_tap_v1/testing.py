# import frappe
# from frappe.utils import get_url
# def send_welcome_mail_to_user():
#     link = reset_password()
#     subject = None
#     method = frappe.get_hooks("welcome_email")
#     if method:
#         subject = frappe.get_attr(method[-1])()
#     if not subject:
#         site_name = frappe.db.get_default("site_name") or frappe.get_conf().get("site_name")
#         if site_name:
#             subject = _("Welcome to {0}").format(site_name)
#         else:
#             subject = _("Complete Registration")

#     welcome_email_template = frappe.db.get_system_setting("welcome_email_template")

#     send_login_mail(
#         subject,
#         "new_user",
#         dict(
#             link=link,
#             site_url=get_url(),
#         ),
#         custom_template=welcome_email_template,
#     )


# 	def reset_password(self, send_email=False, password_expired=False):
# 		from frappe.utils import get_url, now_datetime
#         from frappe.utils.data import sha256_hash


# 		key = frappe.generate_hash()
# 		hashed_key = sha256_hash(key)
# 		# self.db_set("reset_password_key", hashed_key)
# 		# self.db_set("last_reset_password_key_generated_on", now_datetime())

# 		url = "/update-password?key=" + key
# 		if password_expired:
# 			url = "/update-password?key=" + key + "&password_expired=true"

# 		link = get_url(url)
# 		if send_email:
# 			self.password_reset_mail(link)

# 		return link

# def send_login_mail(self, subject, template, add_args, now=None, custom_template=None):
#     """send mail with login details"""
#     from frappe.utils import get_url
#     from frappe.utils.user import get_user_fullname

#     created_by = get_user_fullname(frappe.session["user"])
#     if created_by == "Guest":
#         created_by = "Administrator"
#     first_name = "A"
#     last_name = "P"
#     name = "V"
#     args = {
#         "first_name": first_name or last_name or "user",
#         "user": name,
#         "title": subject,
#         "login_url": get_url(),
#         "created_by": created_by,
#     }

#     args.update(add_args)

#     sender = (
#         frappe.session.user not in STANDARD_USERS and get_formatted_email(frappe.session.user) or None
#     )

#     if custom_template:
#         from frappe.email.doctype.email_template.email_template import get_email_template

#         email_template = get_email_template(custom_template, args)
#         subject = email_template.get("subject")
#         content = email_template.get("message")

#     frappe.sendmail(
#         recipients=self.email,
#         sender=sender,
#         subject=subject,
#         template=template if not custom_template else None,
#         content=content if custom_template else None,
#         args=args,
#         header=[subject, "green"],
#         delayed=(not now) if now is not None else self.flags.delay_emails,
#         retry=3,
#     )

# 	def password_reset_mail(link):
# 		reset_password_template = frappe.db.get_system_setting("reset_password_template")

# 		send_login_mail(
# 			_("Password Reset"),
# 			"password_reset",
# 			{"link": link},
# 			now=True,
# 			custom_template=reset_password_template,
# 		)

import frappe
from frappe.utils import get_url
from frappe.utils.data import sha256_hash
from frappe.utils.user import get_user_fullname
from frappe.email.doctype.email_template.email_template import get_email_template

def send_welcome_mail_to_user():
    link = reset_password()
    subject = None
    method = frappe.get_hooks("welcome_email")
    if method:
        subject = frappe.get_attr(method[-1])()
    if not subject:
        site_name = frappe.db.get_default("site_name") or frappe.get_conf().get("site_name")
        if site_name:
            subject = _("Welcome to {0}").format(site_name)
        else:
            subject = _("Complete Registration")

    welcome_email_template = frappe.db.get_system_setting("welcome_email_template")

    send_login_mail(
        subject,
        "new_user",
        dict(
            link=link,
            site_url=get_url(),
        ),
        custom_template=welcome_email_template,
    )

def reset_password(send_email=False, password_expired=False):
    key = frappe.generate_hash()
    hashed_key = sha256_hash(key)
    # self.db_set("reset_password_key", hashed_key)
    # self.db_set("last_reset_password_key_generated_on", now_datetime())

    url = "/update-password?key=" + key
    if password_expired:
        url = "/update-password?key=" + key + "&password_expired=true"

    link = get_url(url)
    if send_email:
        password_reset_mail(link)

    return link

def send_login_mail(subject, template, add_args, now=None, custom_template=None):
    created_by = get_user_fullname(frappe.session["user"])
    if created_by == "Guest":
        created_by = "Administrator"
    first_name = "A"  # You may want to replace these placeholders with actual values
    last_name = "P"   # You may want to replace these placeholders with actual values
    name = "V"        # You may want to replace these placeholders with actual values
    args = {
        "first_name": first_name or last_name or "user",
        "user": name,
        "title": subject,
        "login_url": get_url(),
        "created_by": created_by,
    }

    args.update(add_args)

    sender = (
        frappe.session.user not in STANDARD_USERS and get_formatted_email(frappe.session.user) or None
    )

    if custom_template:
        email_template = get_email_template(custom_template, args)
        subject = email_template.get("subject")
        content = email_template.get("message")

    frappe.sendmail(
        recipients=self.email,
        sender=sender,
        subject=subject,
        template=template if not custom_template else None,
        content=content if custom_template else None,
        args=args,
        header=[subject, "green"],
        delayed=(not now) if now is not None else self.flags.delay_emails,
        retry=3,
    )

def password_reset_mail(link):
    reset_password_template = frappe.db.get_system_setting("reset_password_template")

    send_login_mail(
        _("Password Reset"),
        "password_reset",
        {"link": link},
        now=True,
        custom_template=reset_password_template,
    )
