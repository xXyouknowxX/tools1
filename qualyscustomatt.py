import requests
from requests.auth import HTTPBasicAuth
import xml.etree.ElementTree as ET
import csv

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

# Read asset IDs and owner values from the CSV file
with open('assets.csv', newline='') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        asset_id, owner_value = row
        response = update_qualys_asset(username, password, asset_id, owner_value)
        print(f'Updated asset {asset_id} with response: {response}')

