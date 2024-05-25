# def delete_function(**args, **kwargs):
#     l = args
#     d = kwargs
#     print(l)
#     print(d)
#     pass
import frappe

def print_hello_on_update(doc, method):
    for fieldname, value in doc.get("__old_values", {}).items():
        old_value = value
        new_value = doc.get(fieldname)
        print(f"Field '{fieldname}' changed from '{old_value}' to '{new_value}'")

    print("Hello")

def Ot_zone_master_change(doc, method):
    frappe.logger().info(f'QWERTY : {doc.name}')