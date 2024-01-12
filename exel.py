import pandas as pd

# Load the CSV file
df = pd.read_csv('your_file.csv', header=None)  # Replace 'your_file.csv' with your file name

# Assuming columns are numbered from 1 in your description, 
# but pandas uses 0-indexing (so we adjust to 0-1 for cols 1-2 and 2-3)
locked_columns = df.iloc[:, [0, 1, 2, 3]]  

# Find duplicates in columns 2-3
duplicates = locked_columns.duplicated(subset=[1, 2], keep=False)

# Filter the DataFrame to only include these duplicates
filtered_df = locked_columns[duplicates]

# Optional: Sort by columns 2 and 3 for better readability
sorted_df = filtered_df.sort_values(by=[1, 2])

# Save the processed data to a new CSV file
sorted_df.to_csv('processed_file.csv', index=False, header=False)
