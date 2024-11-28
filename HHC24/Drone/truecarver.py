import pandas as pd

# Input and output file paths
input_file = r"C:\Users\hecki\Downloads\ELF-HAWK-dump.csv"
output_file = r"C:\Users\hecki\Prog\All_Small_Things\HHC24\Drone\filtered_data.csv"

# Read the CSV file into a DataFrame
df = pd.read_csv(input_file)

# Filter rows where any column contains the value "TRUE"
filtered_df = df[df.apply(lambda row: row.astype(str).str.upper().eq("TRUE").any(), axis=1)]

# Write the filtered rows to a new CSV file
filtered_df.to_csv(output_file, index=False)

print(f"Filtered rows saved to {output_file}")
