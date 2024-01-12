import pandas as pd
import ipaddress

def is_valid_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def process_csv(file_name, output_file_name):
    try:
        # Load the CSV file
        df = pd.read_csv(file_name, header=None)

        # Filter out rows where column 3 is not a valid IP address
        df = df[df[2].apply(lambda x: isinstance(x, str) and is_valid_ip(x))]

        # Find duplicates in columns 2-3
        duplicates = df.duplicated(subset=[1, 2], keep=False)

        # Filter the DataFrame to only include these duplicates
        filtered_df = df[duplicates]

        # Optional: Sort by columns 2 and 3 for better readability
        sorted_df = filtered_df.sort_values(by=[1, 2])

        # Save the processed data to a new CSV file
        sorted_df.to_csv(output_file_name, index=False, header=False)
        print(f"Processed file saved as {output_file_name}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
process_csv('your_file.csv', 'processed_file.csv')  # Replace with your file names
