import frappe
from .doctype import Doctype

def update_task_status_helper(data):
    task = frappe.get_doc(Doctype.TASK, data['task_name'])
    task.status = data.get('status', "Completed")
    task.save(ignore_permissions=True)
    frappe.db.commit()
    return "Task updated successfully"

def get_project_tasks_helper(project_id):
    tasks = frappe.get_all(Doctype.TASK, filters={'project': project_id}, fields=["name", "subject", "status"], order_by="subject")
    resp = {}
    idx = 1
    for task in tasks:
        resp[idx] = {
            "task_name": task.name,
            "subject": task.subject,
            "status": task.status
        }
        idx += 1
    return resp