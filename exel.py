import csv

def is_valid_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def process_csv(input_file, output_file):
    try:
        with open(input_file, 'r', newline='', encoding='utf-8') as infile:
            reader = csv.reader(infile)
            processed_data = []

            for row in reader:
                if len(row) < 4:
                    continue  # Skip rows that don't have enough columns

                # Assuming columns are 0-indexed in description
                col2, col3 = row[1], row[2]
                if is_valid_ip(col3) and col2 == col3:  # Check if col3 is a valid IP and col2 equals col3
                    processed_data.append([row[0], col2, col3, row[3]])  # Keep cols 1, 2, 3, and 4

        # Writing processed data to output file
        with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)
            writer.writerows(processed_data)
            print(f"Processed data saved to {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
process_csv('your_input_file.csv', 'your_output_file.csv')  # Replace with your actual file names
