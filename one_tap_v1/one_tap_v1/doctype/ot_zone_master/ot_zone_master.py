# Copyright (c) 2024, one_tap_v1 and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class OTZoneMaster(Document):
    pass



def Ot_zone_master_change(doc, method):
    frappe.logger().info(f'QWERTY : {doc.name}')
    frappe.logger().debug('This is a debug message')
    frappe.logger().info('This is an info message')
    frappe.logger().warning('This is a warning message')
    frappe.logger().error('This is an error message')
    frappe.logger().critical('This is a critical message')