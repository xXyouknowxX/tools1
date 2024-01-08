import requests
import xml.etree.ElementTree as ET
import configparser

def fetch_option_profile_ids(config_file):
    """Fetches option profile IDs from Qualys using GET request."""
    
    # Read configuration file
    config = configparser.ConfigParser()
    config.read(config_file)

    hostname = config['qualys']['hostname']
    username = config['qualys']['username']
    password = config['qualys']['password']

    # Endpoint URL to list option profiles
    url = f'https://{hostname}/api/2.0/fo/subscription/option_profile/'
    
    # Parameters for the GET request
    params = {'action': 'list'}

    # Make the GET request with HTTP Basic Authentication
    response = requests.get(url, params=params, auth=(username, password))
    
    # Check if request was successful
    if response.status_code != 200:
        raise Exception("Error fetching option profiles: " + response.text)

    # Parse the XML response
    option_profiles = []
    root = ET.fromstring(response.text)
    for profile in root.findall('.//OPTION_PROFILE'):
        profile_id = profile.find('ID').text
        profile_name = profile.find('TITLE').text
        option_profiles.append({'id': profile_id, 'name': profile_name})

    return option_profiles

def main():
    config_file = 'qualys_config.ini'
    profiles = fetch_option_profile_ids(config_file)
    for profile in profiles:
        print(f"ID: {profile['id']}, Name: {profile['name']}")

if __name__ == "__main__":
    main()
