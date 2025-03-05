from azure.identity import AzureCliCredential
from dotenv import load_dotenv
import requests
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve subscriptionId from .env file
subscriptionId = os.getenv("SUBSCRIPTION_ID")

if not subscriptionId:
    raise ValueError("SUBSCRIPTION_ID not found in .env file. Please add it.")

# Authenticate using Azure CLI credentials
credential = AzureCliCredential()

# Get the access token
access_token = credential.get_token("https://management.azure.com/.default").token

api_version = "2019-01-01-preview"

# 1. get Regulatory Compliance Standars
# Construct the URL
url = f"https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.Security/regulatoryComplianceStandards?api-version={api_version}"

# Set up headers with the access token
headers = {
    "Authorization": f"Bearer {access_token}"
}

# Make the API request
response = requests.get(url, headers=headers)

# Check the response
if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print(f"Error: {response.status_code}")
    print(response.json())


# 2. list all controls
# API endpoint
standard_name = "CIS-Azure-Foundations-v2.0.0"
url = f"https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.Security/regulatoryComplianceStandards/{standard_name}/regulatoryComplianceControls?api-version={api_version}"

# Headers with access token
headers = {
    "Authorization": f"Bearer {access_token}"
}

# Make the API call
response = requests.get(url, headers=headers)
if response.status_code == 200:
    controls = response.json().get("value", [])
    for control in controls:
        print(f"Control ID: {control['id']}")
        print(f"Control Name: {control['name']}")
        print(f"State: {control['properties']['state']}")
        print(f"Description: {control['properties']['description']}")
        print("------")
else:
    print(f"Failed to fetch controls. Status code: {response.status_code}")
    print(response.json())
