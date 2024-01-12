import csv

def process_csv(input_file, output_file):
    try:
        with open(input_file, 'r', newline='', encoding='utf-8') as infile:
            reader = csv.reader(infile)
            rows = list(reader)
            processed_data = []

            # Iterate through each row
            for row in rows:
                if len(row) < 4:
                    continue  # Skip if the row doesn't have enough columns

                col1, col2 = row[0].strip(), row[1].strip().lower()

                # Search for matches in column 3 of all rows
                for target_row in rows:
                    col3, col4 = target_row[2].strip().lower(), target_row[3].strip()
                    if col2 == col3:
                        # If a match is found, append the data to processed_data
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
