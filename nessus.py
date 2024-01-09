import requests
import json

def get_nessus_auth_token(username, password, nessus_url):
    """Authenticate with Nessus and return the auth token."""
    url = f"{nessus_url}/session"
    data = {"username": username, "password": password}
    response = requests.post(url, json=data)
    return response.json().get('token')

def create_scan(nessus_url, auth_token, scan_name, targets):
    """Create a new scan in Nessus."""
    url = f"{nessus_url}/scans"
    headers = {'X-Cookie': f'token={auth_token}', 'Content-Type': 'application/json'}
    scan_data = {
        "uuid": "template_uuid",  # Replace with actual template UUID
        "settings": {
            "name": scan_name,
            "text_targets": targets
        }
    }
    response = requests.post(url, headers=headers, json=scan_data)
    return response.json()

def launch_scan(nessus_url, auth_token, scan_id):
    """Launch the scan."""
    url = f"{nessus_url}/scans/{scan_id}/launch"
    headers = {'X-Cookie': f'token={auth_token}'}
    response = requests.post(url, headers=headers)
    return response.json()

def read_targets_from_file(file_path):
    """Reads targets from a file and returns them as a string."""
    with open(file_path, 'r') as file:
        return ','.join([line.strip() for line in file if line.strip()])

def main():
    nessus_url = "https://your-nessus-instance:8834"  # Replace with your Nessus instance URL
    username = input("Enter your Nessus username: ")
    password = input("Enter your Nessus password: ")
    scan_name = input("Enter the scan name: ")
    file_path = input("Enter the file path for the targets: ")

    targets = read_targets_from_file(file_path)
    auth_token = get_nessus_auth_token(username, password, nessus_url)
    scan_response = create_scan(nessus_url, auth_token, scan_name, targets)
    scan_id = scan_response.get('scan', {}).get('id')

    if scan_id:
        launch_response = launch_scan(nessus_url, auth_token, scan_id)
        print(f"Scan launched: {launch_response}")
    else:
        print("Failed to create scan.")

if __name__ == "__main__":
    main()
