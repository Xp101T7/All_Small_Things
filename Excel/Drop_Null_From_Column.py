import pandas as pd

def delete_null_rows(file_path, column_name):
    # Load the Excel file
    df = pd.read_excel(file_path)

    # Drop rows where the specified column is null
    df.dropna(subset=[column_name], inplace=True)

    # Save the cleaned data back to Excel
    df.to_excel(file_path, index=False)

# Replace 'your_file.xlsx' with your file path and 'your_column' with your column name
delete_null_rows('your_file.xlsx', 'your_column')
