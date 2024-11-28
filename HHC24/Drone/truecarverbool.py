import csv

# Input file path
input_file = r"C:\Users\hecki\Downloads\ELF-HAWK-dump.csv"


# Initialize a list to store the extracted TRUE and FALSE values
extracted_values = []

# Read the CSV file
with open(input_file, mode='r') as file:
    reader = csv.reader(file)
    for row in reader:
        for value in row:
            # Normalize the value and check if it's TRUE or FALSE
            if isinstance(value, str):
                value_normalized = value.strip().upper()
                if value_normalized == "TRUE":
                    extracted_values.append(1)  # Replace TRUE with 1
                elif value_normalized == "FALSE":
                    extracted_values.append(0)  # Replace FALSE with 0

# Output the extracted and converted values
print("Extracted and converted values (1 for TRUE, 0 for FALSE):", extracted_values)

output_file = r"C:\Users\hecki\Prog\All_Small_Things\HHC24\Drone\filtered_data.csv"
with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(extracted_values)  # Write the values in a single row

print(f"Extracted values saved to {output_file}")