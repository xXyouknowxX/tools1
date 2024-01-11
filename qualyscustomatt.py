import requests
from requests.auth import HTTPBasicAuth
import xml.etree.ElementTree as ET

def get_asset_id(username, password, ip_address):
    url = 'https://qualysapi.qg4.apps.qualys.com/api/2.0/fo/asset/host/'  # Correct API endpoint
    params = {
        'action': 'list',
        'ips': ip_address,
        'details': 'Basic'
    }
    response = requests.get(url, params=params, auth=HTTPBasicAuth(username, password))
    
    if response.status_code == 200:
        root = ET.fromstring(response.content)
        # Loop through each HOST element and extract ASSET_ID
        for host in root.findall('.//HOST'):
            asset_id = host.find('ASSET_ID').text
            return asset_id  # Return the first found ASSET_ID
    else:
        return None

def update_qualys_asset(username, password, asset_id, custom_attributes):
    url = 'https://qualysapi.qg4.apps.qualys.com/qps/rest/2.0/update/am/asset'
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    data = {
        "ServiceRequest": {
            "filters": {
                "Criteria": [
                    {
                        "field": "id",  # Use 'id' since we have the asset ID
                        "operator": "EQUALS",
                        "value": asset_id
                    }
                ]
            },
            "data": {
                "Asset": {
                    "customAttributes": {
                        "add": {
                            "CustomAttribute": custom_attributes
                        }
                    }
                }
            }
        }
    }
    response = requests.post(url, json=data, headers=headers, auth=HTTPBasicAuth(username, password))
    return response.json()

# Example usage
username = 'your_username'
password = 'your_password!'
custom_attributes = [
    {"key": "MyFirstCustomAttribute", "value": "QualysFunTeam"},
    {"key": "MyAssetProcurementID", "value": "QLYS 123456"}
]

# Read IP addresses from a file
with open('ip_addresses.txt', 'r') as file:
    for ip_address in file:
        ip_address = ip_address.strip()
        asset_id = get_asset_id(username, password, ip_address)
        if asset_id:
            response = update_qualys_asset(username, password, asset_id, custom_attributes)
            print(f'Updated asset {asset_id} with response: {response}')
        else:
            print(f'No asset found for IP address {ip_address}')
