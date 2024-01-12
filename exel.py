import csv

def process_csv(input_file, output_file):
    try:
        with open(input_file, 'r', newline='', encoding='utf-8') as infile:
            reader = csv.reader(infile)
            processed_data = []

            for index, row in enumerate(reader):
                try:
                    if len(row) < 4:
                        print(f"Skipping row {index + 1}: Insufficient columns")
                        continue

                    col1, col2, col3, col4 = row[0], row[1], row[2], row[3]

                    # Log the values for debugging
                    print(f"Row {index + 1} data: {col1}, {col2}, {col3}, {col4}")

                    # Check if columns 2 and 3 have the same values
                    if col2 == col3:
                        processed_data.append([col1, col2, col3, col4])
                        print(f"Added row {index + 1} to processed data")
                    else:
                        print(f"Skipping row {index + 1}: Column 2 and 3 values are not the same")
                except Exception as e:
                    print(f"Error processing row {index + 1}: {e}")

        # Check if any data is processed
        if processed_data:
            with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
                writer = csv.writer(outfile)
                writer.writerows(processed_data)
                print(f"Processed data saved to {output_file}")
        else:
            print("No data was processed. Output file will be empty.")

    except Exception as e:
        print(f"An error occurred while reading the file: {e}")

# Example usage
process_csv('your_input_file.csv', 'your_output_file.csv')
