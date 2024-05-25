import requests
import frappe

@frappe.whitelist(allow_guest=True)
def get_conversations():
    url = "https://flowxo.com/api/conversations/"
    payload = {}
    headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2NTlmZjNiNGQ4MjM5ODAwN2M2NDk3MzkiLCJyb2xlIjoidXNlciIsImZlYXR1cmVzIjpbXSwiYXBpX2tleSI6dHJ1ZSwiaWF0IjoxNzA0OTgxNDI4fQ.yWKEfsUADHiF2B4fu8Pf8JTRQWsCPz98KpWj3mpGQT8',
        'Content-Type': 'application/json'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    if response.status_code == 200:
        return response.json()  # Parse JSON response
    else:
        return response.status_code

@frappe.whitelist(allow_guest=True)
def get_conversations_summary():
    data = json.loads(frappe.request.data)
    url = f"https://flowxo.com/api/conversations/{data['id']}"
    payload = {}
    headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2NTlmZjNiNGQ4MjM5ODAwN2M2NDk3MzkiLCJyb2xlIjoidXNlciIsImZlYXR1cmVzIjpbXSwiYXBpX2tleSI6dHJ1ZSwiaWF0IjoxNzA0OTgxNDI4fQ.yWKEfsUADHiF2B4fu8Pf8JTRQWsCPz98KpWj3mpGQT8',
        'Content-Type': 'application/json'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    if response.status_code == 200:
        return response.json()  # Parse JSON response
    else:
        return response.status_code

@frappe.whitelist(allow_guest=True)
def get_conversations_messages(id):
    data = json.loads(frappe.request.data)
    url = f"https://flowxo.com/api/conversations/{data['id']}/messages"
    payload = {}
    headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2NTlmZjNiNGQ4MjM5ODAwN2M2NDk3MzkiLCJyb2xlIjoidXNlciIsImZlYXR1cmVzIjpbXSwiYXBpX2tleSI6dHJ1ZSwiaWF0IjoxNzA0OTgxNDI4fQ.yWKEfsUADHiF2B4fu8Pf8JTRQWsCPz98KpWj3mpGQT8',
        'Content-Type': 'application/json'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    if response.status_code == 200:
        return response.json()  # Parse JSON response
    else:
        return response.status_code

@frappe.whitelist(allow_guest=True)
def get_FlowXO():
    url = f"https://flowxo.com/app/livechat?c_am&_hideLogo=true&&_hideNav=true&_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2NTlmZjNiNGQ4MjM5ODAwN2M2NDk3MzkiLCJyb2xlIjoiQWdlbnQiLCJzZXNzaW9uX3NlY3JldCI6IiQyYiQxMCR3ZVRpTWlKencxSDBSRTFROWNaSjJlUWtrVEpwdWc3czY2ZW9nNmFMVGVqNzYuVDVzRllnYSIsImZlYXR1cmVzIjpbXSwidGVhbU1lbWJlcklkIjoiNjVhNTMxNWRkZjQ5NjMwMDVmMDBkNTFhIiwiaWF0IjoxNzA1MzI1MzAxfQ.5C_Lqo0qlbZuJcudEVd9e9ytnbOJ4_HPc-LnaA0jQuc"
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    if response.status_code == 200:
        return response.json()  # Parse JSON response
    else:
        return response.status_code
