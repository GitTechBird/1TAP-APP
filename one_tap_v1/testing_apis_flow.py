import requests
import frappe
@frappe.whitelist
# def generate(email, pwd):
    # generate otp for email
def generate(args):
    email = args.get("email")
    pwd = args.get("pwd")
    url = "http://13.233.216.191/api/method/one_tap_v1.api.generate_otp"
    querystring = {"user_email": email}
    headers = {"Authorization": "token 71c26bf67dc93c9:9f6b42ec03533c8"}
    response = requests.get(url, headers=headers, params=querystring)
    response = response.json()

    # validate otp
    otp = input("Enter the otp")
    url = "http://13.233.216.191/api/method/one_tap_v1.api.validate_otp"
    querystring = {"user_email":email,"otp": otp,"tmp_id": response['tmp_id']}
    headers = {"Authorization": "token 71c26bf67dc93c9:9f6b42ec03533c8"}
    response2 = requests.get(url, headers=headers, params=querystring)
    print(response2.json())

    # Create User
    url = "http://13.233.216.191/api/resource/User"
    body = {
        "email": email,
        "user": "Hitesh",
        "first_name": "Hitesh",
        "new_password": pwd,
        "roles": [
            {"role": "1tap_user"}
        ]
    }
    headers = {"Authorization": "token 71c26bf67dc93c9:9f6b42ec03533c8"}
    response3 = requests.post(url, headers=headers, json=body)
    print(response3.json())

def send_email():
    url = "http://13.233.216.191/api/method/one_tap_v1.api.send_email"
    payload = {
        "user_email": "hitesh.sahu@techbirdit.in",
        "subject": "Login Alert",
        "message": "You have been logged in successfully"
    }
    headers = {"Authorization": "token 71c26bf67dc93c9:9f6b42ec03533c8"}
    response = requests.post(url, json=payload, headers=headers)
    print(response.json())

def test():
    print("Vishal")