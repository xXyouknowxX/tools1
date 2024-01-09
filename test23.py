import requests
import getpass
import xml.etree.ElementTree as ET

def fetch_option_profile_ids(username, password):
    """Fetches option profile IDs from Qualys."""

    url = 'https://qualysapi.qualys.com/api/2.0/fo/subscription/option_profile/'
    params = {'action': 'list'}
    auth = (username, password)

    response = requests.get(url, params=params, auth=auth)
    if response.status_code != 200:
        raise Exception("Error fetching option profiles: " + response.text)

    option_profiles = []
    root = ET.fromstring(response.text)
    for profile in root.findall('.//OPTION_PROFILE'):
        profile_id = profile.find('ID').text
        profile_name = profile.find('TITLE').text
        option_profiles.append((profile_id, profile_name))

    return option_profiles

def launch_qualys_scan(username, password, scan_title, ip_addresses, option_id, iscanner_name):
    """Launch a scan in Qualys using IP addresses."""

    url = 'https://qualysapi.qualys.com/api/2.0/fo/scan/'
    headers = {'X-Requested-With': 'curl demo'}
    data = {
        'action': 'launch',
        'scan_title': scan_title,
        'ip': ip_addresses,
        'option_id': option_id,
        'iscanner_name': iscanner_name
    }

    response = requests.post(url, auth=(username, password), headers=headers, data=data)
    if response.status_code != 200:
        raise Exception("Error in launching scan: " + response.text)

    return response.text

def read_targets_from_file(file_path):
    """Reads targets from a file and returns them as two lists: IPs and FQDNs."""
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file if line.strip()]
        ip_targets = [line for line in lines if '.' in line]  # Simple check for IPs and FQDNs
        fqdn_targets = [line for line in lines if line not in ip_targets]
    return ip_targets, fqdn_targets

def main():
    username = input("Enter your Qualys username: ")
    password = getpass.getpass("Enter your Qualys password: ")

    # Fetch and choose option profile ID
    option_profiles = fetch_option_profile_ids(username, password)
    print("Available Option Profiles:")
    for id, name in option_profiles:
        print(f"ID: {id}, Name: {name}")
    
    option_id = input("Enter the chosen Option Profile ID: ")

    # Read targets from file
    file_path = input("Enter the file path for the targets: ")
    targets = read_targets_from_file(file_path)
    ip_addresses = ','.join(targets)  # Converts list of targets to a comma-separated string

    scan_title = input("Enter the scan title: ")
    iscanner_name = input("Enter the scanner name: ")

    # Launch the scan
    response = launch_qualys_scan(username, password, scan_title, ip_addresses, option_id, iscanner_name)
    print(response)

if __name__ == "__main__":
    main()
