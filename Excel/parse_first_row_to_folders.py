import openpyxl
import os

# Load the Excel workbook
workbook = openpyxl.load_workbook('C:/Users/hecki/Downloads/layer.xlsx')

# Select the active sheet
sheet = workbook.active

# Get the values from the first row
first_row = sheet[1]

# Iterate over each cell in the first row
for cell in first_row:
    folder_name = str(cell.value)
    
    # Replace invalid characters in the folder name
    folder_name = folder_name.replace(':', '_')
    
    # Create the folder if it doesn't exist
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"Created folder: {folder_name}")
    else:
        print(f"Folder already exists: {folder_name}")