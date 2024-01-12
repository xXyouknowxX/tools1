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

                # Pair up values from columns 1-2 and 3-4
                pair1 = (row[0], row[1])  # Pair from columns 1 and 2
                pair2 = (row[2], row[3])  # Pair from columns 3 and 4

                # Compare the second elements of each pair (columns 2 and 3)
                if pair1[1].strip() == pair2[0].strip():
                    # If they match, append both pairs side by side
                    processed_data.append(pair1 + pair2)

        with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)
            writer.writerows(processed_data)
            print(f"Processed data saved to {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
process_csv('your_input_file.csv', 'your_output_file.csv')
