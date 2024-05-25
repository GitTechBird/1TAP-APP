# my_app/my_app/api/tasks.py

import frappe
from frappe import json

@frappe.whitelist()
def generate_tasks(num_tasks):
    try:
        num_tasks = int(num_tasks)

        new_tasks = []
        for i in range(num_tasks):
            task_name = f"Task {i+1}"
            new_task = frappe.get_doc({
                'doctype': 'Task',
                'subject': task_name,
                 'project' : 'PROJ-0003'

                # Add more fields as needed
            })
            new_task.insert()
            new_tasks.append(new_task)

        return {"message": f"{num_tasks} tasks generated successfully", "tasks": new_tasks}

    except Exception as e:
        frappe.log_error(f"Error generating tasks: {str(e)}")
        return {"error": str(e)}

@frappe.whitelist()
def auto_generate_task():
    try:
        task_name = frappe.generate_hash(length=8)  # Generate a random task name
        new_task = frappe.get_doc({
            'doctype': 'Task',
            'subject': f"Auto-Generated Task - {task_name}",
            # Add more fields as needed
        })
        new_task.insert()

        return {"message": "Task auto-generated successfully", "task": new_task}

    except Exception as e:
        frappe.log_error(f"Error auto-generating task: {str(e)}")
        return {"error": str(e)}


# Python code to update prices based on changes in activity groups

@frappe.whitelist()
def update_prices():
        # Fetch activity groups with associated price changes
        activity_groups = frappe.get_all("Activity Group", filters={"status": "Active"}, fields=["name", "new_price"])
        print(activity_groups);
        return activity_groups
        for group in activity_groups:
            # Fetch items associated with the activity group
            items = frappe.get_all("Item", filters={"activity_group": group.name}, fields=["name", "price"])

            # Update prices based on the new price in the activity group
            for item in items:
                frappe.db.set_value("Item", item.name, "price", group.new_price)

        frappe.db.commit()
#         frappe.msgprint("Prices updated successfully")

#     except Exception as e:
#         frappe.log_error(f"Error updating prices: {str(e)}")

# if __name__ == "__main__":
#     update_prices()
