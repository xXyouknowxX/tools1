import requests
from requests.auth import HTTPBasicAuth
import xml.etree.ElementTree as ET
import csv

def get_asset_id(username, password, ip_address):
    url = 'https://qualysapi.qg4.apps.qualys.com/api/2.0/fo/asset/host/'
    headers = {
        'X-Requested-With': 'curl',
        'Authorization': f'Bearer {password}'  # Assuming password is the token
    }
    params = {
        'action': 'list',
        'show_asset_id': '1',
        'host_metadata': 'all',
        'details': 'All',
        'ips': ip_address
    }
    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        try:
            root = ET.fromstring(response.content)
            for host in root.findall('.//HOST'):
                if host.find('IP').text == ip_address:
                    asset_id = host.find('ASSET_ID').text
                    return asset_id  # Return the ASSET_ID for the matching IP address
        except ET.ParseError as e:
            print("Error parsing the XML response:", e)
    else:
        print(f"API request failed with status code {response.status_code}, Response: {response.text}")

    return None

def update_qualys_asset(username, password, asset_id, owner_value):
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
                        "field": "id",
                        "operator": "EQUALS",
                        "value": asset_id
                    }
                ]
            },
            "data": {
                "Asset": {
                    "customAttributes": {
                        "add": {
                            "CustomAttribute": [
                                {"key": "Owner", "value": owner_value}
                            ]
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
password = 'your_password!'  # Replace with your token or password

# Read IP addresses and owner values from the CSV file
with open('assets.csv', newline='') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)  # Skip the header row
    for row in csvreader:
        ip_address, owner_value = row
        asset_id = get_asset_id(username, password, ip_address)
        if asset_id:
            response = update_qualys_asset(username, password, asset_id, owner_value)
            print(f'Updated asset {asset_id} with IP {ip_address} and response: {response}')
        else:
            print(f'No asset found for IP address {ip_address}')
