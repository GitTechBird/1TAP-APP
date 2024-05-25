import frappe

SERVICE_METADATA = {
    "CompanySetup": {
        "LicenseType": [
                "Commercial(Includes Trade)",
                "Professional(Include Service & Consultancy)",
                "Combination(Additional Charges may apply)",
            ],
        "Country": frappe.get_list("Country", pluck="name"),
        "LicenseZone": frappe.get_list("OT Zone Master", pluck="name"),
    }
}