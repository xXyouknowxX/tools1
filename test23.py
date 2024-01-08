import requests
import getpass

def launch_qualys_scan(username, password, scan_title, ip_addresses, option_id, iscanner_name):
    """Launch a scan in Qualys using IP addresses."""

    # Endpoint URL to launch a scan
    url = 'https://qualysapi.qualys.com/api/2.0/fo/scan/'

    # Headers
    headers = {'X-Requested-With': 'curl demo'}

    # Data payload
    data = {
        'action': 'launch',
        'scan_title': scan_title,
        'ip': ip_addresses,
        'option_id': option_id,
        'iscanner_name': iscanner_name
    }

    # Make the POST request with HTTP Basic Authentication
    response = requests.post(url, auth=(username, password), headers=headers, data=data)
    
    # Check if request was successful
    if response.status_code != 200:
        raise Exception("Error in launching scan: " + response.text)

    return response.text

def main():
    username = input("Enter your Qualys username: ")
    password = getpass.getpass("Enter your Qualys password: ")

    scan_title = input("Enter the scan title: ")
    ip_addresses = input("Enter IP addresses (comma-separated): ")
    option_id = input("Enter the option ID: ")
    iscanner_name = input("Enter the scanner name: ")

    response = launch_qualys_scan(username, password, scan_title, ip_addresses, option_id, iscanner_name)
    print(response)

if __name__ == "__main__":
    main()
