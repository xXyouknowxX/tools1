import qualysapi

def start_scan(scan_title, scan_target):
    """Start a new scan."""
    qgc = qualysapi.connect('qualysapi.ini')
    parameters = {
        'action': 'launch',
        'scan_title': scan_title,
        'ip': scan_target,
        'option_id': 'your_option_profile_id'  # Replace with your option profile ID
    }
    xml_output = qgc.request('/api/2.0/fo/scan/', parameters)
    return xml_output

def main():
    scan_title = 'My Security Scan'
    scan_target = '192.168.1.1'  # Replace with your target IP or range
    xml_response = start_scan(scan_title, scan_target)
    
    print(xml_response)

if __name__ == "__main__":
    main()
