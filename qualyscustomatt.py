import requests
from requests.auth import HTTPBasicAuth


def get_asset_id(username, password, ip_address):
    # Define the URL to fetch asset information
    url = 'https://qualysapi.qg4.apps.qualys.com/api/2.0/fo/asset/host/'  # Update with the correct API endpoint
    params = {
        'action': 'list',
        'ips': ip_address,
        'details': 'Basic'
    }
    response = requests.get(url, params=params, auth=HTTPBasicAuth(username, password))
    if response.status_code == 200:
        data = response.json()
        # Extract and return the asset ID from the response
        # Note: Update the JSON path according to the actual structure of the response
        return data['RESPONSE']['ASSET_LIST']['ASSET']['ID']
    else:
        return None

def update_qualys_asset_by_ip(username, password, asset_ip, custom_attributes):
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
                        "field": "ip",  # Assuming 'ip' is the correct field name
                        "operator": "EQUALS",
                        "value": asset_ip
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
asset_ip = '192.168.1.1'  # Replace with the actual IP address of the asset
custom_attributes = [
    {"key": "MyFirstCustomAttribute", "value": "QualysFunTeam"},
    {"key": "MyAssetProcurementID", "value": "QLYS 123456"}
]

response = update_qualys_asset_by_ip(username, password, asset_ip, custom_attributes)
print(response)
