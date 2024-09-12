import json
import re
import csv

# File paths
json_file_path = 'dummy_data_simple.json'
csv_file_path = 'event_data_output.csv'

# Load the JSON data
with open(json_file_path, 'r') as file:
    data = json.load(file)

# Extract "Detection" values
detection_values = [item.get("Detection", "") for item in data]

# Print first few detection values for debugging
print("First few Detection values:")
for i, detection in enumerate(detection_values[:5]):
    print(f"{i+1}: {detection[:100]}...")  # Print first 100 characters

# Define patterns for EventID
event_id_patterns = [
    re.compile(r'EventID\s*(?:=|==|:|\bin\b)\s*(?:\'|\")?\s*(\d{1,6})\s*(?:\'|\")?', re.IGNORECASE),
    re.compile(r'EventID\s+in\s*\((\'|\")?\s*(\d{1,6})(?:\s*,\s*(?:\'|\")?\d{1,6}(?:\'|\")?\s*)*\)', re.IGNORECASE),
    re.compile(r'EventID:?\s*\n\s*-\s*(\d{1,6})(?:\s*\n\s*-\s*\d{1,6})*', re.IGNORECASE),
    re.compile(r'EventID:?\s*(\d{1,6})', re.IGNORECASE),
    re.compile(r'\bevent_id\s*[=:]\s*(\d{1,6})', re.IGNORECASE)
]

# Function to find EventID using multiple patterns
def find_event_id(detection):
    for pattern in event_id_patterns:
        match = pattern.search(detection)
        if match:
            return match.group(1)  # Return the first captured group
    return None

# Collect the matches
all_matches = []
for detection in detection_values:
    if isinstance(detection, str):
        event_id = find_event_id(detection)
        if event_id:
            all_matches.append({"EventID": event_id})
        else:
            print(f"No match found in: {detection[:100]}...")  # Print first 100 characters of non-matching detections

# Print debugging information
print(f"Total detections processed: {len(detection_values)}")
print(f"Total matches found: {len(all_matches)}")

# If no matches found, let's try a more general pattern
if not all_matches:
    print("No matches found with specific patterns. Trying a more general pattern.")
    general_pattern = re.compile(r'(?:event|id|eventid).*?(\d{1,6})', re.IGNORECASE)
    for detection in detection_values:
        if isinstance(detection, str):
            match = general_pattern.search(detection)
            if match:
                all_matches.append({"EventID": match.group(1)})

    print(f"Matches found with general pattern: {len(all_matches)}")

# Write to CSV
if all_matches:
    fieldnames = ["EventID"]
    with open(csv_file_path, mode='w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_matches)
    print(f"Data has been written to {csv_file_path}")
else:
    print("No matches found. CSV file was not created.")

# Print a sample of matches
print("\nSample of matches found:")
for match in all_matches[:5]:
    print(match)