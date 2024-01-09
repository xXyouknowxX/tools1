# cloudflareexporttool

import requests
import csv
import getpass


Text= """   ___ _                 _   ___ _                    __                       _     _____            _ 
  / __\ | ___  _   _  __| | / __\ | __ _ _ __ ___    /__\_  ___ __   ___  _ __| |_  /__   \___   ___ | |
 / /  | |/ _ \| | | |/ _` |/ _\ | |/ _` | '__/ _ \  /_\ \ \/ / '_ \ / _ \| '__| __|   / /\/ _ \ / _ \| |
/ /___| | (_) | |_| | (_| / /   | | (_| | | |  __/ //__  >  <| |_) | (_) | |  | |_   / / | (_) | (_) | |
\____/|_|\___/ \__,_|\__,_\/    |_|\__,_|_|  \___| \__/ /_/\_\ .__/ \___/|_|   \__|  \/   \___/ \___/|_|
                                                             |_|                                        """

print(Text)
print ('This tool can export a list with all your DNS records and Firewall rules from your cloudflare zones')
print ("""Your personal Token MUST have the following permissions: 
 _________________________________________      
| Zone: Read     | DNS: Read              |
| Zone WAF: Read | FireWall Serivce: Read |
¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯    """ )      
          

# Cloudflare credentials
api_token = getpass.getpass("Enter your personal API Token: ")
email = input("Enter your personal Cloudflare email: ")

# Cloudflare API URL
base_url = 'https://api.cloudflare.com/client/v4'

#Function to fetch zones
def fetch_zones(api_token):
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json'
    }
    response = requests.get(f'{base_url}/zones', headers=headers)
    data = response.json()
    print('Your zones are: ')
    return data.get('result', [])    

#Function to fetch DNS record for a given zone
def fetch_dns_records( zone_id): 
    url =   f'{base_url}/zones/{zone_id}/dns_records'
    headers = {
        'X-Auth-Email': f'email {email}',
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json'
    }
    all_records = []
    page = 1
    total_pages = 1
    while page <= total_pages:
        params = {
            'page': page,
            'per_page': 100
        }
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        if not data['success']:
            raise Exception("Faild to fetch DNS record")
        all_records.extend(data['result'])
        total_pages = data['result_info']['total_pages']
        page +=1 
    return all_records

#Function to fetch Firewall rules for a given zone
def fetch_firewall_rules( zone_id):
    all_rules = []
    page = 1
    per_page = 100
    while True:
        url = f'{base_url}/zones/{zone_id}/firewall/rules?page={page}'f'&per_page={per_page}'
        headers = {
            'X-Auth-Email': f'email {email}',
            'Authorization': f'Bearer {api_token}',
            'Content-Type': 'application/json'
        }
        response = requests.get(url, headers=headers)
        data_fw = response.json()
        rules = data_fw.get('result', [])
        if not rules:
            break
        all_rules.extend(rules)
        total_pages = data_fw.get('result_info', {}).get('total_pages', 0)
        if page >= total_pages:
            break
        page += 1
    return all_rules

#Function to fetch Rulesets  for a given zone
def fetch_zone_rulesets_ids_and_details(zone_id, api_token):   
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json'
    }
    response = requests.get(f'{base_url}/zones/{zone_id}/rulesets', headers=headers)
    data2 = response.json()
    if not data2.get('success'):
        print ('Eroor')  
        return []    
    ruleset_details_list = []
    for ruleset in data2.get('result', []):
        ruleset_id = ruleset.get('id')
        if ruleset_id:
            url_details = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/rulesets/{ruleset_id}'
            response_details = requests.get(url_details, headers=headers)
            data_details = response_details.json()
            if data_details.get('success'):
                 detail = data_details.get('result')
                 print(f' fetched details for ruleset id: {ruleset_id} at url: {url_details}')
                 ruleset_details_list.append(detail)
        else:
                print(f'faild to fetch details for ruleset id: {ruleset_id} at url: {url_details}')
    return ruleset_details_list
 
    
