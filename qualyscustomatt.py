import requests
from requests.auth import HTTPBasicAuth

def get_asset_id(username, password, ip_address):
    url = 'https://qualysapi.qg4.apps.qualys.com/api/2.0/fo/asset/host/'  # Update with the correct API endpoint
    params = {
        'action': 'list',
        'ips': ip_address,
        'details': 'Basic'
    }
    response = requests.get(url, params=params, auth=HTTPBasicAuth(username, password))
    if response.status_code == 200:
        data = response.json()
        # Update the JSON path according to the actual structure of the response
        # Example: return data['RESPONSE']['ASSET_LIST'][0]['ID']
        return data['RESPONSE']['ASSET_LIST']['ASSET']['ID']  # Adjust this line
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
