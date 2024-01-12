import pandas as pd
import ipaddress

def is_valid_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

# Load the CSV file
df = pd.read_csv('your_file.csv', header=None)  # Replace 'your_file.csv' with your file name

# Filter out rows where column 3 is not a valid IP address
df = df[df[2].apply(lambda x: is_valid_ip(x))]

# Find duplicates in columns 2-3
duplicates = df.duplicated(subset=[1, 2], keep=False)

# Filter the DataFrame to only include these duplicates
filtered_df = df[duplicates]

# Optional: Sort by columns 2 and 3 for better readability
sorted_df = filtered_df.sort_values(by=[1, 2])

# Save the processed data to a new CSV file
sorted_df.to_csv('processed_file.csv', index=False, header=False)
