import requests
from requests.auth import HTTPBasicAuth
import xml.etree.ElementTree as ET

def get_asset_id(username, password, ip_address):
    url = 'https://qualysapi.qg4.apps.qualys.com/api/2.0/fo/asset/host/'
    headers = {
        'X-Requested-With': 'curl',
        'Authorization': f'Bearer {password}'  # Adjust with correct authorization
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
                    return asset_id
        except ET.ParseError as e:
            print("Error parsing the XML response:", e)
    else:
        print(f"API request failed with status code {response.status_code}, Response: {response.text}")

    return None

# Example usage
username = 'your_username'
password = 'your_password!'  # or your token

# Ask the user to enter the IP address
ip_address_to_search = input("Enter the IP address to search for: ")

asset_id = get_asset_id(username, password, ip_address_to_search)
if asset_id:
    print(f'Asset ID for IP address {ip_address_to_search} is: {asset_id}')
else:
    print(f'No asset found for IP address {ip_address_to_search}')
