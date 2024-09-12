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
detection_values = [item["Detection"] for item in data if "Detection" in item]

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

# Write to CSV
fieldnames = ["EventID"]
with open(csv_file_path, mode='w', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(all_matches)

print(f"Data has been written to {csv_file_path}")