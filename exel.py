import csv

def process_csv(input_file, output_file):
    try:
        with open(input_file, 'r', newline='', encoding='utf-8') as infile:
            reader = csv.reader(infile)
            processed_data = []

            for index, row in enumerate(reader):
                if len(row) < 4:
                    print(f"Skipping row {index + 1}: Insufficient columns")
                    continue

                # Strip whitespace and lower the case for accurate comparison
                col1, col2, col3, col4 = row[0].strip(), row[1].strip().lower(), row[2].strip().lower(), row[3].strip()

                # Compare values in columns 2 and 3
                if col2 == col3:
                    # If they match, append the row data to processed_data
                    processed_data.append([col1, col2, col3, col4])

        # Check if any data was processed
        if processed_data:
            with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
                writer = csv.writer(outfile)
                writer.writerows(processed_data)
                print(f"Processed data saved to {output_file}")
        else:
            print("No matching data found. Output file will be empty.")

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
process_csv('your_input_file.csv', 'your_output_file.csv')  # Replace with your actual file names
