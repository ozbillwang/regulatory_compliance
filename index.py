import os
import requests
from dotenv import load_dotenv
from azure.identity import AzureCliCredential

# Load environment variables from .env file
load_dotenv()

# Fetch high_priority_list from .env
subscription_id = os.getenv("SUBSCRIPTION_ID")
high_priority_list = os.getenv("HIGH_PRIORITY_LIST", "").split(",")

if not subscription_id:
    raise ValueError("SUBSCRIPTION_ID not found in .env file. Please add it.")

# Replace these with your Azure AD app details
# tenant_id = "your-tenant-id"
# client_id = "your-client-id"
# client_secret = "your-client-secret"
# subscription_id = "your-subscription-id"
standard_name = "CIS-Azure-Foundations-v2.0.0"  # Example standard
api_version = "2019-01-01-preview"

# Step 1: Get Access Token
# def get_access_token():
#     url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
#     headers = {
#         "Content-Type": "application/x-www-form-urlencoded"
#     }
#     data = {
#         "grant_type": "client_credentials",
#         "client_id": client_id,
#         "client_secret": client_secret,
#         "scope": "https://management.azure.com/.default"
#     }
#     response = requests.post(url, headers=headers, data=data)
#     return response.json().get("access_token")
def get_access_token():
    credential = AzureCliCredential()
    return credential.get_token("https://management.azure.com/.default").token
# Step 2: Fetch Controls
def fetch_controls(access_token):
    url = f"https://management.azure.com/subscriptions/{subscription_id}/providers/Microsoft.Security/regulatoryComplianceStandards/{standard_name}/regulatoryComplianceControls?api-version={api_version}"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("value", [])
    else:
        print(f"Failed to fetch controls. Status code: {response.status_code}")
        print(response.json())
        return []

# Step 3: Check Conditions and Print Relevant Controls
def check_and_print_controls(controls):
    for control in controls:
        control_id = control["name"]  # Control ID (e.g., "3.7")
        control_state = control["properties"]["state"]  # State (e.g., "Passed", "Failed")
        control_description = control["properties"]["description"]  # Description

        # Check if control is in high_priority_list and state is not "Passed"
        if control_id in high_priority_list and control_state != "Passed":
            print(f"Control ID: {control_id}")
            print(f"State: {control_state}")
            print(f"Description: {control_description}")
            print("------")

# Main Function
def main():
    # Step 1: Get Access Token
    access_token = get_access_token()
    if not access_token:
        print("Failed to get access token.")
        return

    # Step 2: Fetch Controls
    controls = fetch_controls(access_token)
    if not controls:
        print("No controls found.")
        return

    # Step 3: Check Conditions and Print Relevant Controls
    check_and_print_controls(controls)

if __name__ == "__main__":
    main()
