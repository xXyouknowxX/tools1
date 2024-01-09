import requests
import getpass
import xml.etree.ElementTree as ET
import re
import glob
import os

def find_target_file():
    return glob.glob('fqdns_*.txt')

def fetch_option_profile_ids(username, password):
    """Fetches option profile IDs from Qualys."""

    url = 'https://qualysapi.qg2.apps.qualys.eu/api/2.0/fo/subscription/option_profile/vm/'
    headers = {'X-Requested-With': 'curl demo'}
    params = {'action': 'list'}
    auth = (username, password)

    response = requests.get(url, headers=headers ,params=params, auth=auth)
    #print(response.text) DEBUG STATEMENT
    if response.status_code != 200:
        raise Exception("Error fetching option profiles: " + response.text)

    option_profiles = []
    root = ET.fromstring(response.text)
    for profile in root.findall('.//OPTION_PROFILE'):
        profile_id = profile.find('BASIC_INFO/ID').text
        group_name = profile.find('BASIC_INFO/GROUP_NAME').text
        option_profiles.append((profile_id, group_name))

    return option_profiles

def launch_qualys_scan(username, password, scan_title, option_id, fqdn_targets):
    """Launch a scan in Qualys using IP addresses."""

    url = 'https://qualysapi.qg2.apps.qualys.eu/api/2.0/fo/scan/'
    headers = {'X-Requested-With': 'curl demo'}
    data = {
        'action': 'launch',
        'scan_title': scan_title,
        'fqdn': fqdn_targets,
        'option_id': option_id,
        'iscanner_name': 'VA-Modena'
    }
    response = requests.post(url, auth=(username, password), headers=headers, data=data)
    if response.status_code != 200:
        raise Exception("Error in launching scan: " + response.text)
    return response.text

def split_file_if_needed(file_path, char_limit=4000):
    """Splits the file at line breaks if it exceeds a specified character limit."""
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    total_size = sum(len(line) for line in lines)

    # If the file is within the limit, return the original file path
    if total_size <= char_limit:
        return [file_path]

    current_size = 0
    current_part = []
    parts = []

    for line in lines:
        if current_size + len(line) > char_limit:
            parts.append(''.join(current_part))
            current_part = []
            current_size = 0
        current_part.append(line)
        current_size += len(line)

    # Add the last part if there's any
    if current_part:
        parts.append(''.join(current_part))

    file_base_name = os.path.splitext(os.path.basename(file_path))[0]
    split_file_paths = []

    for i, part in enumerate(parts):
        part_file_path = f"{file_base_name}_part{i+1}.txt"
        with open(part_file_path, 'w', encoding='utf-8') as file:
            file.write(part)
        split_file_paths.append(part_file_path)

    return split_file_paths

def read_targets_from_file(file_path):
    """Reads IP addresses and FQDNs from a file, identifying each."""
    ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
    fqdn_pattern = r'\b(?:[a-zA-Z\d-]{,63}\.)+[a-zA-Z]{2,63}\b'
    all_ips, all_fqdns = [], []
    for file_path in split_file_if_needed(file_path):
        with open(file_path, 'r') as file:
            lines = file.read().splitlines()        
            ips = [line for line in lines if re.fullmatch(ip_pattern, line)]
            fqdns = [line for line in lines if re.fullmatch(fqdn_pattern, line)]
            # all_fqdns.extend(fqdns)

        return ','.join(fqdns)
    #return all_fqdns

def get_scan_name(file_path):
    base_name = os.path.basename(file_path)
    scan_name = base_name.replace('fqdns_', '').replace('.txt', '')
    return f"{scan_name} scan"

def main():
    username = input("Enter your Qualys username: ")
    password = getpass.getpass("Enter your Qualys password: ")

    # Fetch and choose option profile ID
    option_profiles = fetch_option_profile_ids(username, password)
    print("Available Option Profiles:")
    for id, name in option_profiles:
        print(f"ID: {id}, Name: {name}")
    
    option_id = input("Enter the chosen Option Profile ID: ")
    target_files = find_target_file()
    # Read targets from file
    for file_path in target_files:
        print(f"processing file: {file_path}")
        fqdn_targets = read_targets_from_file(file_path)
        scan_title = get_scan_name(file_path)
        #ip_targets_str = ','.join(ip_targets)  # Converts list of targets to a comma-separated string  
        # iscanner_name = input("Enter the scanner name: ")
        # Launch the scan
        response = launch_qualys_scan(username, password, scan_title, option_id, fqdn_targets)  #ip_targets_str, fqdn_targets_str,
        print(response)

if __name__ == "__main__":
    main()