def main():
    print("Fetching zones...")
    zones = fetch_zones(api_token)

    if zones:
        for idx, zone in enumerate(zones, start=1):
            print(f"{idx}. {zone['name']} (ID: {zone['id']})")
        print(f"{len(zones) + 1}. Export all zones")

        try:
            choice = int(input("Enter the number of the zone to export (or the last number to export all): "))
            if choice == len(zones) + 1:
                for zone in zones:
                    export_zone_data(zone)
            elif 1 <= choice <= len(zones):
                selected_zone = zones[choice - 1]
                export_zone_data(selected_zone)
            else:
                print("Invalid input. Please enter a valid number.")
        except (ValueError, IndexError):
            print("Invalid input. Please enter a valid number.")
            return

def export_zone_data(zone):
    zone_id = zone['id']
    zone_name = zone['name']

    firewall_rules = fetch_firewall_rules(zone_id)
    ruleset_details = fetch_zone_rulesets_ids_and_details(zone_id, api_token)
    dns_records = fetch_dns_records(zone_id)

    # New code to print and save FQDNs
    fqdn_filename = f"fqdns_{zone_name}.txt"
    with open(fqdn_filename, 'w') as fqdn_file:
        for record in dns_records:
            if record['type'] in ['A', 'AAAA', 'CNAME']:
                fqdn = record['name']
                print(fqdn)
                fqdn_file.write(fqdn + '\n')

    filename = f"dns_record_export_{zone_name}.csv"
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        data = fetch_dns_records(zone_id)
        data1 = fetch_firewall_rules (zone_id)
        data3 = fetch_zone_rulesets_ids_and_details (zone_id, api_token)


    if data:
        records = data
        ruleset_details_list = data3
        firewall_rules = data1 
        filename = f"dns_record_export_{zone_name}.csv"
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Zone ID', 'Type', 'Name', 'Content', 'Proxiable','Proxied', 'TTL', 'Comment', 'Tags', 'Zone Name'])
            for record in records:
                writer.writerow([record.get(field, 'N/A') for field in ['id', 'type','name', 'content','proxiable', 'proxied', 'ttl', 'comment', 'tags', 'zone_name']])
            writer.writerow([])
            writer.writerow([])
            writer.writerow([])
            writer.writerow(['Firewall Rules'])
            writer.writerow([])
            writer.writerow(['Rule ID', 'Action', 'Description', 'Expression', 'Rule description'])
            for rule in firewall_rules:
                if not isinstance(rule, dict):
                    continue
                filter_info = rule.get('filter', {})
                writer.writerow([
                    rule.get('id'),
                    rule.get('action'),
                    rule.get('description'),
                    filter_info.get('expression'),
                    filter_info.get('description')
                ])
            writer.writerow([])
            writer.writerow([])
            writer.writerow([])
            writer.writerow(['Rulesets'])
            writer.writerow([])
            writer.writerow(['Ruleset ID','Name',  'Ruleset description', 'Action', 'Categories', 'Description', 'Expression', 'Last Updated','ID','Phase'])
            for details in ruleset_details_list:
                rules_info =  details.get ('rules', [])
                for rule in rules_info:
                    #print(rule)     
                    if isinstance(rule, dict):
                        writer.writerow([
                            # details.get('rules'), ## this can displey the whole rule section of the response
                            details.get('id', 'N/A'),
                            details.get('name', 'N/A'),
                            details.get('description', 'N/A'),
                            rule.get('action', 'N/A'),
                            rule.get('categories', 'N/A'),
                            rule.get('description', 'N/A'),
                            rule.get('expression', 'N/A'),
                            rule.get('last_updated', 'N/A'),
                            rule.get('id', 'N/A')

                        ])
        print (f"DNS record, FW rules and Rulesets exported to {filename}")


if __name__ == "__main__":
    main()