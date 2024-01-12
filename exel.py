import csv

def process_csv(input_file, output_file):
    try:
        with open(input_file, 'r', newline='', encoding='utf-8') as infile:
            reader = csv.reader(infile)
            processed_data = []

            for index, row in enumerate(reader):
                try:
                    if len(row) < 4:
                        continue  # Skip rows with insufficient columns

                    col1, col2, col3, col4 = row[0], row[1], row[2], row[3]

                    # Skip rows where col3 contains non-numeric characters (like 'cloudprov')
                    if any(char.isalpha() for char in col3):
                        continue

                    if col2 == col3:  # Check if columns 2 and 3 have the same values
                        processed_data.append([col1, col2, col3, col4])  # Keep cols 1, 2, 3, and 4
                except Exception as e:
                    print(f"Error processing row {index + 1}: {e}")

        with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)
            writer.writerows(processed_data)
            print(f"Processed data saved to {output_file}")

    except Exception as e:
        print(f"An error occurred while reading the file: {e}")

# Example usage
process_csv('your_input_file.csv', 'your_output_file.csv')  # Replace with your actual file names
