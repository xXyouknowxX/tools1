import qualysapi
import xml.etree.ElementTree as ET

def fetch_option_profile_ids():
    """Fetches option profile IDs from Qualys."""

    # Connect to Qualys using the configuration file
    qgc = qualysapi.connect('qualysapi.ini')

    # API endpoint to list option profiles
    endpoint = '/api/2.0/fo/subscription/option_profile/'

    # Make the API request
    xml_output = qgc.request(endpoint)

    # Parse the XML response
    option_profiles = []
    root = ET.fromstring(xml_output)
    for profile in root.findall('.//OPTION_PROFILE'):
        profile_id = profile.find('ID').text
        profile_name = profile.find('TITLE').text
        option_profiles.append({'id': profile_id, 'name': profile_name})

    return option_profiles

def main():
    profiles = fetch_option_profile_ids()
    for profile in profiles:
        print(f"ID: {profile['id']}, Name: {profile['name']}")

if __name__ == "__main__":
    main()
