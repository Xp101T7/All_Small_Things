import pandas as pd

def excel_to_json(excel_path, json_path):
    # Load the Excel file
    df = pd.read_excel(excel_path)

    # Convert the DataFrame to JSON and save it
    df.to_json(json_path, orient='records', indent=4)

# Replace 'input_file.xlsx' with your Excel file path and 'output_file.json' with your desired JSON file path
excel_to_json('input_file.xlsx', 'output_file.json')
